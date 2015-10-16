$(document).ready(function() {
	var item="preorder";
	var handler = StripeCheckout.configure({
	          key: stripekey,
	          image: '/static/img/icon_mathbreakers_small.png',
	          token: function(response) {
	          	$("#stripeform").attr("action", "/purchase/stripe/" + item + "/");
	            var tokenInput = $("<input type=hidden name=stripeToken />").val(response.id);
	            var emailInput = $("<input type=hidden name=stripeEmail />").val(response.email);
	            $("#stripeform").append(tokenInput).append(emailInput).submit();
	          }});	

	$("#stripeBuy").click(function(){
				handler.open({
			      name: 'Mathbreakers',
			      description: purchases[item]['name'] + "( $" + purchases[item]['price'] + " )",
			      amount: purchases[item]['price'] * 100
			    });	
	});
});
