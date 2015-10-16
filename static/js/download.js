(function() {
/*	$(document).ready(function() {
		$('#windl').click(function(e) {
			ajaxFormSubmit(e, "#downloadForm", "/ajax/download/win", function(response) {
				window.location.href = response['url'];
			});
		});
		$('#macdl').click(function(e) {
			ajaxFormSubmit(e, "#downloadForm", "/ajax/download/mac", function(response) {
				window.location.href = response['url'];
			});
		});	

		var checkbox = $('#downloadForm input[name=over_13]');
		checkbox.change(function() {
			$('#downloadForm input[name=parent_email]').parent().toggle(!checkbox.is(':checked'));
		});			
	});

*/


})();

function AddDownloadResponseToGoogleDoc(){ // Charlie
	var email = $('#downloadEmail').val();
	var parentemail = $('#downloadParentEmail').val();
	var hearaboutus = $('#hearaboutus').val();
	


	// Download survey
	
	// Data order:
	// entry.1769026509 hearaboutus
	// entry.638716550 email1
	// entry.2076140035 email2
	// entry.265792676 platform
	
	
	$.ajax({
		url: "https://docs.google.com/forms/d/19nnHJID3OwZsOsIxymsSmORnua58wTBsh8P2b1uqkfs/formResponse",	 			
		data: {"entry.1769026509": hearaboutus, "entry.638716550": email, "entry.2076140035": parentemail},
		type: "POST",
		dataType: "xml",

		success: function(msg) {
			/* 		    $('#success').html('hi'+msg); */
		},
		error: function(msg) {
			/* 		    $('#success').html('bhi'+msg); */
		}

	});
	
	
	


}

