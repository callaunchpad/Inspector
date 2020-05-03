async function main(){
    SERVER_ENDPOINT = 'https://us-central1-inspector-project.cloudfunctions.net/fuck_gcp';

    const fetch = require("node-fetch");

    var request_body = {'title': 'Coronavirus Live Updates: As Economy Hemorrhages Jobs, Europeans Agree to Prime E.U.’s Pump - The New York Times',
                    'body': 'I hate monkeys. I just want cookies.'};

    let result = await fetch(SERVER_ENDPOINT, {
        method: 'POST',
        headers: {
                'Content-Type': 'application/json',            
        },
        body: JSON.stringify(request_body)
    });

    result = await result.json();
    console.log(result);
}
main();