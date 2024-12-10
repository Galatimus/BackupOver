// The URL to load.
var url = 'https://bcinform.moscow/arenda-ofisa/id1047402/';

// Start a PhantomJS "page" and point it to the desired URL.
var page = require('webpage').create();
page.open(url, function(status) {

    if (status === 'success') {

        // Run a function in the webpage's context and catch what it returns.
        var html = page.evaluate(function() {
            // Optionally, do some more page manipulation here.
            // ...

            // Return the HTML from the loaded and JS-manipulated page.
            // Note that a console.log() here in this context won't be visible (by default).
            return document.documentElement.outerHTML;
        });

        // Print the HTML to standard output.
        console.log(html);
    }

    // Make sure we quit PhantomJS, no point to keep waiting for nothing.
    phantom.exit();
});