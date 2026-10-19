document.addEventListener("DOMContentLoaded", function () {
    const yearEl = document.getElementById("current-year");
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }
});
