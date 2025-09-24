document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const defaultInput = document.getElementById("defaultPassword");

    const errorDiv = document.getElementById("errorMessage");
    const errorText = document.getElementById("errorText");

    const successDiv = document.getElementById("successMessage");
    const successText = document.getElementById("successText");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevent normal form submission

        // Hide previous messages
        errorDiv.style.display = "none";
        successDiv.style.display = "none";

        // Get values
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        

    

        try {
            const response = await fetch("/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password})
            });

            const data = await response.json();

            if (data.status === "error") {
                errorText.textContent = data.message;
                errorDiv.style.display = "block";
            } else if (data.status === "success") {
                successText.textContent = data.message;
                successDiv.style.display = "block";

                // Redirect to home after short delay
                setTimeout(() => {
                    window.location.href = "/home/";
                }, 1000);
            }

        } catch (err) {
            errorText.textContent = "Unexpected error occurred.";
            errorDiv.style.display = "block";
        }
    });
});
