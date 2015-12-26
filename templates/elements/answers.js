<script type="text/javascript">
	//From official documentation
	// using jQuery
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	
	var csrftoken = getCookie('csrftoken');

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (/*!csrfSafeMethod(settings.type) && */!this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
		
	function ajax_answer_vote(aid, sign){
		$.ajax({
			url : "/ajax/", // the endpoint
			type : "POST", // http method
			data : { type: 'answer_vote', message: {question_id: '{{quid}}', answer_id: aid, vote_sign: sign} }, // data sent with the post request

			// handle a successful response
			success : function(json) {
				//$('#post-text').val(''); // remove the value from the input
				console.log(json.type + ":"); // another sanity check
				console.log(json); // log the returned json to the console
				$('#answer_' + json.message.answer_id + '_rating_label').html(json.message.new_rating);
			},

			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				//$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				//	" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				var myWindow = window.open("data:text/html," + xhr.responseText, "_blank", "width=200,height=100");
				myWindow.focus();
			}
		});
	}
	
	function ajax_answer_checkbox(aid)
	{
		$.ajax({
			url : "/ajax/", // the endpoint
			type : "POST", // http method
			data : { type: 'answer_checkbox', message: {question_id: '{{quid}}', answer_id: aid} }, // data sent with the post request

			// handle a successful response
			success : function(json) {
				//$('#post-text').val(''); // remove the value from the input
				console.log(json.type + ":"); // another sanity check
				console.log(json); // log the returned json to the console
				if (json.message.new_state == false)
					$('#answer_' + json.message.answer_id + '_checkbox').removeClass('correct-answer-checkbox-inner-thing-checked');
				else
					$('#answer_' + json.message.answer_id + '_checkbox').addClass('correct-answer-checkbox-inner-thing-checked');
			},

			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				//$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				//	" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				var myWindow = window.open("data:text/html," + xhr.responseText, "_blank", "width=200,height=100");
				myWindow.focus();
			}
		});
	}
</script>