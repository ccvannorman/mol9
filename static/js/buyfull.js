$(document).ready(function() {
	var item="mbfull";
	var handler = StripeCheckout.configure({
	          key: stripekey,
	          image: '/static/img/icon_mathbreakers_small.png',
	          token: function(response) {
	          	$("#stripeform").attr("action", "/purchase/stripe/" + item + "/");
	            var tokenInput = $("<input type=hidden name='stripeToken'/>").val(response.id);
	            var emailInput = $("<input type=hidden name='stripeEmail'/>").val(response.email);
	            $("#stripeform").append(tokenInput).append(emailInput).submit();
	          }});	

	$("#stripeBuy").click(function(){
				var price = parseInt(purchases[item]['price']);
				handler.open({
			      name: 'Mathbreakers',
			      description: purchases[item]['name'] + "( $" + price + " )",
			      amount: price * 100
			    });	
	});
});
