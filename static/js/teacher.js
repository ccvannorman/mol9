$(document).ready(function() {
	$("#teacherSignupSubmit").click(function(e) {
		ajaxFormSubmit(e, "#teacherSignupForm", "/ajax/createteacheraccount/", function(response) {
			location.reload();
		});
	});
	$("#teacherConvertSubmit").click(function(e) {
		ajaxFormSubmit(e, "#teacherConvertForm", "/ajax/convertteacheraccount/", function(response) {
			location.reload();
		});
	});	
});