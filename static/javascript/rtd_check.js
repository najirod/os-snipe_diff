function post_data() {
    $('#loading-spinner').show();
    const input_data = document.getElementById("inputData").value.trim().split("\n");
    console.log(input_data);
    console.log(typeof input_data);

    $.ajax({
        url: "/rtd_check",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "os_numbers": input_data }),
        xhrFields: {
            responseType: 'blob' // Set the response type to blob
        },
        success: function(response) {
            var url = window.URL.createObjectURL(response);

            var link = document.createElement('a');
            link.href = url;
            link.target = '_blank';
            link.download = 'non_rtd_assets.xlsx'; // Set the desired file name

            link.click();

            window.URL.revokeObjectURL(url);

            $('#loading-spinner').hide();
        }
    });
}
