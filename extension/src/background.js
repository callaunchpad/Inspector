// if we wanna make this automatic after clicking icon, put javascript here for automatic processing
// https://www.youtube.com/watch?v=ew9ut7ixIlI
var SEND_REQUEST = "send request"

console.log("backgroud running");

chrome.browserAction.onClicked.addListener((tab) => {
    // remove "default_popup": "popup.html" from manifest for this to work
    console.log("sending request...")
    // tab param has info about the tab you're on

    // sending message to content.js for it to handle stuff
    chrome.tabs.query({active: true, lastFocusedWindow: true}, (tabs) => {
        let message = {
            msg: SEND_REQUEST,
            url: tabs[0].url
        }
        chrome.tabs.sendMessage(tab.id, message)
    });
});

console.log("added listener")
