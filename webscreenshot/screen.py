#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import subprocess
import random
import datetime
import time
import signal
import multiprocessing
import itertools
import shlex
import logging
import errno

reload(sys)
sys.setdefaultencoding('utf-8')
# Script version
VERSION = '2.2.2'

# OptionParser imports
from optparse import OptionParser
from optparse import OptionGroup

# Options definition
parser = OptionParser()

main_grp = OptionGroup(parser, 'Main parameters')
main_grp.add_option('--input-file',default = 'gde.txt', nargs = 1)
main_grp.add_option('--output-directory', help = '(default \'./screenshots/\')', nargs = 1)
main_grp.add_option('--renderer', default = 'phantomjs', nargs = 1)
main_grp.add_option('--workers',default = 2, nargs = 1)
main_grp.add_option('--verbosity',action = 'count', default = 2)

proc_grp = OptionGroup(parser, 'Input processing parameters')
proc_grp.add_option('-p', '--port', help = '<PORT> (optional): use the specified port for each target in the input list. Ex: -p 80', nargs = 1)
proc_grp.add_option('-s', '--ssl', help = '<SSL> (optional): enforce ssl for every connection', action = 'store_true', default = False)
proc_grp.add_option('-m', '--multiprotocol', help = '<MULTIPROTOCOL> (optional): perform screenshots over HTTP and HTTPS for each target', action = 'store_true', default = False) 

http_grp = OptionGroup(parser, 'HTTP parameters')
http_grp.add_option('-c', '--cookie', help = '<COOKIE_STRING> (optional): cookie string to add. Ex: -c "JSESSIONID=1234; YOLO=SWAG"', nargs = 1)
http_grp.add_option('-a', '--header', help = 'Ex: -a "Host: localhost" -a "Foo: bar"', action = 'append')

http_grp.add_option('-u', '--http-username', help = '<HTTP_USERNAME> (optional): specify a username for HTTP Basic Authentication.')
http_grp.add_option('-b', '--http-password', help = '<HTTP_PASSWORD> (optional): specify a password for HTTP Basic Authentication.')

conn_grp = OptionGroup(parser, 'Connection parameters')
conn_grp.add_option('-P', '--proxy', help = '<PROXY> (optional): specify a proxy. Ex: -P http://proxy.company.com:8080')
conn_grp.add_option('-A', '--proxy-auth', help = '<PROXY_AUTH> (optional): provides authentication information for the proxy. Ex: -A user:password')
conn_grp.add_option('-T', '--proxy-type', default = 'http')
conn_grp.add_option('-t', '--timeout', default = 60, nargs = 1)

parser.option_groups.extend([main_grp, proc_grp, http_grp, conn_grp])

#parser.add_option('--header',default = '"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"',action = 'append')
# renderer binaries, hoping to find it in a $PATH directory
## Be free to change them to your own full-path location 
PHANTOMJS_BIN = 'phantomjs'
WEBSCREENSHOT_JS = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), './fetch.js'))
SCREENSHOTS_DIRECTORY = os.path.abspath(os.path.join(os.getcwdu(), './screenshots/'))

# Logger definition
LOGLEVELS = {0 : 'ERROR', 1 : 'INFO', 2 : 'DEBUG'}
logger_output = logging.StreamHandler(sys.stdout)
logger_output.setFormatter(logging.Formatter('[%(levelname)s][%(name)s] %(message)s'))

logger_gen = logging.getLogger("General")
logger_gen.addHandler(logger_output)

# Macros
SHELL_EXECUTION_OK = 0
SHELL_EXECUTION_ERROR = -1
PHANTOMJS_HTTP_AUTH_ERROR_CODE = 2

# Handful patterns
p_ipv4_elementary = '(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})'
p_domain = '[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,6}'
p_port = '\d{0,5}'
p_resource = '(?:/(?P<res>.*))?'

full_uri_domain = re.compile('^(?P<protocol>http(?:|s))://(?P<host>%s|%s)(?::(?P<port>%s))?%s$' % (p_domain, p_ipv4_elementary, p_port, p_resource))

