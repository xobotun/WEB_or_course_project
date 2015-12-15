<script type="text/javascript">
	$('#answer_{{aid}}_voteup_button').click(function(){
		ajax_answer_vote({{aid}}, 'up');
	});
	$('#answer_{{aid}}_votedown_button').click(function(){
		ajax_answer_vote({{aid}}, 'down');
	});
</script>