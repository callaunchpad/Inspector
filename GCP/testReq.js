const fetch = require("node-fetch");
endpoint_handler = 'https://us-central1-inspector-experiments.cloudfunctions.net/handler'
endpoint_hello = 'https://us-central1-inspector-experiments.cloudfunctions.net/hello_get'
review = "this film was just brilliant casting location scenery story direction everyone's really suited the part they played and you could just imagine being there robert # is an amazing actor and now the same being director # father came from the same scottish island as myself so i loved the fact there was a real connection with this film the witty remarks throughout the film were great it was just brilliant so much that i bought the film as soon as it was released for # and would recommend it to everyone to watch and the fly fishing was amazing really cried at the end it was so sad and you know what they say if you cry at a film it must have been good and this definitely was also # to the two little boy's that played the # of norman and paul they were just brilliant children are often left out of the # list i think because the stars that play them all grown up are such a big profile for the whole film but these children are amazing and should be praised for what they have done don't you think the whole story was so lovely because it was true and was someone's life after all that was shared with us all"

async function makeReq() {
    var reqBody = {
        text: review
    }
    try {
        var res = await fetch(endpoint_handler, {
            method: 'POST',
            body: JSON.stringify(reqBody),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        console.log(res)
        var json = await res.json()
        console.log(json)
    } catch(e) {
        console.error(e)
    }
}
makeReq()