fqdn_and_port = re.compile('^(?P<host>%s):(?P<port>%s)%s$' % (p_domain, p_port, p_resource))
fqdn_only = re.compile('^(?P<host>%s)%s$' % (p_domain, p_resource))

ipv4_and_port = re.compile('^(?P<host>%s):(?P<port>%s)%s' % (p_ipv4_elementary, p_port, p_resource))
ipv4_only = re.compile('^(?P<host>%s)%s$' % (p_ipv4_elementary, p_resource))

entry_from_csv = re.compile('^(?P<host>%s|%s)\s+(?P<port>\d+)$' % (p_domain, p_ipv4_elementary))

# Handful functions
def init_worker():
    """ 
        Tell the workers to ignore a global SIGINT interruption
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
def kill_em_all(signal, frame):
    """
        Terminate all processes while capturing a SIGINT from the user
    """
    logger_gen.info('CTRL-C received, exiting')
    sys.exit(0)
    
def shell_exec(url, command, options):
    """
        Execute a shell command following a timeout
        Taken from http://howto.pui.ch/post/37471155682/set-timeout-for-a-shell-command-in-python
    """
    global SHELL_EXECUTION_OK, SHELL_EXECUTION_ERROR
    
    logger_url = logging.getLogger("%s" % url)
    logger_url.setLevel(options.log_level)
    
    timeout = int(options.timeout)
    start = datetime.datetime.now()
    
    try :
        p = subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # binaries timeout
        while p.poll() is None:
            time.sleep(1)
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                logger_url.debug("Shell command PID %s reached the timeout, killing it now" % p.pid)
                logger_url.error("Screenshot somehow failed\n")
                
                if sys.platform == 'win32':
                    p.send_signal(signal.SIGTERM)
                else:
                    p.send_signal(signal.SIGKILL)
                
                return SHELL_EXECUTION_ERROR
        
        retval = p.poll()
        if retval != SHELL_EXECUTION_OK:
            if retval == PHANTOMJS_HTTP_AUTH_ERROR_CODE:
                # HTTP Authentication request
                logger_url.error("HTTP Authentication requested, try to pass credentials with -u and -b options")
            else:
                # Phantomjs general error
                logger_url.error("Shell command PID %s returned an abnormal error code: '%s'" % (p.pid,retval))
                logger_url.error("Screenshot somehow failed\n")
                    
            return SHELL_EXECUTION_ERROR
        
        else:
            # Phantomjs ok
            logger_url.debug("Shell command PID %s ended normally" % p.pid)
            logger_url.info("Screenshot OK\n")
            return SHELL_EXECUTION_OK
    
    except Exception as e:
        if e.errno and e.errno == errno.ENOENT :
            logger_url.error('renderer binary could not have been found in your current PATH environment variable, exiting')
        else:
            logger_gen.error('Unknown error: %s, exiting' % e )
        return SHELL_EXECUTION_ERROR

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('http://', '').replace('https://', '')
    
    return re.sub('[^\w\-_\. ]', '_', filename).replace('_443', '').replace('_80', '')

def extract_all_matched_named_groups(regex, match):
    """
        Return a set of all extractable matched parameters.
        >>> full_uri_domain.groupindex
        {'domain': 1, 'port': 3}
        >>>full_uri_domain.match('http://8.8.8.8:80').group('domain')
        '8.8.8.8'
        >>>extract_all_matched_named_groups() => {'domain': '8.8.8.8', 'port': '80'}
            
    """
    result = {}
    for name, id in regex.groupindex.items():
        matched_value = match.group(name)
        if matched_value != None: result[name] = matched_value
    
    return result
    
def entry_format_validator(line):
    """
        Validate the current line against several regexes and return matched parameters (ip, domain, port etc.)
    """
    tab = { 'full_uri_domain'       : full_uri_domain,
            'fqdn_only'             : fqdn_only,
            'fqdn_and_port'         : fqdn_and_port, 
            'ipv4_and_port'         : ipv4_and_port, 
            'ipv4_only'             : ipv4_only, 
            'entry_from_csv'        : entry_from_csv
    }
    
    for name, regex in tab.items():
        validator = regex.match(line)
        if validator:
            return extract_all_matched_named_groups(regex, validator)

def parse_targets(options, arguments):
    """
        Parse list and convert each target to valid URI with port(protocol://foobar:port) 
    """
    
    target_list = []
    
    if options.input_file != None:    
        with open(options.input_file,'rb') as fd_input:
            try:
                lines = [l.decode('utf-8').lstrip().rstrip().strip() for l in fd_input.readlines()]
            except UnicodeDecodeError as e:
                logger_gen.error('Your input file is not UTF-8 encoded, please encode it before using this script')
                sys.exit(0)
    else:
        lines = arguments
        
    for index, line in enumerate(lines, start=1):
        matches = entry_format_validator(line)
        
        # pass if line can be recognized as a correct input, or if no 'host' group could be found with all the regexes
        if matches == None or not('host' in matches.keys()):
            logger_gen.warn("Line %s '%s' could not have been recognized as a correct input" % (index, line))
            pass
        else:
            host = matches['host']
            
            # Protocol is 'http' by default, unless ssl is forced
            if options.ssl == True:
                protocol = 'https'
            elif 'protocol' in matches.keys():
                protocol = str(matches['protocol'])
            else:
                protocol = 'http'
            
            # Port is ('80' for http) or ('443' for https) by default, unless a specific port is supplied
            if options.port != None:
                port = options.port
            elif 'port' in matches.keys():
                port = int(matches['port'])
                
                # if port is 443, assume protocol is https if is not specified
                protocol = 'https' if port == 443 else protocol
            else:
                port = 443 if protocol == 'https' else 80
            
            # No resource URI by default
            if 'res' in matches.keys():
                res = str(matches['res'])
            else:
                res = None
            
            # perform screenshots over HTTP and HTTPS for each target
            if options.multiprotocol:
                final_uri_http_port = int(matches['port']) if 'port' in matches.keys() else 80
                final_uri_http = '%s://%s:%s' % ('http', host, final_uri_http_port)
                target_list.append(final_uri_http)
                logger_gen.info("'%s' has been formatted as '%s' with supplied overriding options" % (line, final_uri_http))
                
                
                final_uri_https_port = int(matches['port']) if 'port' in matches.keys() else 443
                final_uri_https = '%s://%s:%s' % ('https', host, final_uri_https_port)
                target_list.append(final_uri_https)
                logger_gen.info("'%s' has been formatted as '%s' with supplied overriding options" % (line, final_uri_https))
            
            else:
                final_uri = '%s://%s:%s' % (protocol, host, port)
                final_uri = final_uri + '/%s' % res if res != None else final_uri
                target_list.append(final_uri)

                logger_gen.info("'%s' has been formatted as '%s' with supplied overriding options" % (line, final_uri))
    
    return target_list      

def craft_cmd(url_and_options):
    """
        Craft the correct command with url and options
    """
    global logger_output, PHANTOMJS_BIN, WEBSCREENSHOT_JS, SCREENSHOTS_DIRECTORY, SHELL_EXECUTION_OK, SHELL_EXECUTION_ERROR
    
    url, options = url_and_options
    
    logger_url = logging.getLogger("%s" % url)
    logger_url.addHandler(logger_output)
    logger_url.setLevel(options.log_level)

    output_filename = os.path.join(SCREENSHOTS_DIRECTORY, ('%s.png' % filter_bad_filename_chars(url)))
    
    options.proxy = random.choice(list(open('ivan.txt').read().splitlines())).split(':Ivan')[0]
    #options.header ="User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'"
    options.proxy_auth = 'Ivan:tempuvefy'
    #options.proxy_type = 'http'
    cmd_parameters = [PHANTOMJS_BIN,'--ignore-ssl-errors true','--ssl-protocol any','--ssl-ciphers ALL']
    
    cmd_parameters.append("--proxy %s" % options.proxy) if options.proxy != None else None
    cmd_parameters.append("--proxy-auth %s" % options.proxy_auth) if options.proxy_auth != None else None
    cmd_parameters.append("--proxy-type %s" % options.proxy_type) if options.proxy_type != None else None

    cmd_parameters.append('"%s" url_capture="%s" output_file="%s"' % (WEBSCREENSHOT_JS, url, output_filename))
    
    cmd_parameters.append('header="Cookie: %s"' % options.cookie.rstrip(';')) if options.cookie != None else None
    
    cmd_parameters.append('http_username="%s"' % options.http_username) if options.http_username != None else None
    cmd_parameters.append('http_password="%s"' % options.http_password) if options.http_password != None else None
  
    if options.header:
        for header in options.header:
            cmd_parameters.append('header="%s"' % header.rstrip(';'))

    
    cmd = " ".join(cmd_parameters)
    
    logger_url.debug("Shell command to be executed\n'%s'\n" % cmd)
    
    execution_retval = shell_exec(url, cmd, options)
    
    return execution_retval, url

    
def take_screenshot(url_list, options):
    """
        Launch the screenshot workers
        Thanks http://noswap.com/blog/python-multiprocessing-keyboardinterrupt
    """
    global SHELL_EXECUTION_OK, SHELL_EXECUTION_ERROR
    
    screenshot_number = len(url_list)
    print "[+] %s URLs to be screenshot" % screenshot_number
    
    pool = multiprocessing.Pool(processes=int(options.workers), initializer=init_worker)
    
    taken_screenshots = [r for r in pool.imap(func=craft_cmd, iterable=itertools.izip(url_list, itertools.repeat(options)))]

    screenshots_error_url = [url for retval, url in taken_screenshots if retval == SHELL_EXECUTION_ERROR]
    screenshots_error = sum(retval == SHELL_EXECUTION_ERROR for retval, url in taken_screenshots)
    screenshots_ok = int(screenshot_number - screenshots_error)
    
    print "[+] %s actual URLs screenshot" % screenshots_ok
    print "[+] %s error(s)" % screenshots_error
    
    while len(screenshots_error_url) > 0 :
        print "[++++++++++++++++++++++++] %s URLs to be screenshot again!!" % len(screenshots_error_url),'[++++++++++++++++++++++++++++++++++++++++++++]'
        taken_screenshots = [r for r in pool.imap(func=craft_cmd, iterable=itertools.izip(screenshots_error_url, itertools.repeat(options)))]
        screenshots_error_url = [url for retval, url in taken_screenshots if retval == SHELL_EXECUTION_ERROR]
            
    print 'Done!!!'
    
def main():
    """
        Dat main
    """
    global VERSION, SCREENSHOTS_DIRECTORY, LOGLEVELS
    signal.signal(signal.SIGINT, kill_em_all)
    
    
    
    
    #parser.add_option('--input-file',default = 'gde.txt', nargs = 1) 
    
    options, arguments = parser.parse_args()
    
   
    
    try :
        options.log_level = LOGLEVELS[options.verbosity]
        logger_gen.setLevel(options.log_level)
    except :
        parser.error("Please specify a valid log level")
        
    if (options.input_file == None and (len(arguments) > 1 or len(arguments) == 0)):
        parser.error('Please specify a valid input file or a valid URL')
    
    if (options.input_file != None and len(arguments) == 1):
        parser.error('Please specify either an input file or an URL')
    
    if (options.output_directory != None):
        SCREENSHOTS_DIRECTORY = os.path.abspath(os.path.join(os.getcwdu(), options.output_directory))
    
    logger_gen.debug("Options: %s\n" % options)
    if not os.path.exists(SCREENSHOTS_DIRECTORY):
        logger_gen.info("'%s' does not exist, will then be created" % SCREENSHOTS_DIRECTORY)
        os.makedirs(SCREENSHOTS_DIRECTORY)
        
    url_list = parse_targets(options, arguments)
    print url_list
    take_screenshot(url_list, options)
    
    return None

if __name__ == "__main__" :
    main()