
function DeleteBug(desc){
	// AJAX for posting
	console.log("create post is working!") // sanity check

	$.post("/modifydb/deleterow/",{
			"model" : "Bug", 
			"col" : "description",
			"val" : desc,
			"csrfmiddlewaretoken" : csrf},
		function(response) {
			if(response['success']) {		
			}
			else {
			}
	});
	
	// console.log('desc: ' + desc);
	setTimeout(function () {
		location.reload();
    }, 500);
}
