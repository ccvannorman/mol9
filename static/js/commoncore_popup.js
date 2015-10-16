$(document).ready(function() {
	var desc = $('#lessondesc');
	$('.lesson').mouseover(function(el) {
		desc.show();
		var targ = $(el.target);
		var lesson = targ.attr('data');
		desc.html(lesson);
		var pos = targ.position();
		if(pos.left < $(window).width() / 2)
		{
			pos.left += targ.width();
		}
		else
		{
			pos.left -= desc.width();
		}
		pos.top -= desc.height() / 2;
		desc.offset(pos);
		
	});

	$('.lesson').mouseout(function(el) {
		desc.hide();
	});
});