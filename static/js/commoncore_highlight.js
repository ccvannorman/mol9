$(document).ready(function() {
	if(window.location.hash) {
		var hash = window.location.hash.replace(/\./g, "\\.");
		var p = $(hash).parent();
		var oldcolor = p.css("backgroundColor");
		//p.css("backgroundColor","#fe3");
		p.css("outline","4px solid #1e3");
	}
});