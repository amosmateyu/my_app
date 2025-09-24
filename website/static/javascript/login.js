// static/javascript/login.js

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const errorMessage = document.getElementById("errorMessage");
    const errorText = document.getElementById("errorText");
    const successMessage = document.getElementById("successMessage");
    const successText = document.getElementById("successText");
  
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault(); // Stop page reload
  
      // Get input values
     const email = document.getElementById("email").value.trim();
     const password = document.getElementById("password").value.trim();
  
      try {
       const formData = new FormData();
       formData.append("email", email);
       formData.append("password", password);
       
       const response = await fetch("/auth/", {
         method: "POST",
         body: formData, // No headers needed, Flask will read request.form
       });
  
        const data = await response.json();
  
        // Hide previous messages
        errorMessage.style.display = "none";
        successMessage.style.display = "none";
  
        if (data.status === "error") {
          errorText.textContent = data.message;
          errorMessage.style.display = "block";
        } else if (data.status === "success") {
          successText.textContent = data.message;
          successMessage.style.display = "block"; 
           // Redirect to home after short delay
 setTimeout(() => {
    window.location.href = "/home/";
}, 1000); 
          
        }
      } catch (err) {
        console.error("Login error:", err);
        errorText.textContent = "Something went wrong. Please try again.";
        errorMessage.style.display = "block";
      }
    });
  });
  