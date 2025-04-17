// Auto-hide flash messages after 4 seconds
document.addEventListener("DOMContentLoaded", () => {
    const flash = document.querySelector(".flash-message");
    if (flash) {
        setTimeout(() => flash.style.display = "none", 4000);
    }
});
document.querySelector('form').addEventListener('submit', function(e) {
    const password = document.getElementById('password').value;
    const strongRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!strongRegex.test(password)) {
        alert("❌ Password must be 8+ chars, include uppercase, number, and special character.");
        e.preventDefault();
    }
});


