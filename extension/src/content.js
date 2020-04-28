// stuff that runs once the webpage loads
// https://www.youtube.com/watch?v=ew9ut7ixIlI

console.log('listener added');

chrome.runtime.onMessage.addListener(gotMessage);
async function gotMessage(message, sender, sendResponse) {
    let { model_result } = message;
    let { pred_class, probability } = model_result;
}