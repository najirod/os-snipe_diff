$(document).ready(function() {
    var $select = $('select#floatingSelect');
    var $options = $select.children();
    var $defaultOption = $options.first();

    $('#user-search').on('input', function() {
        var query = $(this).val().toLowerCase();
        var matchingOptions = $options.filter(function() {
            return $(this).text().toLowerCase().indexOf(query) !== -1;
        });

        $options.hide();
        matchingOptions.show();

        if (matchingOptions.length > 0) {
            $select.val(matchingOptions.first().val());
        } else {
            $select.val('');
        }
    });
});


function disableEnterKey(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        return false;
      }

      const inputChar = event.key.toLowerCase();
      const keyCode = event.keyCode || event.which; // For cross-browser compatibility
      const regex = /^[0-9a-f]$/;

      if (keyCode !== 8 && keyCode !== 46 && !regex.test(inputChar)) {
        event.preventDefault();
        return false;
      }
    }

function checkInputs() {
    const assetTagValue = document.getElementById("asset_tag").value;
    const hexInputValue = document.getElementById("hex_input").value;
    const decInputValue = document.getElementById("dec_input").value;
    const submitButton = document.getElementById("submit_button");

    if (assetTagValue.trim() !== "" && hexInputValue.trim() !== "" && decInputValue.trim() !== "") {
      submitButton.disabled = false; // Enable the button
    } else {
      submitButton.disabled = true; // Disable the button
    }
  }


function submitSelection(event) {
    event.preventDefault();
    var selected_user = document.getElementById("floatingSelect").value;
    $('#loading-spinner').show();

    $.ajax({
        url: "/submit-user",
        type: "POST",
        data: {
            "selected_user": selected_user,
            "for_cards": "True"
        },
        success: function(response) {
            // Do something with the server response
            console.log(response);
            var asset_list = document.getElementById("floatingSelect1")
            asset_list.innerHTML = response;
            $('#floatingSelect').prop('disabled', 'disabled');
            $('#user-search').prop('disabled', 'disabled');
            $('#floatingSelect').css('color', 'green');
            $('#loading-spinner').hide();
        }
    });
}


function select_card() {
    event.preventDefault();
    $('#loading-spinner').show();
    var selected_card = $('#floatingSelect1').val();
    console.log(selected_card);
    if (Array.isArray(selected_card) && selected_card.length === 0) {
  console.log("Empty list");
  alert("Nothing selected")
} else {
    var selected_asset_tag = selected_card[0].split(',')[0];
    var selected_hex = selected_card[0].split(',')[1];
    var selected_dec = selected_card[0].split(',')[2];

    console.log(selected_card);
    console.log(selected_hex);
    console.log(selected_dec)
    asset_tag.value = selected_asset_tag;
    hex_input.value = selected_hex;
    dec_input.value = selected_dec;
  
}
    
    $('#loading-spinner').hide();
}


function createDocument(event) {
    event.preventDefault();
    $('#loading-spinner').show();

    var card_data = {
        asset_tag: asset_tag.value,
        dec: dec_input.value,
        hex: hex_input.value
    };
    console.log(card_data);

    $.ajax({
        url: "/update-card",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "card_data": card_data }),
        success: function(response) {
            // Do something with the server response
            console.log(response);

            $('#loading-spinner').hide();
        }
    });

}

function calculate_dec(event) {
    event.preventDefault();
    $('#loading-spinner').show();

    let hex_input = $('#hex_input').val(); // Example input, assuming there is an input field with id "hex_input"

    let first_two_char = hex_input.substring(0, 2);

    let short_hex;
    if (first_two_char === "92" || first_two_char === "91") {
        short_hex = hex_input.substring(2);
    } else {
        alert("Wrong hex_input")
        console.log("Wrong hex_input");
        $('#loading-spinner').hide();
        return; // Exit the function if the hex_input is invalid
    }

    let dec = parseInt(short_hex, 16);
    dec_input.value = dec; 
    $('#loading-spinner').hide();
}