document.getElementById('pay-electricity-btn').addEventListener('click', function (event) {
    // Prevent the default form submission behavior (if the button is inside a form)
    event.preventDefault();

    // Get input values
    const serviceID = document.getElementById('service-provider').value;
    const meterNumber = document.getElementById('meter-number').value;
    const meterType = document.getElementById('meter-type').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const amount = document.getElementById('amount').value;

    // Check if all fields are filled
    if (serviceID && meterNumber && meterType && phoneNumber && amount) {
        // If all fields are filled, prepare data to send
        const formData = new FormData();
        formData.append('serviceID', serviceID);
        formData.append('meter_number', meterNumber);
        formData.append('meter_type', meterType);
        formData.append('phone', phoneNumber);
        formData.append('amount', amount);

        // Disable the button or show a loading message to prevent repeated clicks
        document.getElementById('pay-electricity-btn').disabled = true;
        document.getElementById('pay-electricity-btn').innerText = 'Processing...';

        // Send the data to the server via fetch
        fetch('/billPayments/pay-electricity/', {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Payment failed.');
                    });
                }
                // Redirect to success page on success
                window.location.href = '/billPayments/subscription-success/';
            })
            .catch(error => {
                console.error('Payment error:', error);

                // Re-enable the button if there was an error and show the error message
                document.getElementById('pay-electricity-btn').disabled = false;
                document.getElementById('pay-electricity-btn').innerText = 'Try Again';

                alert(`Error: ${error.message}`);
            });
    } else {
        // Show alert only if required fields are missing
        alert('Please fill in all fields.');
    }
});