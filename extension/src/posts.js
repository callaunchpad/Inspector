export default async function inference(title, body) {
    let SERVER_ENDPOINT = 'https://us-central1-inspector-project.cloudfunctions.net/handler';
    // var request_body = {'title': 'Coronavirus Live Updates: As Economy Hemorrhages Jobs, Europeans Agree to Prime E.U.’s Pump - The New York Times',
    //                 'body': 'I hate monkeys. I just want cookies.'};
    var request_body = {
        title,
        body,
    }
    try {
        var result = await fetch(SERVER_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',            
            },
            body: JSON.stringify(request_body)
        });
    } catch(e) {
        console.error(e);
    }
    try {
        console.log(result)
        var json = await result.json();
        console.log(json);
    } catch(e) {
        console.error(e);
    }

    return json;
}
