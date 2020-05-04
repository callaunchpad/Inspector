// if we wanna make this automatic after clicking icon, put javascript here for automatic processing
// https://www.youtube.com/watch?v=ew9ut7ixIlI
console.log("backgroud running");

import Mercury from '@postlight/mercury-parser';
import inference from './posts.js'

// load the json of sources first
async function loadSources() {
    let res = await fetch("./sources.json");
    let json = await res.json();
    return json;
}
// global sources dictionary so don't have to keep loading it every time
var sources = null;

chrome.browserAction.onClicked.addListener(async (tab) => {
    // load json sources array globally if not null
    if (sources === null) {
        sources = await loadSources();
    }
    console.log(sources);

    // remove "default_popup": "popup.html" from manifest for this to work
    // tab param has info about the tab you're on

    chrome.tabs.query({active: true, lastFocusedWindow: true}, async (tabs) => {
        // send a message to trigger an alert via content.js
        chrome.tabs.sendMessage(tabs[0].id, null);

        let url = tabs[0].url;
        console.log("url: ", url);

        // get webpage information with the Mercury package
        let webpage_info = await Mercury.parse(url);
        
        let source_type = checkSources(url, sources);
        console.log("type: ", source_type);
        if (source_type != null) {
            // found the webpage is list of sources
            if (source_type === "trusted") {
                console.log("this is a trusted source!");
            } else {
                console.log("this is sketchy source: ", source_type);
            }
            return;
        }
        // remove html tags with regex
        let article_body = webpage_info.content.replace( /(<([^>]+)>)/ig, '');
        let article_title = webpage_info.title;
        console.log("title: ", article_title);
        console.log("body: ", article_body);

        console.log("sending request...")
        let model_result = await inference(article_title, article_body);

        let { cnn_probability, cnn_class, 
            article1_class, article1_link, 
            article2_class, article2_link, 
            article3_class, article3_link, 
            article4_class, article4_link } = model_result;

        chrome.windows.create({url: "display.html?data=" + encodeURIComponent(JSON.stringify({
            p_class: cnn_class, 
            p_score: cnn_probability, 
            a1_class: article1_class,
            a1_link: article1_link,
            a2_class: article2_class,
            a2_link: article2_link,
            a3_class: article3_class,
            a3_link: article3_link,
            a4_class: article4_class,
            a4_link: article4_link
        })), type: "popup", height: 580, width: 500});
    });
});

// checks to see if the webpage url is on our list of 
// trusted/sketch sources. Returns source type as a string if it is,
// otherwise it returns null.
function checkSources(url, sources) {
    let hostName = getHostName(url);
    if (sources[hostName] != null) {
        return sources[hostName].type;
    }
    return null;
}

// extracts just the hostname of a url using regex
function getHostName(url) {
    let hostname = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    console.log("hostname: ", hostname);
    if (hostname != null && hostname.length > 2 && typeof hostname[2] === 'string' && hostname[2].length > 0) {
        console.log("hostname: ", hostname[2]);
        return hostname[2];
    }
    else {
        return null;
    }
}