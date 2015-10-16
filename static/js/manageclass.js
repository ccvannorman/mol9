$(document).ready(function() {
	var updateStudentNotice = function() {
		if($("table tbody").children().length > 0) {
			$("#nostudents").hide();
		}
		else {
			$("#nostudents").show();
		}
	}

	var resetEvents = function() {
		$(".remove").off("click");
		$(".remove").click(function(e) {
			var name = $(e.target).attr("data");

			$.post("/class/ajax/remove/",
				{"username":name, "csrfmiddlewaretoken":csrf},
				function(response) {
					if(response['success']) {
						$(e.target).parent().parent().remove();
						updateStudentNotice();
					}
			});
		});

		$(".reset").off("click");
		$(".reset").click(function(e) {
			var btn = $(e.target);
			var name = btn.attr("data");
			var inp = $("<input type='text'>");
			var par = btn.parent();
			inp.keypress(function(e) {
				if(e.which == 13) {
					$.post("/class/ajax/setpassword/",
						{"username":name, "password":inp.val(), "csrfmiddlewaretoken":csrf},
						function(response) {
							console.log(response);
							inp.remove();
							par.append(btn);
							resetEvents();
					});
				};
			});
			par.append(inp);
			btn.remove();
		});


	}

	var addStudent = function(obj) {
		name = obj["name"];
		username = obj["username"];
		playtime = obj["playtime"];
		var tab = $("table");
		var row = $("<tr>");
		row.append("<td class='name'>" + name + "</td>");
		row.append("<td class='playtime'>" + playtime + " minutes played</td>");
		//row.append("<td><a href='javascript:void(0)' class='reset' data='"+name+"''>Set password</a></td>");
		//row.append("<td><a href='/user/"+name+"/'>User page</a></td>");
		row.append("<td><a href='javascript:void(0)' class='remove' data='"+username+"'>Remove</a></td>");
		tab.append(row);
	}

	$.get("/class/ajax/getstudents/preventCache="+new Date(), function(response) {
		for(var i = 0; i < response.students.length; i++) {
			addStudent(response.students[i]);
		}
		resetEvents();
		updateStudentNotice();
		$("#ajaxing").hide();
	});

	$("#createStudent").click(function() {
		var name = $("#createStudentName").val();
		//var password = $("#createStudentPassword").val();
		$.post("/class/ajax/create/",
			{"username":name, "password":"default", "csrfmiddlewaretoken":csrf},
			function(response) {
				if(response['success']) {
					addStudent({"name":name, "username":response["username"], "playtime":0});
					resetEvents();
					updateStudentNotice();
					$("#createStudentName").css("border-color","#ccc");
					$("#createStudentName").val("");
					$("#createStudentPassword").val("");
				}
				else {
					$("#createStudentName").css("border-color","#c22");
				}
			});
	});

	$("#addStudent").click(function() {
		var name = $("#addStudentName").val();
		$.post("/class/ajax/add/",
			{"username":name, "csrfmiddlewaretoken":csrf},
			function(response) {
				if(response['success']) {
					addStudent(name);
					resetEvents();
					updateStudentNotice();
					$("#addStudentName").css("border-color","#ccc");
					$("#addStudentName").val("");
				}
				else {
					$("#addStudentName").css("border-color","#c22");
				}
			});
	});	
});
