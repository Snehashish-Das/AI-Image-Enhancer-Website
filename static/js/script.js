document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const progressContainer = document.getElementById("progressContainer");
    const progressBar = document.getElementById("progressBar");
    const resultContainer = document.getElementById("resultContainer");
    const originalImage = document.getElementById("originalImage");
    const enhancedImage = document.getElementById("enhancedImage");
    const viewOriginal = document.getElementById("viewOriginal");
    const viewEnhanced = document.getElementById("viewEnhanced");
    const downloadEnhanced = document.getElementById("downloadEnhanced");

    // Hide progress and result containers initially
    progressContainer.classList.add("hidden");
    resultContainer.classList.add("hidden");

    uploadForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        if (fileInput.files.length === 0) {
            alert("Please select an image file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // Show progress bar and hide result container
        progressContainer.classList.remove("hidden");
        resultContainer.classList.add("hidden");

        // Start the progress bar animation
        progressBar.style.width = "0%";

        try {
            // Make AJAX request to upload and enhance the image
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                const { original_filename, enhanced_filename } = result;

                // Set URLs for original and enhanced images
                originalImage.src = `/static/uploads/${original_filename}`;
                enhancedImage.src = `/static/results/${enhanced_filename}`;
                viewOriginal.href = originalImage.src;
                viewEnhanced.href = enhancedImage.src;
                downloadEnhanced.href = enhancedImage.src;

                // Show result container and hide progress bar
                resultContainer.classList.remove("hidden");
                progressContainer.classList.add("hidden");
            } else {
                alert("Image enhancement failed. Please try again.");
                progressContainer.classList.add("hidden");
            }
        } catch (error) {
            alert("An error occurred while uploading the image.");
            progressContainer.classList.add("hidden");
        }
    });
});
