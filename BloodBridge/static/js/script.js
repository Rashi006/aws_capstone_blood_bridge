
document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash messages after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 4000);
    });

    // Password Confirmation Validation (if applicable)
    const signupForm = document.querySelector('form[action="/signup"]');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            // If we had a confirm password field, we'd check it here.
            // But the simple requirement was just name/email/role/password.
            // We can check strictly if fields are filled (HTML5 does this mostly).
        });
    }
});
