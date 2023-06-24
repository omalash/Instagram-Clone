$(document).ready(function () {
	let passwordInput = $("#password-input");
	let lengthIndicator = $("#length-indicator");
	let uppercaseIndicator = $("#uppercase-indicator");
	let lowercaseIndicator = $("#lowercase-indicator");
	let numberIndicator = $("#number-indicator");
	let specialCharIndicator = $("#special-char-indicator");

	// Function to update password indicators
	function updateIndicators() {
		let password = passwordInput.val();

		lengthIndicator.text(password.length >= 8 ? "✓" : "✗");
		uppercaseIndicator.text(/[A-Z]/.test(password) ? "✓" : "✗");
		lowercaseIndicator.text(/[a-z]/.test(password) ? "✓" : "✗");
		numberIndicator.text(/\d/.test(password) ? "✓" : "✗");
		specialCharIndicator.text(/[!@#\$%\^&\*\(\)\.]/.test(password) ? "✓" : "✗");
	}

	updateIndicators();
	passwordInput.on("input", updateIndicators);
});
