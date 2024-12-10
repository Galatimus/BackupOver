#!/usr/bin/python
# -*- coding: utf-8 -*-




from xhtml2pdf import pisa             # import python module
from grab import Grab
import logging
from grab.error import GrabTimeoutError, GrabNetworkError,DataNotFound,GrabConnectionError
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG)

g = Grab(timeout=20, connect_timeout=50)
g.proxylist.load_file(path='../tipa.txt',proxy_type='http')

my_link = 'https://ffpmif.com/marketing'

g.go(my_link)
html_string = g.doc.body

# Define your data
sourceHtml = html_string
outputFilename = "test.pdf"

# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)    