import os
from website import create_app

# Create the Flask app
app = create_app()

# ===============================
# Dynamic port for Render
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)
