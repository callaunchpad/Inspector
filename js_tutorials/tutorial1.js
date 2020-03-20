// This is a short assignment on making GET requests to a server, getting the response data,
// parsing it, and sending a POST request back to the server with new data. These 
// requests follow the HTTP protocol, so they must have headers. POST requests
// normally have a body that follows the json format, but GET requests can't have a body.
// All responses will have a response body in the json format.

// Here's a link to how HTTP requests are structured: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages

// endpoint url of the mock server
MOCK_SERVER_ENDPOINT = 'https://eab77041-8340-40d6-bfde-248332bc5286.mock.pstmn.io' 

// endpoint to get the members in our team
MEMBER_ENDPOINT = `${MOCK_SERVER_ENDPOINT}/getMembers`;

// endpoint to get the last names of members in our team
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
// returns an Array of json-formatted response bodies
function getNamesPromises() {
    return Promise.all([
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
        // since we are using Promise.all, we get a 2-element array with the responses in it
        return Promise.all([response[0].json(), response[1].json()]);
    }).then((jsons) => {
        // console.log(jsons[0], jsons[1]);
        return jsons;
    }).catch(e => console.error(e));
}

// Use the async/await syntax with fetch to make a request to the mock server.
// The fetches must be run IN PARALLEL, not one after another!
// You should always surround await ... in try/catch blocks in case the 
// request fails to go through, which occurs pretty often in the real world
// returns an Array of json-formatted response bodies
async function getNames() {
    try {
        let [mem_res, name_res] = await Promise.all([
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
        ]);
        let [mem_json, name_json] = await Promise.all([
            mem_res.json(),
            name_res.json()
        ]);
        // console.log(mem_json);
        // console.log(name_json);
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
    try {
        var info = await getNamesPromises(); // notice how we're using var instead of let here, cuz var is function scoped
        console.log(info)
    } catch(e) {
        console.error(e)
    };
    member_json = info[0];
    info_json = info[1];

    let response_body = {};
    // iterate through the members, and match their first names with their last names
    // for each loops are slightly different in javascript!
    console.log(member_json);
    console.log(info_json);
    member_json.members.forEach((fname, idx) => {
        response_body[fname] = info_json[fname].lastName
    });
    // does this look right?
    console.log(response_body);

    // make a fetch POST request with Promise or async/await syntax
    let response = await fetch(SEND_NAMES_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': API_KEY
        },
        body: JSON.stringify(response_body)
    });
    let response_json = await response.json();
    
    // lmk what the secret is so ik you finished!
    console.log(response_json.secret)
}
// send the first and last names of our team members to the server with
// the sendNames function. It should use one of the getNames functions to do so.
sendNames()