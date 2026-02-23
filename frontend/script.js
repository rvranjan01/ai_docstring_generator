async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const resultDiv = document.getElementById("result");

    if (!fileInput.files.length) {
        alert("Please select a file");
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            resultDiv.innerHTML = `<p style="color:red;">${data.detail}</p>`;
            return;
        }

        displayResults(data);

    } catch (error) {
        resultDiv.innerHTML = "<p style='color:red;'>Error connecting to server</p>";
    }
}


function displayResults(data) {
    const resultDiv = document.getElementById("result");

    let output = `<h3>File: ${data.filename}</h3>`;

    data.functions_found.forEach(func => {
        output += `
            <div style="border:1px solid #ccc; padding:10px; margin:10px 0;">
                <strong>Function:</strong> ${func.function_name}<br>
                <strong>Parameters:</strong> ${func.parameters.join(", ") || "None"}<br>
                <strong>Generated Docstring:</strong>
                <pre>${func.docstring}</pre>
            </div>
        `;
    });

    resultDiv.innerHTML = output;
}