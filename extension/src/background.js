// if we wanna make this automatic after clicking icon, put javascript here for automatic processing
// https://www.youtube.com/watch?v=ew9ut7ixIlI
console.log("backgroud running");

import Mercury from '@postlight/mercury-parser';
import inference from './posts.js'


chrome.browserAction.onClicked.addListener(async (tab) => {
    // remove "default_popup": "popup.html" from manifest for this to work
    console.log("sending request...")
    // tab param has info about the tab you're on

    // sending message to content.js for it to handle stuff
    chrome.tabs.query({active: true, lastFocusedWindow: true}, async (tabs) => {
        // why do they still use callbacks kill me
        let url = tabs[0].url;
        console.log("url: ", url);

        // get webpage information with the Mercury package
        let [webpageInfo, sourceType] = await Promise.all([Mercury.parse(url), checkSources(url)]);
        
        // var webpage_info = await Mercury.parse(url);

        // remove html tags with regex
        let articleBody = webpageInfo.content.replace( /(<([^>]+)>)/ig, '');
        let articleTitle = webpageInfo.title;
        console.log("title: ", articleTitle);
        console.log("body: ", articleBody);

        let modelResult = await inference(articleTitle, articleBody);
        let message = { modelResult };
        
        chrome.tabs.sendMessage(tab.id, message);
    });
});

// checks to see if the webpage url is on our list of 
// trusted/sketch sources. Returns source type as a string if it is,
// otherwise it returns null.
async function checkSources(url) {
    let res = await fetch("./sources.json");
    let sources = res.json();
    let hostName = getHostName(url);
    if (sources[hostName] != null) {
        return sources[hostName].type;
    }
    return null;
}

// extracts just the hostname of a url using regex
function getHostName(url) {
    var match = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    if (match != null && match.length > 2 && typeof match[2] === 'string' && match[2].length > 0) {
        console.log("hostname: ", match[2]);
        return match[2];
    }
    else {
        return null;
    }
}