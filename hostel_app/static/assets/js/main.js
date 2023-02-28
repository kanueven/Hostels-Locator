$(document).ready(function () {
	// get select with id location
	var location = $("#locationSelect");
	// detect select onchange
	location.change(function (e) {
		// get the selected value
		var selectedLocation = $(this).val();
		// pass variable as query to the page
		window.location.href = `/hostels/?location=${selectedLocation}`;
	});
});
