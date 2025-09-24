document.addEventListener("DOMContentLoaded", () => {
    const predictionForm = document.getElementById("predictionForm");

    predictionForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // prevent default form submission
        const encodedData = {
            //add them here
            first_name: document.getElementById("first_name").value.trim(),
            last_name: document.getElementById("last_name").value.trim(),
            age_in_years: parseInt(document.getElementById("age").value),
            gender_identity: document.getElementById("gender").value === "male" ? 1 : 0,
            high_blood_pressure: document.getElementById("bp").value === "yes" ? 1 : 0,
            high_cholesterol_level: document.getElementById("cholesterol").value === "yes" ? 1 : 0,
            has_diabetes: document.getElementById("diabetes").value === "yes" ? 1 : 0,
            has_obesity: document.getElementById("obesity").value === "yes" ? 1 : 0,
            sedentary_lifestyle: document.getElementById("sedentary_lifestyle").value === "yes" ? 1 : 0,
            family_history_of_heart_disease: document.getElementById("family_history").value === "yes" ? 1 : 0,
            chronic_stress_level: document.getElementById("chronic_stress").value === "yes" ? 1 : 0,
            smoking_habit: document.getElementById("smoking").value === "yes" ? 1 : 0
        };
        

        try {
            const response = await fetch("/predict/result", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(encodedData)
            });

            const data = await response.json();

            if (data.status === "success") {
               
    
                window.location.href = "/home/results";

            } else {
                alert(data.message || "Error sending data.");
            }

        } catch (err) {
            console.error(err);
            alert("Failed to send prediction. Try again.");
        }
    });
});
