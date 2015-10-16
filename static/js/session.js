$(document).ready(function() {
	var start = Date.now();
	var checkUsers = function() {
		$.ajax({
			url:"/session/ajax/users/",
			type:"GET",

			success:function(msg) {
				if(msg['users'].length > 0) {
					$("#userlist").html("");
					$("#seedashboard").show()
					for(var i = 0;i < msg['users'].length; i++) {
						var user = msg['users'][i]
						if(user['active']) {
							var u = $("<div class='user playing'>" + user['name'] +" (now playing - " + user['playtime'] + " minutes)</div>");
						}
						else if(user['playtime'] > 60){
							var u = $("<div class='user expired'>" + user['name'] +" (played " + user['playtime'] + " minutes)</div>");
						}						
						else if(user['playtime'] > 0){
							var u = $("<div class='user'>" + user['name'] +" (played " + user['playtime'] + " minutes)</div>");
						}
						else {
							var u = $("<div class='user'>" + user['name'] +"</div>");
						}
						$("#userlist").append(u);
					}
					if(Date.now() - start > 1000 * 60 * 5) {
						$("#saveclass").show();
					}
				}
			},

			failure:function(msg) {
				console.log(msg);
			}
		});	
	}

	var checkTimer = function() {
		$.ajax({
			url:"/session/ajax/playtime/",
			type:"GET",

			success:function(msg) {
				$("#expiredstudents").empty();
				if(msg['has_playtime']) {
					if(msg['licenses'] == 0){
						$("#playtimenotice").show();
						$("#playtime").text(msg['avg'] +" remaining per student (average)");
						if(msg['expired'].length > 0) {
							$("#playtimenotice").addClass('ended');
							for(var i = 0; i < msg['expired'].length; i++) {
								$("#expiredstudents").append($("<li>Expired: " + msg['expired'][i] + "</li>"));
							}
						}
					}
					else if(msg['licenses'] < msg['num_students']) {
						$("#playtimenotice").removeClass('ended');
						$("#playtimenotice").show();
						$("#playtime").text("Warning: You have " + msg['licenses'] +
							" licenses but " + msg["num_students"] + " students." +
							" Only " + msg["licenses"] + " students will be able to play at once.");
					}
					else {
						$("#playtimenotice").hide();
					}
				}
			},

			failure:function(msg) {
				console.log(msg);
			}
		});	
	}

	setInterval(checkUsers, 10000);
	setInterval(checkTimer, 10000);
	checkTimer();
	checkUsers();

	$("#expandInstructions").click(function() {
		$("#instructions").toggle();
		$("#expandInstructions").toggle();
	});
	$("#closeInstructions").click(function() {
		$("#instructions").toggle();
		$("#expandInstructions").toggle();
	});	
});