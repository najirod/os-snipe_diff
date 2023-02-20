function submitSelection(event) {
    event.preventDefault();
    var selected_user = document.getElementById("floatingSelect").value;

    $.ajax({
        url: "/submit-user",
        type: "POST",
        data: { "selected_user": selected_user },
        success: function(response) {
            // Do something with the server response
            console.log(response);
            var asset_list = document.getElementById("floatingSelect1")
            asset_list.innerHTML = response;
            $('#floatingSelect').prop('disabled', 'disabled');
        }
    });
}

function createDocument(event) {
    event.preventDefault();
    var selected_user = document.getElementById("floatingSelect").value;
    var selected_assets = $('#floatingSelect1').val();
    var statement_type_option = document.getElementById("floatingSelect2").value;
    console.log(selected_assets)

    $.ajax({
        url: "/create-document",
        type: "POST",
        data: {
            "selected_user": selected_user,
            "selected_assets": selected_assets,
            "statement_type_option": statement_type_option,
        },
        success: function(response) {
            // Create a temporary link to the PDF file
            var link = document.createElement('a');
            link.href = URL.createObjectURL(response);
            link.target = '_blank';
            link.style.display = 'none';
            document.body.appendChild(link);

            // Simulate a click on the link to download the file
            link.click();

            // Remove the link from the document
            document.body.removeChild(link);
        },
        xhrFields: {
            responseType: 'blob'
        }
    });
}