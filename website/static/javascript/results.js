document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Fetch data from your backend API
        const response = await fetch("/patient/recent_patient");
        const resultData = await response.json();

        // Populate Risk Summary
        document.getElementById("riskLevel").innerText = resultData.risk_level;
       // document.getElementById("riskDescription").innerText = resultData.riskDescription;
        document.getElementById("probability").innerText = "Probability: " + resultData.probability;

        // Assume resultData has risk_level and probability
        const riskLevel = resultData.risk_level;         // "High Risk"
        const probability = resultData.probability;      // "100.00%"

// Build user-friendly sentence
        const riskSentence = `Based on your health information, your 10-year heart disease risk is classified as ${riskLevel} with a probability of ${probability}. Please consult your doctor for personalized advice.`;
           // Risk reason
        const riskReason = `The ${riskLevel.toLowerCase()} is because of your top risk factors. Based on these, here are personalized recommendations:`;
// Display in a div
document.getElementById("riskDescription").innerText = riskSentence;
document.getElementById("recommendationIntro").innerText = riskReason;


        // Populate Recommendation Intro
     //   document.getElementById("recommendationIntro").innerText = resultData.recommendationsIntro;

        // Feature label mapping (same as backend)
        const featureLabelMap = {
            "high_blood_pressure": "Blood Pressure",
            "high_cholesterol_level": "Cholesterol Level",
            "has_diabetes": "Diabetes Status",
            "has_obesity": "Obesity",
            "sedentary_lifestyle": "Activity Level",
            "family_history_of_heart_disease": "Family History of Heart Disease",
            "chronic_stress_level": "Stress Level",
            "smoking_habit": "Smoking Habit",
            "age_in_years": "Age",
            "gender_identity": "Gender"
        };

        // Populate Recommendation Table dynamically
        const tableBody = document.getElementById("recommendationTableBody");
        tableBody.innerHTML = ""; // Clear existing rows

        for (const factor in resultData.recommendations) {
            const row = document.createElement("tr");

            const factorCell = document.createElement("td");
            factorCell.className = "factor";

            // Use mapping to get readable label
            factorCell.innerText = featureLabelMap[factor] || factor.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

            const recommendationCell = document.createElement("td");
            recommendationCell.innerText = resultData.recommendations[factor];

            row.appendChild(factorCell);
            row.appendChild(recommendationCell);

            tableBody.appendChild(row);
        }

    } catch (error) {
        console.error("Error fetching result data:", error);
        // Optionally show an error message to the user
    }
});
