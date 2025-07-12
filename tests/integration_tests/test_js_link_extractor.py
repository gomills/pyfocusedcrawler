from app.parsers.js_link_extractor.js_link_extractor import extract_links_from_js

js_minimal_test = """
// Visit https://example.com for info

const homepage = "https://homepage.com";

const api = `https://api.site.com/user/${userId}`;
"""

def test_minimal_extract_links_from_js():

    extracted_urls = extract_links_from_js(js_minimal_test)

    target_urls = [
        "https://example.com",
        "https://homepage.com",
        "https://api.site.com/user/${userId}"
        ]
    assert len(target_urls) == len(extracted_urls)

    for url in target_urls:
        assert url in extracted_urls

js_medium_test = """
// URL in a comment: https://comment-url.com

import api from "https://import-url.com/api"; // import_statement

const homepage = "https://homepage.com"; // variable_declarator

let apiEndpoint;
apiEndpoint = "https://assignment-url.com"; // assignment_expression

const userApi = `https://template-url.com/user/${userId}`; // template_string

const config = {
  endpoint: "https://pair-url.com", // pair
  docs: `https://pair-template.com/docs/${docId}` // pair with template
};

fetch("https://call-expression.com/data"); // call_expression

function getData(url = "https://default-arg.com") { // arguments
  return url;
}

const url1 = "https://binary1.com" + "https://binary2.com"; // binary_expression

// Embedded HTML string (should use regex):
const html = `
  <a href="https://html-url.com">Link</a>
  <img src="https://html-img.com/img.png" />
`;
"""




def test_medium_extract_links_from_js():

    extracted_urls = extract_links_from_js(js_medium_test)

    target_urls = [
        "https://comment-url.com",
        "https://import-url.com/api",
        "https://homepage.com",
        "https://assignment-url.com",
        "https://template-url.com/user/${userId}",
        "https://pair-url.com",
        "https://pair-template.com/docs/${docId}",
        "https://call-expression.com/data",
        "https://default-arg.com",
        "https://binary1.com",
        "https://binary2.com",
        "https://html-url.com",
        "https://html-img.com/img.png"
        ]
    
    print(extracted_urls)
    for url in target_urls:
        assert url in extracted_urls
    
    assert len(target_urls) == len(extracted_urls)

['https://comment-url.com', 
 'https://import-url.com/api', 
 'https://homepage.com', 
 'https://assignment-url.com', 
 'https://template-url.com/user/${userId}', 
 'https://pair-url.com', 
 'https://pair-template.com/docs/${docId}', 
 'https://call-expression.com/data', 'https://binary1.com', 
 'https://binary2.com', 
 '<a href="https://html-url.com">Link</a>\n  <img src="https://html-img.com/img.png" /> // Here should not extract url!'] 

    
