function Start(){
	setInterval(function() { ObserveInputValue($('#id_num_students').val()); }, 100);
}

$(document).ready(function() {
	var item="teacherpurchase";
	var handler = StripeCheckout.configure({
	          key: stripekey,
	          image: '/static/img/icon_mathbreakers_small.png',
	          token: function(response) {
	          	$("#purchaseform").attr("action", "/purchase/stripe/" + item + "/");
	            var tokenInput = $("<input type=hidden name='stripeToken'/>").val(response.id);
	            var emailInput = $("<input type=hidden name='stripeEmail'/>").val(response.email);
	            var numLicenses = $("<input type=hidden name='numLicenses'/>").val($("#id_num_students").val());
	            var theform = $("#purchaseform");
	            theform.append(tokenInput).append(emailInput).append(numLicenses);
	            //console.log(theform);
	            theform.submit();
	          }});	

	$("#stripeBuy").click(function(){
				var numstudents = parseInt($("#id_num_students").val());
				if(isNaN(numstudents) || (numstudents + num_existing_licenses) <= 9) {
					$("#errornum").show();
					return;
				}
				$("#errornum").hide();
				var price = parseInt(purchases[item]['price']) * numstudents;
				handler.open({
			      name: 'Mathbreakers',
			      description: purchases[item]['name'] + "( $" + price + " )",
			      amount: price * 100
			    });	
	});


});

function ObserveInputValue(v){
	v = Math.floor(parseInt(v));
	if(isNaN(v) || (v + num_existing_licenses) <= 9) { v = 0; }
	$('#totalcost').text(" $"+v*3+".00");
}