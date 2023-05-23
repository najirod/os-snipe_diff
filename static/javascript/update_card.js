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


function submitSelection(event) {
    event.preventDefault();
    var selected_user = document.getElementById("floatingSelect").value;
    $('#loading-spinner').show();

    $.ajax({
        url: "/submit-user",
        type: "POST",
        data: { "selected_user": selected_user,
                "for_cards": "True" },
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


function select_card(){
    var selected_card = $('#floatingSelect1').val();
    var selected_hex = selected_card[0].split(',')[0];
    var selected_dec = selected_card[0].split(',')[1];
    
    console.log(selected_card);
    console.log(selected_hex);
    console.log(selected_dec)
    hex_input.value = selected_hex;
    dec_input.value = selected_dec;



}