

document.addEventListener('DOMContentLoaded', function () {

    // Get the form element and submit button
    const header = document.getElementById("header");
    const paymentForm = document.getElementById("payment-form");
    const payButton = document.getElementById("pay-button");
    const continueButton = document.getElementById("continue");
    const backButton = document.getElementById("back");
    const informationsDiv = document.getElementById("informationsDiv");
    const paymentDiv = document.getElementById("paymentDiv");
    // Get all required input fields
    const backToCheckout = document.getElementById("back-to-checkout");
    const backToCart = document.getElementById("back-to-cart");
    const requiredFields = document.querySelectorAll('[data-required="true"]');

    // Function to check if all required fields are filled
    function checkRequiredFields() {
        const allFieldsFilled = Array.from(requiredFields).every(field => field.value.trim() !== '');
        payButton.disabled = !allFieldsFilled; // Disable the button if any required field is empty
        continueButton.disabled = !allFieldsFilled;
    }
    continueButton.addEventListener('click', function () {
        var emailInput = document.getElementById('email').value;
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput)) {
            phoneError.textContent = 'Please enter a valid email adress.';


        } else {
            phoneError.textContent = ""
            informationsDiv.style.display = "none";
            paymentDiv.style.display = "block";
            header.textContent = "Payment";
            payButton.style.display = "block";
            continueButton.style.display = "none";
            backToCart.style.display = "none";
            backToCheckout.style.display = "block";
            StripeFunction();
        }
    });
    backButton.addEventListener('click', function () {
        informationsDiv.style.display = "block";
        paymentDiv.style.display = "none";
        payButton.style.display = "none";
        continueButton.style.display = "block";
        backToCart.style.display = "block";
        header.textContent = "Checkout";
        backToCheckout.style.display = "none";

    });


    // Add event listeners to required fields
    requiredFields.forEach(field => {
        field.addEventListener('input', checkRequiredFields);
        field.addEventListener('change', checkRequiredFields);
    });

    // Add a submit event listener for the payment form
    paymentForm.addEventListener('submit', async function (event) {
        if (!payButton.disabled) {
            event.preventDefault(); // Prevent the default form submission

            // ... (previous code for stripe.confirmPayment)
        }
    });

    // Initial check for required fields on page load
    checkRequiredFields();




    let shippingRates = {};

    // Function to fetch shipping data via AJAX
    function fetchShippingRates() {
        fetch('/get_shipping_rates/')
            .then(response => response.json())
            .then(data => {
                shippingRates = data;
                // Now you have the shipping data in the shippingRates object
                console.log(shippingRates);

                // Populate the country select options
                const countrySelect = document.getElementById("country");
                for (const country in shippingRates) {
                    const option = document.createElement("option");
                    option.value = country;
                    option.text = country;
                    countrySelect.appendChild(option);
                }

                // Add an event listener to the country select to populate shipping methods
                countrySelect.addEventListener("change", updateShippingMethods);

                // Trigger the change event to initialize the shipping methods
                const event = new Event("change");
                countrySelect.dispatchEvent(event);
            })
            .catch(error => console.error('Error fetching shipping rates: ', error));
    }

    // Call the function to fetch shipping rates when the page loads
    fetchShippingRates();

    // Get the select elements and the price elements
    const countrySelect = document.getElementById("country");
    const shippingMethodSelect = document.getElementById("shipping_method");
    const priceProducts = document.getElementById("price_products");
    const priceShipping = document.getElementById("price_shipping");
    const price = document.getElementById("price");

    // Function to update the available shipping methods and total price
    function updateShippingMethods() {
        const selectedCountry = countrySelect.value;
        const methods = Object.keys(shippingRates[selectedCountry]);

        // Clear existing options in the shipping method select
        shippingMethodSelect.innerHTML = "";

        // Populate the shipping method select with options
        methods.forEach(method => {
            const option = document.createElement("option");
            option.value = method;
            option.text = method;
            shippingMethodSelect.appendChild(option);
        });

        // Trigger the change event to update the prices
        const event = new Event("change");
        shippingMethodSelect.dispatchEvent(event);
    }

    // Function to update the total price
    function updateShippingOptions() {
        const selectedCountry = countrySelect.value;
        const selectedShippingMethod = shippingMethodSelect.value;
        const selectedShippingPrice = shippingRates[selectedCountry][selectedShippingMethod];

        const productPrice = parseFloat(priceProducts.textContent, 10);



        priceShipping.textContent = selectedShippingPrice;
        price.textContent = (productPrice + selectedShippingPrice).toFixed(2);
        var payButton = document.getElementById("pay-button");



    }

    // Add event listeners to update when the shipping method changes
    shippingMethodSelect.addEventListener("change", updateShippingOptions);
    // stripe
    var elements;
    var order_number;

    var stripe = Stripe('pk_live_51OPW2eEkROwRX2XNhLDXjALxXvVlRWkwBXzE1Z8U30UjOLjeN5xDNQFYWNdD29boSvoMXM2CtKU9U2M2YPHrvyAM00ChdJkLmL');
    function StripeFunction() {

        var payButton = document.getElementById("pay-button");
        payButton.disabled = true
        var paymentForm = document.getElementById("payment-form");
        var email = document.getElementById("email").value;
        var clientSecret;
        var paymentElement;
        var paymentMethodId;


        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


        fetch('/charge/', {
            method: 'POST', headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json' // Specify the content type as JSON
            },
            body: JSON.stringify({ price: parseFloat(price.textContent, 10), customer_identifier: email })
        })
            .then(response => response.json())
            .then(data => {
                clientSecret = data.client_secret;
                order_number = data.order_number
                console.log(order_number);
                const appearance = {
                    theme: 'night',
                    labels: 'floating',
                    variables: { colorPrimaryText: '#FFFFFF' }
                };
                const options = {

                }
                setTimeout(function () {
                    payButton.disabled = false;
                }, 1000);
                elements = stripe.elements({ clientSecret, appearance });
                paymentElement = elements.create('payment', options);
                paymentElement.mount('#payment-element');


            })
            .catch(error => {
                console.error('Error fetching client secret:', error);
            });



    }

    payButton.addEventListener('click', async function () {

        payButton.disabled = true

        var formData = new FormData(document.getElementById("payment-form"));
        formData.append("order_number", order_number);


        const params = new URLSearchParams();
        for (const pair of formData.entries()) {
            params.append(pair[0], pair[1]);
        }

        // Construct the final URL
        const url = 'https://youmadclo.com/create-order/?' + params.toString();

        stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: url,

            }
        }).then(function (result) {

            if (result.error) {
                console.log("error")
                payButton.disabled = false




            }
        });




    });

});

