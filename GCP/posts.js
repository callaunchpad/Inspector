async function main(){
    SERVER_ENDPOINT = 'https://us-central1-inspector-project.cloudfunctions.net/fuck_gcp';

    const fetch = require("node-fetch");

    var request_body = {'title': 'Jobless Claims Surpass 16 Million; Aid Package Stalls in Senate',
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