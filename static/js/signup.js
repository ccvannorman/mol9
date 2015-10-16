(function() {
	$(document).ready(function() {
		var checkbox = $('#emailSignup input[name=over_13]');
		checkbox.change(function() {
			$('#emailSignup input[name=parent_email]').parent().toggle(!checkbox.is(':checked'));
		});
		

		setupForm("#emailSignup", "/ajax/signup/");
	});

})();