realistic_html = """
/**************************** Prices ******************************/

// Select all price buttons by class
const priceButtons = document.querySelectorAll('.price-link');

// Add onclick event to all payments buttons
priceButtons.forEach(button => {
  button.addEventListener('click', function handleClick(event) {
      
      event.preventDefault();
    
      // Update active class
      priceButtons.forEach(priceButton => {
        priceButton.classList.remove("active");
      })
      button.classList.add("active");

      // Get payment button attributes
      let paymentMode = button.getAttribute('data-mode');
      let priceId = button.getAttribute('data-price');

      // Set payment attributes to checkout button
      const checkoutButton = document.querySelector('#stripe-checkout-button');
      checkoutButton.setAttribute('data-mode', paymentMode);
      checkoutButton.setAttribute('data-price', priceId);

      // Remove error message
      let pricesMessage = document.querySelector('#prices-message');
      pricesMessage.classList.remove("show");
  });
});

/**************************** Submit ******************************/

// Select the checkout payment button
const checkoutButton = document.querySelector('#stripe-checkout-button');

if (checkoutButton !== null) {

    // Add onclick event to checkout button
    checkoutButton.addEventListener('click', function handleClick(event) {

        event.preventDefault();
                
        let valid = true;
        
        // Get payment button attributes
        let paymentMode = checkoutButton.getAttribute('data-mode');
        let priceId = checkoutButton.getAttribute('data-price');
        let pricesMessage = document.querySelector('#prices-message');
            
        if ( empty(paymentMode) || empty(priceId) ) {
            pricesMessage.classList.add("show");
            valid = false;
        }
        else {
            pricesMessage.classList.remove("show");
        }

        // Get the TaxId value
        let taxIdInput = document.querySelector('#taxId');
        let taxId = taxIdInput.value;
        let taxidMessage = document.querySelector('#taxid-message');
            
        if ( empty(taxId) || !validateDniNif(taxId) ) {
            taxidMessage.classList.add("show");
            valid = false;
        }
        else {
            taxidMessage.classList.remove("show");
        }

        //Get the result url values
        let successUrl = checkoutButton.getAttribute('data-success-url');
        let cancelUrl = checkoutButton.getAttribute('data-cancel-url');

        // Send to stripe checkout payment page
        if (valid) {
            // Set Stripe publishable key to initialize Stripe.js
            const stripe = Stripe('pk_testjofjeisofjesiofjesaiofjesiofa');
            
            // Set loading
            setLoading(true);

            // Crear el checkout session y si ok redireccionar
            createCheckoutSession(paymentMode, priceId, taxId, successUrl, cancelUrl)
            .then(function (data) {
                if(data.sessionId) {
                    stripe
                        .redirectToCheckout({
                            sessionId: data.sessionId,
                        })
                        .then(handleResult);
                }
                else {
                    handleResult(data);
                }
            });
        }
    
    });

}
    
// Create a Checkout Session with the selected product
const createCheckoutSession = function (payment_mode, price_id, tax_id, success_url, cancel_url) {
    return fetch("https://example.com/create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            createCheckoutSession: 1,
            paymentMode: payment_mode,
            priceId: price_id,
            taxId: tax_id,
            successUrl: success_url,
            cancelUrl: cancel_url
        }),
    }).then(function (result) {
        return result.json();
    });
};

// Handle any errors returned from Checkout
const handleResult = function (result) {
    if (result.error) {
        showMessage(result.error.message);
    }
    
    setLoading(false);
};

// Show a spinner on payment processing
function setLoading(isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        checkoutButton.disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#buttonText").classList.add("hidden");
    } else {
        // Enable the button and hide spinner
        checkoutButton.disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#buttonText").classList.remove("hidden");
    }
}

// Display message
function showMessage(messageText) {
    const messageContainer = document.querySelector("#paymentResponse");
	
    messageContainer.classList.remove("hidden");
    messageContainer.textContent = messageText;
	
    setTimeout(function () {
        messageContainer.classList.add("hidden");
        messageText.textContent = "";
    }, 5000);
}

const validateDniNif = (value) => {
    let number, dni, letter;
    let expresion_regular_dni = /^[XYZ]?\d{5,8}[A-Z]$/;
    value = value.replaceAll(' ','').replaceAll('-','').replaceAll('_','').toUpperCase();
    if (expresion_regular_dni.test(value) === true) {
        number = value.substr(0, value.length - 1);
        number = number.replace('X', 0);
        number = number.replace('Y', 1);
        number = number.replace('Z', 2);
        dni = value.substr(value.length - 1, 1);
        number = number % 23;
        letter = 'FSFESFESF';
        letter = letter.substring(number, number + 1);
        if (letter != dni) {
            console.log('Wrong ID, the letter of the NIF does not correspond');
            return false;
        } else {
            console.log('Correct ID');
            return true;
        }
    }else{
        console.log('Wrong ID, invalid format');
        return false;
    }
}

function empty(str) {
  return typeof str === 'string' && str.trim().length === 0;
}"""



def test_extract_links_from_realistic_js():
    extracted_links = extract_links_from_js(realistic_html)
    expected_url = "https://example.com/create-checkout-session"
    assert extracted_links is not None
    assert expected_url in extracted_links