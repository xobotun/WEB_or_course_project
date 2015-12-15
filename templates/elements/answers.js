<script type="text/javascript">
	function ajax_vote(aid){
		$.ajax({
			url : "ajax/", // the endpoint
			type : "POST", // http method
			data : { type: 'question_vote', message: {question_id: '{{quid}}', answer_id: aid}, {% csrf_token %} }, // data sent with the post request

			// handle a successful response
			success : function(json) {
				//$('#post-text').val(''); // remove the value from the input
				console.log(json); // log the returned json to the console
				console.log("success"); // another sanity check
			},

			// handle a non-successful response
			/*error : function(xhr,errmsg,err) {
				$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
					" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}*/
		});
	});
</script>