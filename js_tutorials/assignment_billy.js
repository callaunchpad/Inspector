// This is a short assignment on making GET requests to a server, getting the response data,
// parsing it, and sending a POST request back to the server with new data. These 
// requests follow the HTTP protocol, so they must have headers. POST requests
// normally have a body that follows the json format, but GET requests can't have a body.
// All responses will have a response body in the json format.

// Here's a link to how HTTP requests are structured: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages

// BEFORE YOU START:
// 1) Make sure you have Node.js installed: https://nodejs.org/en/download/
// 2) run npm install in the js_tutorials folder

// GOAL:
// complete the sendNames function so that:
// 1) it gets an array of our team names from the server
// 2) it gets a json with a bunch of info on each member in our team
// 3) it gets the first name and last name of each member with the data from 1 and 2 (or just 2) and
// sends that info back to the server with a POST request.
// getNames and getNames promise are utility functions that should complete steps 1 and 2.

// endpoint url of the mock server 
MOCK_SERVER_ENDPOINT = 'https://eab77041-8340-40d6-bfde-248332bc5286.mock.pstmn.io';

// endpoint to get the members in our team
MEMBER_ENDPOINT = `${MOCK_SERVER_ENDPOINT}/getMembers`;

// endpoint to get the info of the members in our team
INFO_ENDPOINT = `${MOCK_SERVER_ENDPOINT}/getLastNames`;

SEND_NAMES_ENDPOINT = `${MOCK_SERVER_ENDPOINT}/sendNames`;

// API KEY that we must include in order to have permission to use the API of the mock server.
// For most web APIs, we need to provide API keys that are generated after signing up to use
// the web API in our request headers. I've gone ahead and done that step already and pasted the key here.
API_KEY = 'PMAK-5e6b30d9d696e70038c23500-ce4bc94c3fbe460ace19fa6c2d94ebf64a';

// function called fetch that let's us send HTTP requests
// check out the doc here: 
const fetch = require("node-fetch");

// Use the promises syntax with .then and .catch and fetch to make a request to the mock server.
// The fetches must be run IN PARALLEL, not one after another!
// returns a PROMISE for an Array of json-formatted response bodies
function getNamesPromises() {
    // a fetch request follows a format like this:
    // fetch(endpoint, {
    //     method: 'GET/POST/PUT/DELETE/etc...',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'x-api-key': API_KEY
    //          ... more header fields...
    //     }
    //     body: JSON.stringify({...}) // ONLY IF IT IS A POST REQUEST, we include a body in the json format, and stringify it 
    // }) 

    // TODO: what should go in the Promise.all array?
    // Promise.all: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all
    let gotNames = Promise.all([
        fetch(MEMBER_ENDPOINT, {
            method: 'GET',
            headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': API_KEY
            }
        }),
        fetch(INFO_ENDPOINT, {
            method: 'GET',
            headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': API_KEY
            }
        })
    ]).then((response) => {
        let resp1_json = response[0].json();
        let resp2_json = response[1].json();
        return Promise.all([resp1_json, resp2_json]);
    }).then((jsons) => {
        // might be a good idea to take a look at what these response jsons look like
        console.log(jsons)

        return jsons;
    }).catch(e => console.error(e));
    return gotNames;
}

// Use the async/await syntax with fetch to make a request to the mock server.
// The fetches must be run IN PARALLEL, not one after another!
// You should always surround await ... in try/catch blocks in case the 
// request fails to go through, which occurs pretty often in the real world
// returns an Array of json-formatted response bodies WHEN AWAITED
async function getNames() {
    try {
        // TODO
        let [mem_res, name_res] = await Promise.all[
            fetch(MEMBER_ENDPOINT, {
                method: 'GET',
                headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': API_KEY
                }
            }),
            fetch(INFO_ENDPOINT, {
                method: 'GET',
                headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': API_KEY
                }
            })];
        let [mem_json, name_json] = await Promise.all[mem_res.json(), name_res.json()];
        // might be a good idea to take a look at what these response jsons look like
        console.log(mem_json, name_json)
        return [mem_json, name_json];
    } catch(e) {
        console.error(e)
    };
}

// sends the first and last names of the inspector members to the SEND_NAMES endpoint
// Since this will use a POST request, we need to define a request body in addition to
// headers and a method.

// the POST body should be of this json format:
// { first name: last name, } i.e { Billy: Wang, David: Shau}
async function sendNames() {
    // get the json that contains the array of team member first names, and the json
    // that contains a key-value format of our first names followed by a json of information
    let x = await getNamesPromises();
    // console.log(x);

    let member_json = x[0];
    let info_json = x[1];

    let response_body = {};
    // iterate through the members, and match their first names with their last names
    // for each loops are slightly different in javascript!
    member_json.members.forEach((fname, idx) => {
        // TODO!

        response_body[fname] = idx;
    });
    // does this look right?
    console.log(response_body);

    // TODO: make a fetch POST request with Promise or async/await syntax
    let secret = await fetch(SEND_NAMES_ENDPOINT, {
        method: 'POST',
        headers: {
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
        },
        body: JSON.stringify({response_body})
    });
    // once you get the response body after sending the POST request, 
    // console log the "secret" field of it and lmk what the text is so ik you finished!
    console.log(secret)
}
// send the first and last names of our team members to the server with
// the sendNames function. It should use one of the getNames functions to do so.
sendNames()