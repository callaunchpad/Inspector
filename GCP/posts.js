SERVER_ENDPOINT = 'https://us-central1-inspector-project.cloudfunctions.net/handler';

const fetch = require("node-fetch");

let result = await fetch(SERVER_ENDPOINT, {
    method: 'POST',
    headers: {
            'Content-Type': 'application/json',            
    },
    body: JSON.stringify(response_body)
});

result = await result.json()
console.log(result)