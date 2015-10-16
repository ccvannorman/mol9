var base = {};

$(document).ready(function() {

	var postpurchases = {
		"mbfull": (function() {
            		base.popup("#postPurchasePopup", function() {location.reload(false);});
            		$("#postPurchasePopupContent").html("<p>Now you can download the game and log in to access all the levels.</p>");
        		}),
		"upgrade": (function() {
            		base.popup("#postPurchasePopup", function() {location.reload(false);});
            		$("#postPurchasePopupContent").html("<p>You now have all lesson packs available.</p>");
        		}),		
	}

	var closeCurrentPopup = null;

	var popup = function(divid, onclose) {
		if(closeCurrentPopup) { closeCurrentPopup(); }
		var popup = $(divid);
		popup.fadeIn(200);
		popup.css(
			{
				"left":($(window).innerWidth() - popup.outerWidth()) / 2,
				"top":($(window).innerHeight() - popup.outerHeight()) / 2
			});
		var bg = $("#black");

		var closeitOnEscape = function(e) {
			if(e.keyCode == 27) { closeit(); }
		}

		var closeit = function() {
			popup.hide();
			bg.hide();
			bg.off();
			$(".popup .notice").remove();
			$(document).off("keyup");
			if(onclose) { onclose(); }
		}

		bg.show();
		bg.click(closeit);
		$(document).keyup(closeitOnEscape);
		closeCurrentPopup = closeit;
		return closeit;
	}
	var makePopupButton = function(buttonid, divid) {
		$(buttonid).click(function() {
			popup(divid);
		});
	}

	$("#createAccountForm").submit(function(e) {
		e.preventDefault();
		$("#createAccountSubmit").click();
	});
	$("#signinForm").submit(function(e) {
		e.preventDefault();
		$("#signinSubmit").click();
	});

	makePopupButton("#createAccountButton", "#createAccountPopup");
	makePopupButton("#signinButton", "#signinPopup");
	base.makePopupButton = makePopupButton;

	$("#createAccountSubmit").click(function(e) {
		ajaxFormSubmit(e, "#createAccountForm", "/ajax/createaccount/", function() {
			window.location.hash="#postcreate";
			location.reload();
		})
	});

	$("#signinSubmit").click(function(e) {
		ajaxFormSubmit(e, "#signinForm", "/ajax/signin/", function() {
			location.reload(false);
		})
	});	

	$("#navbuyupgrade").click(function() {
		base.popup('#kickstarterPopup');
	});


	var purchaseFailure = function(action) {

	}

	var purchaseGotToken = function(jwt, onSuccess) {
		google.payments.inapp.buy({
		    'jwt'     : jwt,
		    'success' : onSuccess,
		    'failure' : purchaseFailure
		  });
	}

	var purchase = function(item) {
		var onSuccess = postpurchases[item];
		if(BUYDEBUG) { onSuccess(); return; }
		$.post("/purchase/ajax/token/", {"item":item, "csrfmiddlewaretoken":csrf}, function(response) {
			if(response["success"]) {
				closeCurrentPopup();
				purchaseGotToken(response["jwt"], onSuccess);
			}
		});
	}

    base.popup = popup;
    base.buyPopup = function(item) {
    	$("#buyPopupHeader").text(purchases[item]['name']);
    	$("#buyPopupParagraph").text(purchases[item]['confirmation_description']);
		$("#buyFinally").text("Buy $" + purchases[item]['price']);

    	var hasAccount = function() {
			$("#buyCreateAccount").hide();
			$("#buyHaveAccount").show();
			$("#buyHaveAccount h1").text("Hi, " + user + "!");

			var handler = StripeCheckout.configure({
	          key: stripekey,
	          image: '/static/img/icon_mathbreakers_small.png',
	          token: function(response) {
	          	$("#stripeform").attr("action", "/purchase/stripe/" + item + "/");
	            var tokenInput = $("<input type=hidden name=stripeToken />").val(response.id);
	            var emailInput = $("<input type=hidden name=stripeEmail />").val(response.email);
	            $("#stripeform").append(tokenInput).append(emailInput).submit();
	          }});	

			$("#buyFinally").off("click");
			$("#buyFinally").click(function(e) {

				handler.open({
			      name: 'Mathbreakers',
			      description: purchases[item]['name'] + "( $" + purchases[item]['price'] + " )",
			      amount: purchases[item]['price'] * 100
			    });		
			    /*				
				if(user != "") {
					purchase(item);
				}
				else {

				}
				*/
			})
    	}

		if(user == "") {
			$("#buyCreateAccount").show();		
			$("#buyHaveAccount").hide();
			$("#createAccountSubmit2").click(function(e) {
				ajaxFormSubmit(e, "#createAccountForm2", "/ajax/createaccount/", function(response) {
					window.location.hash = "#buy." + item;
					location.reload(false);
				});
			});	
		} else {
			hasAccount();
		}
		popup("#buyPopup");
	}

	setTimeout(function() {
	    var hash = window.location.hash.substring(1);
	    if(hash == "postcreate" && window.location.href.indexOf("redeem") == -1) {
	        popup("#postCreatePopup");
	        window.location.hash = "";
	    }	
	    if(hash.substring(0,3) == "buy") {
	    	var item = hash.substring(4);
	    	var cb = null;
	    	base.buyPopup(item, cb);
	    	window.location.hash = "";
	    }
	}, 500)

	var isClickEventRequestingNewTab = function(clickEvent) {
    	return clickEvent.metaKey || clickEvent.ctrlKey || clickEvent.which === 2;
	};

	$("a,input[type=submit]").click(function(e) {
		var page = window.location.href;
		page = page.replace(/^(?:\/\/|[^\/]+)*\//, "");
		page = page.replace(/(#.+)$/, "");
		page = page.replace(/(\/)/, "");
		if(page=="") { page = "home"; }
		var name = e.target.id;
		var href = $(e.target).attr("href");
		if(href && (href.indexOf("javascript") == 0 || href[0] == "#"))
		{
			$.post("/ajax/buttonlog/"+name+"/", {"csrfmiddlewaretoken":csrf}, function() {

			});
		}
		else {
			var d = new Date();
			d.setTime(d.getTime()+(30*24*60*60*1000));
			document.cookie = "buttonlog="+name+"; expires="+d.toGMTString() + "; path=/";
		}
	
	});

	var bli = document.cookie.indexOf("buttonlog");
	if(bli >= 0)
	{
		var cookies = document.cookie.split(";");
		for(var i = 0; i < cookies.length; i++){
			if(cookies[i].indexOf("buttonlog") >= 0)
			{
				var name = cookies[i].substr(11);
				$.post("/ajax/buttonlog/"+name+"/", {"csrfmiddlewaretoken":csrf}, function() {});
			}
		}

		document.cookie = 'buttonlog=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';	
	}
    $(function() { $('body').hide().show(); });
});
