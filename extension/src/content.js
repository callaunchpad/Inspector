// stuff that runs once the webpage loads
// https://www.youtube.com/watch?v=ew9ut7ixIlI

chrome.runtime.onMessage.addListener(gotMessage);
console.log('listener added');
function gotMessage(message, sender, sendResponse) {
    console.log('entered here');
    alert("Thanks for using inspector! Your program is running. Please wait for a window to pop up.");
}