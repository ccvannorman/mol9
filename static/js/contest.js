$(document).ready(function() {
	$('#shareFB').click(function() {
		window.open("https://www.facebook.com/sharer/sharer.php?u=http://mathbreakers.com/contest/", "Share on Facebook", "status=1,height=300, width=600, resizable=0");
	});
	
	$('#shareTwitter').click(function() {
		window.open("http://clicktotweet.com/U40cd");
	});	

	$('#contestsubmit').click(function(e){
		ajaxFormSubmit(e, '#contestForm', '/ajax/contestregister/', function() {
			$("#contestForm").html("<h2>You're in!</h2>");
		});
	});
});