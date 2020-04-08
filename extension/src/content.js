// stuff that runs once the webpage loads
// https://www.youtube.com/watch?v=ew9ut7ixIlI

import Mercury from '@postlight/mercury-parser';
var SEND_REQUEST = "send request"
console.log('listener added');
chrome.runtime.onMessage.addListener(gotMessage);
function gotMessage(message, sender, sendResponse) {
    // do some stuff once the 
    console.log(message, sender)
    if (message.msg === SEND_REQUEST) {
        // do some code based on what the message sent was
        alert("Mercury parsing...");
        Mercury.parse(url).then(result => console.log(result));
    }
}