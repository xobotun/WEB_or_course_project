<script type="text/javascript">
	$('#question_{{quid}}_voteup_button').click(function(){
		ajax_question_vote({{quid}}, 'up');
		$('#question_{{quid}}_votedown_button').removeClass('voted-down');
		$('#question_{{quid}}_voteup_button').addClass('voted-up');
	});
	$('#question_{{quid}}_votedown_button').click(function(){
		ajax_question_vote({{quid}}, 'down');
		$('#question_{{quid}}_votedown_button').addClass('voted-down');
		$('#question_{{quid}}_voteup_button').removeClass('voted-up');
	});
</script>