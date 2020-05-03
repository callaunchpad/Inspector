// if we wanna make this automatic after clicking icon, put javascript here for automatic processing
// https://www.youtube.com/watch?v=ew9ut7ixIlI
var SEND_REQUEST = "send request"
let SERVER_ENDPOINT = 'https://us-central1-inspector-project.cloudfunctions.net/handler';
var request_body = {'title': 'Coronavirus Live Updates: As Economy Hemorrhages Jobs, Europeans Agree to Prime E.U.’s Pump - The New York Times',
                'body': 'I hate monkeys. I just want cookies.'};
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
        var webpage_info = await Mercury.parse(url);

        // remove html tags with regex
        let article_body = webpage_info.content.replace( /(<([^>]+)>)/ig, '');
        let article_title = webpage_info.title;
        console.log("title: ", article_title);
        console.log("body: ", article_body);

        let model_result = await inference(article_title, article_body);
        let message = { model_result };
        // let dict = {
        //     "cnn_probability": "1234",
        //     "cnn_class": str(np.round(cnn_predictions[0][0])),
        //     "article1_class": str(lstm_predictions[0]),
        //     "article1_link": lstm_links[0],
        //     "article2_class": str(lstm_predictions[1]),
        //     "article2_link": lstm_links[1],
        //     "article3_class": str(lstm_predictions[2]),
        //     "article3_link": lstm_links[2],
        //     "article4_class": str(lstm_predictions[3]),
        //     "article4_link": lstm_links[3],
        // };

        //format results into URL
        let { pred_class, probability } = model_result;
        chrome.windows.create({url: "display.html?data=" + encodeURIComponent(JSON.stringify({p_class: pred_class, p_score: probability})), type: "popup", height: 400, width: 400});
        
        chrome.tabs.sendMessage(tab.id, message)
    });
});