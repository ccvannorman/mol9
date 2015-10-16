function Fade(){
		$('#mainSplash').fadeTo('slow', 1, function(){
			$img = DJANGO_STATIC_URL+'img/h'+imageIndex%6+'.png';
			$(this).css('background-image', 'url(' + $img + ')');
			imageIndex++;
		})
		setTimeout(function() {
			Fade();
		},9000);

		console.log("heillo "+imageIndex);
}

var imageIndex = 0;
$(document).ready(function() {
		Fade();


    var headerAlpha = function(){
        var alpha = Math.max(Math.min($(window).scrollTop() / 350,1), 0);
            $('#header').css({"background-color":"rgba(10,10,10,"+alpha+")"})
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

