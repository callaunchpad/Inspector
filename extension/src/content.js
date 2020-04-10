// stuff that runs once the webpage loads
// https://www.youtube.com/watch?v=ew9ut7ixIlI

var SEND_REQUEST = "send request"
console.log('listener added');
import Mercury from '@postlight/mercury-parser';
import fetch from 'node-fetch';
chrome.runtime.onMessage.addListener(gotMessage);
async function gotMessage(message, sender, sendResponse) {
    // do some stuff once the 
    console.log(message, sender)
    if (message.msg === SEND_REQUEST) {
        // why do they still use callbacks kill me
        let url = message.url;
        console.log("url: ", url);

        // get webpage information with the Mercury package
        var webpage_info = await Mercury.parse(url);

        // remove html tags with regex
        let article_body = webpage_info.content.replace( /(<([^>]+)>)/ig, '');
        let article_title = webpage_info.title;
        console.log("title: ", article_title);
        console.log("body: ", article_body);
    }
}