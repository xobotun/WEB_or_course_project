<script type="text/javascript">
	$('#question_{{quid}}_voteup_button').click(function(){
		ajax_question_vote({{quid}}, 'up');
	});
	$('#question_{{quid}}_votedown_button').click(function(){
		ajax_question_vote({{quid}}, 'down');
	});
</script>