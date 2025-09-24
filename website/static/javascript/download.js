
document.getElementById("downloadReportBtn").addEventListener("click", async (e) => {
    e.preventDefault(); // Prevent default link behavior

    try {
        const response = await fetch("/report/download_report", { method: "GET" });

        if (!response.ok) throw new Error("Failed to download report");

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "medical_report.pdf"; // File name for the download
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error("Error downloading medical report:", error);
        alert("Failed to download report. Please try again.");
    }
});
