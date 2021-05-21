$(document).ready(function() {
	$('#datePicker').datepicker({
		format : 'mm/dd/yyyy'
	}).on('changeDate', function(e) {
	});

	var checkin = $('#dpd1').datepicker({
		startDate : '0',
	}).on('changeDate', function(ev) {
		var date2 = $('#dpd1').datepicker('getDate');

		console.log("jjjjjjjjjjjjjjjjjjj",date2)
//		rmmmmmmmmmmm111111
		var checkout = $('#dpd2').datepicker({
		startDate : date2
		});
	});
});