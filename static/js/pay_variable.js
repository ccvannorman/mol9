$(document).ready(function() {
	var item="variablepay";
	var handler = StripeCheckout.configure({
	          key: stripekey,
	          image: '/static/img/icon_mathbreakers_small.png',
	          token: function(response) {
	          	$("#purchaseform").attr("action", "/purchase/stripe/" + item + "/");
	            var tokenInput = $("<input type=hidden name='stripeToken'/>").val(response.id);
	            var emailInput = $("<input type=hidden name='stripeEmail'/>").val(response.email);
	            var dollars = $("<input type=hidden name='dollars'/>").val($("#id_dollars").val());
	            var theform = $("#purchaseform");
	            theform.append(tokenInput).append(emailInput).append(dollars);
	            //console.log(theform);
	            theform.submit();
	          }});	

	$("#stripeBuy").click(function(){
				var dollars = parseFloat($("#id_dollars").val());
				if(isNaN(dollars) || dollars <= 0) {
					$("#errornum").show();
					return;
				}
				$("#errornum").hide();
				handler.open({
			      name: 'Mathbreakers',
			      description: purchases[item]['name'] + "( $" + dollars.toFixed(2) + " )",
			      amount: parseInt(dollars * 100)
			    });	
	});


});