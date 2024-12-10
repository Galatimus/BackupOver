var system = require('system'),
    page = require("webpage").create();
	//page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0';
// Workaround for https://github.com/ariya/phantomjs/issues/12697 since
// it doesn't seem like there will be another 1.9.x release fixing this
var phantomExit = function(exitCode) {
    page.close();
    setTimeout(function() { phantom.exit(exitCode); }, 100);
};
if( system.args.length !== 2 ) {system.stderr.writeLine("Usage: fetch.js URL");phantomExit(1);}

var resourceWait  = 3000,
    maxRenderWait = 10000,
    url           = system.args[1],
    count         = 0,
	forcedRenderTimeout,
    renderTimeout;
var doRender = function() {
    var c = page.evaluate(function() {
        return document.documentElement.outerHTML;
    });
    system.stdout.write(c);
    phantomExit();
}
page.onResourceRequested = function (req) {
    count += 1;
    //system.stderr.writeLine('>>>>>> ' + req.id + ' - ' + req.url);
    clearTimeout(renderTimeout);
};
page.onResourceReceived = function (res) {
    if (!res.stage || res.stage === 'end') {
        count -= 1;
        //system.stderr.writeLine(res.id + ' ' + res.status + ' - ' + res.url);
        if (count === 0) {
            renderTimeout = setTimeout(doRender, resourceWait);
        }
    }
};
page.open(url, function (status) {
    if (status !== "success") {
        system.stderr.writeLine('Unable to load url');
        phantomExit(1);
    } else {
        forcedRenderTimeout = setTimeout(function () {
            console.log(count);
            doRender();
        }, maxRenderWait);
    }
});