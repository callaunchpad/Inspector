// import Mercury from '@postlight/mercury-parser';

$(document).ready(function() {
    var url = 'https://www.nytimes.com/2020/04/08/world/coronavirus-news.html'
    Mercury.parse(url).then(result => alert(result));
    var title = "";
    var body = "";
    var $firstButton = $(".first"),
    $secondButton = $(".second"),
    $input = $("input"),
    $name = $(".name"),
    $more = $(".more"),
    $yourname = $(".yourname"),
    $inspect = $(".inspect"),
    $ctr = $(".container");
  
    $firstButton.on("click", function(e){
        
        // get highlighted text
        chrome.tabs.executeScript( {
            code: "window.getSelection().toString();"
        }, function(selection) {
            alert(selection[0]);
        });

        $(this).delay(50).queue(function(){
            $ctr.addClass("center slider-two-active").removeClass("full slider-one-active");
        });
        e.preventDefault();
    });
    
    $secondButton.on("click", function(e){

        // get highlighted text
        if (window.getSelection) {
            body = window.getSelection().toString();
        } else if (document.selection && document.selection.type != "Control") {
            body = document.selection.createRange().text;
        }

        $(this).delay(50).queue(function(){
            $ctr.addClass("full slider-three-active").removeClass("center slider-two-active slider-one-active");
            $name = $name.val();
            if($name == "") {
                $yourname.html("Anonymous!");
            }
            else { $yourname.html($name+"!"); }
        });
        e.preventDefault();
    });

    $inspect.on("click", async function(e) {
        $inspect.html("Processing...")
        // run Billy and Zach's script
        $inspect.html("Done")
        alert(title);
        alert(body);
    })
})

