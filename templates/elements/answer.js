<script type="text/javascript">
	$('#answer_{{aid}}_voteup_button').click(function(){
		ajax_answer_vote({{aid}}, 'up');
		$('#answer_{{aid}}_votedown_button').removeClass('voted-down');
		$('#answer_{{aid}}_voteup_button').addClass('voted-up');
	});
	$('#answer_{{aid}}_votedown_button').click(function(){
		ajax_answer_vote({{aid}}, 'down');
		$('#answer_{{aid}}_votedown_button').addClass('voted-down');
		$('#answer_{{aid}}_voteup_button').removeClass('voted-up');
	});
	$('#answer_{{aid}}_checkbox').click(function(){
		ajax_answer_checkbox({{aid}});
	});
</script>