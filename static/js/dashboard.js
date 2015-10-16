$(document).ready(function() {

	var showLog = function(text) {
		
		$("#assignmentLog").finish();
		$("#assignmentLog").fadeTo(400, 1.0).delay(3000).fadeOut(3000);
		$("#assignmentLog").text(text);
	}

	$(".dashboard").scroll(function() {
		var off = $(".dashboard").offset().left + 20;
		$("#assignmentLog").offset({left:off});
	});

	var reassignAll = function() {
		$(".assignable").click(function(e) {
			var me = $(e.target);
			if(!me.hasClass("assignable")) {
				me=me.parent();
			}
			var student = me.attr("student");
			var student_name = me.attr("student_name");
			var level = me.attr("level");
			var assigned = me.attr("assigned") == "true";
			if(!assigned) {
				$.post("/class/ajax/assign/", {
					"student":student,
					"level":level,
					"csrfmiddlewaretoken":csrf},
					function(response) {
						if(response.success) {
							me.empty();
							var asn = $("<div class='assigned'></div>");
							me.append(asn);
							me.attr("assigned", true);
							showLog("Assigned " + level + " to " + student_name);
						}
					});
			}
			else {
				$.post("/class/ajax/unassign/", {
					"student":student,
					"level":level,
					"csrfmiddlewaretoken":csrf},
					function(response) {
						if(response.success) {
							me.empty();
							var asn = $("<div class='unassigned'></div>");
							me.append(asn);							
							me.attr("assigned", false);
							showLog("Removed assignment from " + student_name);
						}
					});
			}
		});
	}

	reassignAll();
});