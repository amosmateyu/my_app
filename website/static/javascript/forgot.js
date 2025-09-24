document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("forgotPasswordForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("new_password"); // ✅ fixed

    const errorDiv = document.getElementById("errorMessage");
    const errorText = document.getElementById("errorText");

    const successDiv = document.getElementById("successMessage");
    const successText = document.getElementById("successText");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        errorDiv.style.display = "none";
        successDiv.style.display = "none";

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        try {
            const response = await fetch("/auth/forgot-password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (data.status === "error") {
                errorText.textContent = data.message;
                errorDiv.style.display = "block";
            } else if (data.status === "success") {
                successText.textContent = data.message;
                successDiv.style.display = "block";

                setTimeout(() => {
                    window.location.href = "/auth/"; // goes back to login page
                }, 1000); // give user time to see success message
            }
        } catch (err) {
            errorText.textContent = "Unexpected error occurred.";
            errorDiv.style.display = "block";
        }
    });
});
