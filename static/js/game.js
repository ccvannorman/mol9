var settings = {
	"hat":0,
	"hair":0,
	"hair_color":0,
	"hair_type":0,
	"eyes":0,
	"body":0,
	"arms":0
};

$(document).ready(function() {

	var colors = {
		0:[0, 0.0, 0.33],		// black
		1:[-111, 1.5, 0.33],	// navy
		2:[-22, 1.0, 1.0],		// fuschia
		3:[123, 1.3, 0.5],		// green
		4:[-155, 1.0, 1.0],		// Sky blue		
		5:[170, 1.4, 0.9],		// mint?
		6:[25, 1.0, 1.0],		// orange
		7:[-16, 0.4,1.3],		// pink
		8:[-80, 1.14, 0.77],	// purple
		9:[0, 1.0, 1.0],		// red
		10:[39, 0, 1.5],		// white
		11:[69, 1.0, 1.5],		// yellow?
		12:[0, 0.0, 1.1],		// gray
		13:[-80, 0.3, 1.45],	// lavender
	};

	function colorizeFromIndex(el, ind) {
		colorlist = colors[ind];
		el.css("-webkit-filter", "hue-rotate("+colorlist[0]+"deg) saturate("+colorlist[1]+") brightness("+colorlist[2]*1.5+")");
		el.css("-moz-filter", "hue-rotate("+colorlist[0]+"deg) saturate("+colorlist[1]+") brightness("+colorlist[2]*1.5+")");
		el.css("filter", "hue-rotate("+colorlist[0]+"deg) saturate("+colorlist[1]+") brightness("+colorlist[2]*1.5+")");
	}

	colorizeFromIndex($("#robotbody"), settings["body"]);
	colorizeFromIndex($("#robotarms"), settings["arms"]);
	colorizeFromIndex($("#roboteyes"), settings["eyes"]);

	var num_colors = 14;

	function colorSwitcher(btn, bodypart, step) {
		var target = $("#robot"+bodypart);
		$(btn).click(function() {
			settings[bodypart] = (settings[bodypart] + step) % num_colors;
			if(settings[bodypart] < 0) { settings[bodypart] = num_colors + settings[bodypart]; }
			colorizeFromIndex(target, settings[bodypart])
		});
	}

	function hatSwitcher(btn, step) {
		var target = $("#robothat");
		$(btn).click(function() {
			settings["hat"] = (settings["hat"] + step) % 7;
			if(settings["hat"] < 0) { settings["hat"] = 7 + settings["hat"]; }
			target.css("background-position", (-240 * settings["hat"]))
		});
	}

	function hairSwitcher(btn, step) {
		var target = $("#robothair");
		var totalnum = num_colors * 3 + 1;
		$(btn).click(function() {
			settings["hair"] = (settings["hair"] + step) % totalnum;
			if(settings["hair"] < 0) { settings["hair"] = totalnum + settings["hair"]; }
			var ci = 0;
			var hi = 0;
			if(settings["hair"] == 0) {
				hi = 0;
				ci = 0;
			}
			else {
				var sh = settings["hair"] - 1;
				ci = Math.floor(sh / 3);
				hi = sh % 3 + 1;
			}
			settings["hair_type"] = hi;
			settings["hair_color"] = ci;
			target.css("background-position", (-222 * hi))

			colorizeFromIndex(target, ci);
		});
	}	

	colorSwitcher("#bodyleft", "body", -1);
	colorSwitcher("#bodyright", "body", 1);
	colorSwitcher("#armsleft", "arms", -1);
	colorSwitcher("#armsright", "arms", 1);	
	colorSwitcher("#eyesleft", "eyes", -1);
	colorSwitcher("#eyesright", "eyes", 1);	
	hatSwitcher("#hatleft", -1);
	hatSwitcher("#hatright", 1);
	hairSwitcher("#hairleft", -1);
	hairSwitcher("#hairright", 1);	


});

