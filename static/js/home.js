function SubmitEmailSignupToGoogleDoc(email,parentemail){
	console.log('hi');
	// Email signup newsletter subscription survey
	// email
	// parentemail
	$.ajax({
		url: "https://docs.google.com/forms/d/1KtJyHzzHHnXZC4pKtHYAkEPkZZ3kp0pIxg-xxfHEq50/formResponse",	 			
        data: {"entry.1031625911": email, "entry.396703220": parentemail},
        type: "POST",
        dataType: "xml",

        success: function(msg) {
            /* 		    $('#success').html('hi'+msg); */
        },
        error: function(msg) {
            /* 		    $('#success').html('bhi'+msg); */
        }

    });

}


function Start(){

}

testimonials = {
	"This game is epic!":"&mdash;Eric, grade 3",
	"This game is not just an animated multiplication table. Math is inherent in the game; you get the numbers and you decide what to do with them.":"&mdash;Christine, CSL Associates President",
	"For weeks I tried to explain fractions to my 6-year-old. After playing your game he got it right away!":"&mdash;Susan Prasher",
	"Ew, what's that a math game? .. looks cool .. Can I play?":"&mdash;Jose, grade 4",
	"My kids have been playing Mathbreakers non-stop... Who knew a kid would get up early to get their chores done to do more math?!":"&mdash;Cindy Handler, mother of 3",	
	"For 3 days he could not stop asking when he would get to play again. He said it was better than League of Legends! He wants to show it to his friends.":"&mdash;6th grade mom",
	"Good educational games are extremely rare... Mathbreakers has potential to be one of the great ones.": "&mdash;Edsurge",
	"Really motivates students to work through challenges, rather than avoid them.":"&mdash;Teacher from Palo Alto, California",
	"They are not afraid to make mistakes, so they get creative with their problem solving.":"&mdash;Teacher from Palo Alto, California",
	"It provided a freer and more fun experience than most kids are used to having inside of the classroom.":"&mdash;Teacher from Palo Alto, California",
	"A very effective tool in helping students overcome engagement issues and misconceptions about math.":"&mdash;Vice Principal from Peace River, Canada",
	"I was wrong, fractions are easy!":"&mdash;Alice, grade 6", 
	"It's a euphoric math experience!":"&mdash; Douglas, grade 6"
}
color = ["#0fe625","#ffde0c","#254dff","#ff2525"]
var getRandTestimonial = function() {
	seek = true;
	var quote = "";
	var author = "";
	while (seek){
		seek = false;
		var keys = Object.keys( testimonials );
		quote = keys[Math.floor(Math.random()*keys.length)];
		author = testimonials[quote]
		visibleCells = document.getElementsByClassName("visible");
		$('.visible').each(function(){
			if ($(this).find('.quote').text() == quote) {
				seek = true;
			}
		});
	}
	return [quote,author];
}

$(document).ready(function() {
	els = document.getElementsByClassName("cell2");
	for (var i=0; i<els.length; i++){
		FadeIn(i,i);
	}
	setInterval(function(){
		cells = document.getElementsByClassName("cell2");
		rand = Math.floor(Math.random() * cells.length);
		var keys = Object.keys( testimonials );
		FadeOut(rand);
    },6000)


	function FadeIn(rand){
		testimonial = getRandTestimonial();
		console.log("author: " +testimonial[1]);
		$('.cell2').eq(rand).find(".quote")
			.text(testimonial[0])
		$('.cell2').eq(rand).find(".author")
			.html(testimonial[1])
		$('.cell2').eq(rand).addClass("visible"); // = "cell2 visible";
		$('.cell2').eq(rand).find(".quote").add($('.cell2').eq(rand).find(".author")).delay(500).fadeIn(1000);
	}	
	
	function FadeOut(rand,randT){
		$('.cell2').eq(rand).className = "cell2 faded";
		$('.cell2').eq(rand).find(".quote").add($('.cell2').eq(rand).find(".author")).delay(2000).fadeOut(1500,function(){
				FadeIn(rand);		
		});
		
	}


	var headerAlpha = function(){
        var alpha = Math.max(Math.min($(window).scrollTop() / 350,1), 0);
            //$('#header').css({"background-color":"rgba(10,10,10,"+alpha+")"})
    }
    headerAlpha();
    $(window).scroll(headerAlpha);

    var cssWhenScrolled = function(el, obj1, obj2) {
        if($(window).scrollTop() + $(window).height() > $(el).offset().top + $(el).height()/2)
        {
            return;
        }
        $(el).css(obj1);
        var didit = false;
        $(window).scroll(function() {
            if($(window).scrollTop() + $(window).height() > $(el).offset().top + $(el).height()/2 && !didit)
            {
                $(el).animate(obj2, 500);
                didit=true;
            }
        });
    }

	if(window.location.hash == "#getmathbreakers") {
		window.location.href = "/preorder/";
	}

    if(window.location.hash == "#createaccount") {
        $("#createAccountButton").click();
    }

    $("#getoptionfull").click(function() {
        base.buyPopup("mbfull");
    });

    $("#getoptiondeluxe").click(function() {
        base.popup("#comingsoon");
        /*
        base.buyPopup("mbdeluxe", function() {
            base.popup("#postPurchasePopup");
            $("#postPurchasePopupContent").html("de de luxe");
        });
        */
    });    

	$("#downloadEmailForm").submit(function(e) {
		e.preventDefault();
		$("#downloadEmailSubmit").click();
	});

    var downloadclick = function(platform, closepopup) {
        $("#downloadEmailSubmit").off('click');
        $("#downloadEmailSubmit").click(function(e) {
            ajaxFormSubmit(e, "#downloadEmailForm", "/ajax/download/"+platform, function(response) {
                closepopup();
                window.location.href = response.url;
            });            
        });
    }

    if(haveEmail) {
        $("#macdownload").click(function() {
            window.location.href = "/static/builds/latest/mathbreakers_mac.zip";
        });

        $("#windownload").click(function() {
            window.location.href = "/static/builds/latest/mathbreakers_windows.zip";
        });
    }
    else {
        $("#macdownload").click(function() {
            var closepopup = base.popup("#downloadEmailPopup");
            downloadclick("mac", closepopup);
        });

        $("#windownload").click(function() {
            var closepopup = base.popup("#downloadEmailPopup");
            downloadclick("win", closepopup);
        });
    }

});

