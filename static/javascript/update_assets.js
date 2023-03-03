function createTable() {
    // Get the input data for column 1
    const inputData = document.getElementById("inputData").value.trim();

    // Split the input data into an array of values
    const values = inputData.split("\n");

    // Get the input data for column 2
    const inputData2 = document.getElementById("inputData2").value.trim();

    // Split the input data for column 2 into an array of values
    const values2 = inputData2.split("\n");

    // Get the table body
    const tableBody = document.getElementById("tableBody");

    // Clear the table body
    tableBody.innerHTML = "";

    // Loop through the values and create a row for each value
    for (let i = 0; i < values.length; i++) {
        // Create a new row
        const row = document.createElement("tr");

        // Create two cells and add the values to them
        const cell1 = document.createElement("td");
        cell1.textContent = values[i] || "";
        if (cell1.textContent === "") {
        console.log("empty str");
    }

        const cell2 = document.createElement("td");
        cell2.textContent = values2[i] || "";
        if (cell2.textContent === "") {
        console.log("empty str");
    }

        // Add the cells to the row
        row.appendChild(cell1);
        row.appendChild(cell2);

        // Add the row to the table body
        tableBody.appendChild(row);
    }
}

function postData() {
  // Get the table body
  const tableBody = document.getElementById("tableBody");

  // Get the rows from the table body
  const rows = tableBody.getElementsByTagName("tr");

  // Create an array to hold the data
  const data = [];

  // Loop through the rows and add the data to the array
  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName("td");
    data.push({
      "asset_tag": cells[0].textContent.trim(),
      "os_number": cells[1].textContent.trim()
    });
  }

  // Create a new XMLHttpRequest object
  const xhr = new XMLHttpRequest();

  // Set the URL for the request
  const url = "/update-assets";

  // Set the HTTP method to POST
  xhr.open("POST", url);

  // Set the Content-Type header
  xhr.setRequestHeader("Content-Type", "application/json");

  // Define a callback function to handle the response
  xhr.onload = function () {
    if (xhr.status === 200) {
      console.log(xhr.responseText);
      alert(xhr.responseText)
    } else {
      alert("An error occurred while posting the data.");
    }
  };

  // Convert the data to JSON format
  const json = JSON.stringify(data);

  // Send the request with the JSON data
  xhr.send(json);
}
