document.getElementById("download").addEventListener("click", async (e) => {
    e.preventDefault();

    try {
        const response = await fetch("/report/download_excel", { method: "GET" });
        if (!response.ok) throw new Error("Failed to download Excel file");

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "patients_data.xlsx";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error("Error downloading Excel file:", error);
        alert("Failed to download Excel file. Please try again.");
    }
});
