$(document).ready(function() {
	var onSuccess = function() {
		$("#campForm").html("<h2 style='margin:auto;text-align:center'>Thanks for signing up!</h2>");
	}

	var onFailure = function() {

	}

	$("#submitCampForm").click(function(e) {
		ajaxFormSubmit(e, "#campForm", "/camp/signup/", function(response) {
			var jwt = response['token']
			google.payments.inapp.buy({
			    'jwt'     : jwt,
			    'success' : onSuccess,
			    'failure' : onFailure
			  });		
		});
	});
});
