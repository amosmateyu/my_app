document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");

    logoutBtn.addEventListener("click", async () => {
        
            const response = await fetch("/auth/logout", {
                method: "POST",  // match Flask route
                headers: { "Content-Type": "application/json" }
            });

            const data = await response.json();

            if (data.status === "success") {
                window.location.href = "/auth/";

            } 
              
    
    });
});
