// global variables
var titleText;
var bodyText;

function getTitle() {
    // Code here
    alert("highlight the title of the article and press the button again when done");
    chrome.tabs.executeScript({
        code: "window.getSelection().toString();"
    }, function(selection) {
        titleText = selection[0];
    });
}

function getBody() {
    alert("highlight the body text of the article and press the button again when done");
    chrome.tabs.executeScript({
        code: "window.getSelection().toString();"
    }, function(selection) {
        bodyText = selection[0];
    });
}

function sendRequest() {
    // Import Billy and Zach's code here
    if (!titleText || !bodyText) {
        alert("please highlight the article title and body text first");
    }
}

document.getElementById('button').addEventListener('click', sendRequest);
