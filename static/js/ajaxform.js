var setupForm = function(selector, endpoint) {
	$(selector).submit(function(e) {
		ajaxFormSubmit(e, selector, endpoint, function() {
			$(selector).html('<h2>Thanks!</h2>');
		});
	});
}

var ajaxFormSubmit = function(e, selector, endpoint, after) {
	e.preventDefault();

	$(selector + ' .error').remove();

	obj = {}
	$(selector + ' *').filter(':input').each(function(k, v){
		if( $(v).is(":visible") || $(v).attr('name') == 'csrfmiddlewaretoken' ) {
			if( $(v).attr('type') == 'checkbox' ){
				obj[$(v).attr('name')] = $(v).is(':checked');
			}
			else if ( $(v).attr('type') != 'submit' ){
					obj[$(v).attr('name')] = $(v).val();
				}
			}
	});

	$.post(endpoint, obj, function(response) {
		if(response['result'] == 'success') {
			after(response);
		}
		else {
			console.log(response);
			for(key in response['errors']) {
				var err = $('<div class="error">' + response['errors'][key] + '</div>');
				if( $(selector + ' input[name='+key+']').length )
				{
					$(selector + ' input[name='+key+']').parent().append(err);
				}
				else {
					$(selector + " .catchAll").append(err);
				}
			}
		}
	});	
}