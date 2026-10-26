
document.getElementById("studentForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const student = {
        first_name: document.getElementById("firstName").value.trim(),
        last_name: document.getElementById("lastName").value.trim(),
        roll_number: document.getElementById("rollNumber").value,
        department: document.getElementById("department").value.trim()
    };

    try {
        const response = await fetch("/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        const result = await response.json();

        document.getElementById("message").textContent = result.message;

    } catch (error) {
        document.getElementById("message").textContent =
            "Could not connect to the Python server.";
    }
});
