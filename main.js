$(document).ready(function() {
    // Define a variable to store the extref
    let selectedExtref;
    let partySize;
    let reservationTime;
    let canReserve = false;

    // Initialize Select2 on the select boxes
    $('#locationSelect').select2({
        placeholder: 'Select a location',
        allowClear: true
    });

    $('#partySizeSelect').select2({
        placeholder: 'Select party size',
        allowClear: true
    });

    // Fetch the locations from the server and populate the select box
    $.get("http://localhost:5000/get_locations", function(data, status){
        for (let i = 0; i < data.length; i++) {
            let opt = new Option(data[i].name + ', ' + data[i].city + ', ' + data[i].state, data[i].extref, false, false);
            $('#locationSelect').append(opt);
        }
    });

    $('#reservationForm').on('submit', function (e) {
        e.preventDefault();

        // Gather the form values
        let firstName = $('#firstName').val();
        let lastName = $('#lastName').val();
        let email = $('#email').val();
        let phoneNumber = $('#phoneNumber').val();
        let includeHighchair = $('#includeHighchair').prop('checked');

        $.ajax({
            url: 'http://localhost:5000/submit_reservation',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                // Handle the response from the server
                alert(response);
                console.log(response);
            },
            data: JSON.stringify({
                partySize: partySize,
                reservationTime: reservationTime,
                extref: selectedExtref,
                firstName: firstName,
                lastName: lastName,
                email: email,
                phoneNumber: phoneNumber,
                includeHighchair: includeHighchair
            })
        });
    });

    // Listen for changes to the select box
   $('#locationSelect').on('change', function (e) {
        selectedExtref = $(this).val();
        partySize = $('#partySizeSelect').val();
        reservationTime = $('#reservationTime').val();

        // Only fetch wait time if a location, party size and reservation time are selected
        if (selectedExtref && partySize && reservationTime) {
            // Update the selected location ID on the page
            $('#selectedLocation').text('Selected location ID: ' + selectedExtref);

            // Fetch wait time quote for selected location
        $.get(`http://localhost:5000/get_wait_time/${selectedExtref}/${partySize}`, function(data, status){
            let minQuote = data;

            // Get current time in minutes
            let currentDate = new Date();
            let currentMinutes = currentDate.getHours() * 60 + currentDate.getMinutes();

            // Get reservation time in minutes
            let reservationTimeParts = reservationTime.split(':');
            let reservationMinutes = parseInt(reservationTimeParts[0]) * 60 + parseInt(reservationTimeParts[1]);

            if ((reservationMinutes + minQuote) <= currentMinutes) {
                canReserve = false;
                // Display a message to the user if the reservation is not possible
                $('#waitTimeWarning').text('Warning: The reservation is not possible as the wait time is more than the time left until the reservation.');
            } else {
                canReserve = true;
                $('#waitTimeWarning').text('');
            }
        });

        } else {
            $('#selectedLocation').text('No location selected yet');
            $('#waitTimeWarning').text('');
        }

    });

});
