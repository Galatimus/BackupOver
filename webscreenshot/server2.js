"use strict";
var port,
    server,
    service,
    system = require('system'),
    page,
    address,
    output,
    width;
 
 
if (system.args.length !== 2) {
 
    console.log('Usage: server.js <portnumber>');
    phantom.exit(1);
 
} else {
    port = system.args[1];
    server = require('webserver').create();
 
    service = server.listen(port, function (request, response) {
 
        // logging, comment out if you dont want any
        console.log('Request at ' + new Date());
        console.log(JSON.stringify(request, null, 4));
 
        //url request comes in like this - url encoded url after the 8001/
        //curl http://127.0.0.1:8001/URL_ENCODED_URL_HERE;
        //curl http://127.0.0.1:8001/http%3A%2F%2Fbitbook.io/;
 
        //remove 1st slash on url
        var url = request.url.substring(1, request.url.length);
 
        page = require('webpage').create();
        page.viewportSize = {width: 1200, height: 900};//max ever canvas
        page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
 
        page.open(url, function (status) {
 
            if (status !== 'success') {
 
                page.close();
                response.statusCode = 500;
                response.write('error: url no load');
                response.close();
                console.log('Unable to load the address');
 
            } else {
//              removed timeout
//              window.setTimeout(function () {
                    // phantomjs doesnt set a background if page has none, so force it if none
                    page.evaluate(function() {
                        var style = document.createElement('style'),
                            text = document.createTextNode('body { background: #fff }');
                        style.setAttribute('type', 'text/css');
                        style.appendChild(text);
                        document.head.insertBefore(style, document.head.firstChild);
                    });
 
                    var base64 = page.renderBase64('PNG');
 
                    response.statusCode = 200;
                    response.setHeader("Content-Type", "image/png");
                    response.setEncoding('binary');
                    response.write(atob(base64));
                    response.close();
 
//              }, 21500);
 
            }
        });
 
    });
 
 
    if (service) {
        console.log('Web server running on port ' + port);
    } else {
        console.log('Error: Could not create web server listening on port ' + port);
        phantom.exit();
    }
 
 
}