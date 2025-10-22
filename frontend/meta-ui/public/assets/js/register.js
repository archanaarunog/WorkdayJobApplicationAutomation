// Register Page - Full Validation & Password Strength

// Helper function to validate email format
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Helper function to validate phone number (US format)
function isValidPhone(phone) {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');
  // Check if it's 10 digits (US format)
  return cleaned.length === 10 || cleaned.length === 11;
}

// Helper function to validate name (min 2 chars, letters only)
function isValidName(name) {
  return name.length >= 2 && /^[a-zA-Z\s'-]+$/.test(name);
}

// Password strength calculation
function calculatePasswordStrength(password) {
  const requirements = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
  };
  
  const metCount = Object.values(requirements).filter(Boolean).length;
  
  let strength = 'weak';
  if (metCount === 5) strength = 'strong';
  else if (metCount >= 4) strength = 'good';
  else if (metCount >= 3) strength = 'fair';
  
  return { requirements, strength, metCount };
}

// Update password strength meter
function updatePasswordStrength(password) {
  const meter = document.getElementById('passwordStrengthMeter');
  const fill = document.getElementById('strengthFill');
  const text = document.getElementById('strengthText');
  
  if (!password) {
    meter.classList.remove('show');
    return;
  }
  
  meter.classList.add('show');
  
  const { requirements, strength } = calculatePasswordStrength(password);
  
  // Update bar
  fill.className = 'strength-fill ' + strength;
  
  // Update text
  text.className = 'strength-text ' + strength;
  const strengthLabels = {
    weak: 'Weak Password',
    fair: 'Fair Password',
    good: 'Good Password',
    strong: 'Strong Password'
  };
  text.textContent = strengthLabels[strength];
  
  // Update requirements checklist
  document.getElementById('req-length').classList.toggle('met', requirements.length);
  document.getElementById('req-uppercase').classList.toggle('met', requirements.uppercase);
  document.getElementById('req-lowercase').classList.toggle('met', requirements.lowercase);
  document.getElementById('req-number').classList.toggle('met', requirements.number);
  document.getElementById('req-special').classList.toggle('met', requirements.special);
}

// Validate input and show visual feedback
function validateInput(input, isValid, errorMessage = '') {
  const wrapper = input.closest('.input-icon-wrapper');
  const errorDiv = input.parentElement.nextElementSibling;
  
  if (wrapper) {
    const validIcon = wrapper.querySelector('.bi-check-circle-fill');
    const invalidIcon = wrapper.querySelector('.bi-x-circle-fill');
    
    if (isValid) {
      input.classList.remove('is-invalid');
      input.classList.add('is-valid');
      if (validIcon) validIcon.classList.add('valid');
      if (invalidIcon) invalidIcon.classList.remove('invalid');
      if (errorDiv && errorDiv.classList.contains('error-message')) {
        errorDiv.classList.remove('show');
      }
    } else {
      input.classList.remove('is-valid');
      input.classList.add('is-invalid');
      if (validIcon) validIcon.classList.remove('valid');
      if (invalidIcon) invalidIcon.classList.add('invalid');
      if (errorDiv && errorDiv.classList.contains('error-message')) {
        if (errorMessage) errorDiv.textContent = errorMessage;
        errorDiv.classList.add('show');
      }
    }
  }
}

// Clear validation state
function clearValidation(input) {
  const wrapper = input.closest('.input-icon-wrapper');
  const errorDiv = input.parentElement.nextElementSibling;
  
  input.classList.remove('is-valid', 'is-invalid');
  
  if (wrapper) {
    const validIcon = wrapper.querySelector('.bi-check-circle-fill');
    const invalidIcon = wrapper.querySelector('.bi-x-circle-fill');
    if (validIcon) validIcon.classList.remove('valid');
    if (invalidIcon) invalidIcon.classList.remove('invalid');
  }
  
  if (errorDiv && errorDiv.classList.contains('error-message')) {
    errorDiv.classList.remove('show');
  }
}

// Show alert message
function showAlert(message, type = 'success') {
  const alertDiv = document.getElementById('alertMessage');
  alertDiv.className = `alert alert-custom alert-${type} show`;
  alertDiv.textContent = message;
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    hideAlert();
  }, 5000);
}

// Hide alert message
function hideAlert() {
  const alertDiv = document.getElementById('alertMessage');
  alertDiv.classList.remove('show');
}

// Check if all validations pass
function checkFormValidity() {
  const firstName = document.getElementById('first_name').value.trim();
  const lastName = document.getElementById('last_name').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const termsAccepted = document.getElementById('termsAccepted').checked;
  
  const { strength } = calculatePasswordStrength(password);
  const passwordStrong = strength === 'good' || strength === 'strong';
  
  const isValid = 
    isValidName(firstName) &&
    isValidName(lastName) &&
    isValidEmail(email) &&
    isValidPhone(phone) &&
    password.length >= 8 &&
    passwordStrong &&
    password === confirmPassword &&
    termsAccepted;
  
  document.getElementById('registerBtn').disabled = !isValid;
}

// DOM Elements
const firstNameInput = document.getElementById('first_name');
const lastNameInput = document.getElementById('last_name');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const termsCheckbox = document.getElementById('termsAccepted');
const registerForm = document.getElementById('registerForm');

// First Name validation
firstNameInput.addEventListener('blur', function() {
  const value = this.value.trim();
  if (value) {
    const isValid = isValidName(value);
    validateInput(this, isValid, isValid ? '' : 'Please enter a valid first name (min 2 characters)');
  }
  checkFormValidity();
});

firstNameInput.addEventListener('input', function() {
  if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
    const value = this.value.trim();
    if (value) {
      const isValid = isValidName(value);
      validateInput(this, isValid, isValid ? '' : 'Please enter a valid first name (min 2 characters)');
    }
  }
  checkFormValidity();
});

// Last Name validation
lastNameInput.addEventListener('blur', function() {
  const value = this.value.trim();
  if (value) {
    const isValid = isValidName(value);
    validateInput(this, isValid, isValid ? '' : 'Please enter a valid last name (min 2 characters)');
  }
  checkFormValidity();
});

lastNameInput.addEventListener('input', function() {
  if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
    const value = this.value.trim();
    if (value) {
      const isValid = isValidName(value);
      validateInput(this, isValid, isValid ? '' : 'Please enter a valid last name (min 2 characters)');
    }
  }
  checkFormValidity();
});

// Email validation
emailInput.addEventListener('blur', function() {
  const value = this.value.trim();
  if (value) {
    const isValid = isValidEmail(value);
    validateInput(this, isValid, isValid ? '' : 'Please enter a valid email address');
  }
  checkFormValidity();
});

emailInput.addEventListener('input', function() {
  if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
    const value = this.value.trim();
    if (value) {
      const isValid = isValidEmail(value);
      validateInput(this, isValid, isValid ? '' : 'Please enter a valid email address');
    }
  }
  checkFormValidity();
});

// Phone validation
phoneInput.addEventListener('blur', function() {
  const value = this.value.trim();
  if (value) {
    const isValid = isValidPhone(value);
    validateInput(this, isValid, isValid ? '' : 'Please enter a valid 10-digit phone number');
  }
  checkFormValidity();
});

phoneInput.addEventListener('input', function() {
  if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
    const value = this.value.trim();
    if (value) {
      const isValid = isValidPhone(value);
      validateInput(this, isValid, isValid ? '' : 'Please enter a valid 10-digit phone number');
    }
  }
  checkFormValidity();
});

// Password validation with strength meter
passwordInput.addEventListener('input', function() {
  const password = this.value;
  updatePasswordStrength(password);
  
  if (password) {
    const { strength } = calculatePasswordStrength(password);
    const isValid = password.length >= 8 && (strength === 'good' || strength === 'strong');
    validateInput(this, isValid, isValid ? '' : 'Password must meet the requirements below');
  }
  
  // Also validate confirm password if it has value
  if (confirmPasswordInput.value) {
    const passwordsMatch = password === confirmPasswordInput.value;
    validateInput(confirmPasswordInput, passwordsMatch, passwordsMatch ? '' : 'Passwords do not match');
  }
  
  checkFormValidity();
});

passwordInput.addEventListener('blur', function() {
  const password = this.value;
  if (password) {
    const { strength } = calculatePasswordStrength(password);
    const isValid = password.length >= 8 && (strength === 'good' || strength === 'strong');
    validateInput(this, isValid, isValid ? '' : 'Password must meet the requirements below');
  }
  checkFormValidity();
});

// Confirm Password validation
confirmPasswordInput.addEventListener('input', function() {
  const password = passwordInput.value;
  const confirmPassword = this.value;
  
  if (confirmPassword) {
    const passwordsMatch = password === confirmPassword;
    validateInput(this, passwordsMatch, passwordsMatch ? '' : 'Passwords do not match');
  }
  
  checkFormValidity();
});

confirmPasswordInput.addEventListener('blur', function() {
  const password = passwordInput.value;
  const confirmPassword = this.value;
  
  if (confirmPassword) {
    const passwordsMatch = password === confirmPassword;
    validateInput(this, passwordsMatch, passwordsMatch ? '' : 'Passwords do not match');
  }
  
  checkFormValidity();
});

// Terms checkbox
termsCheckbox.addEventListener('change', function() {
  checkFormValidity();
});

// Prevent terms links from navigating
document.getElementById('termsLink').addEventListener('click', function(e) {
  e.preventDefault();
  // In future, open terms modal
  alert('Terms of Service will be displayed here');
});

document.getElementById('privacyLink').addEventListener('click', function(e) {
  e.preventDefault();
  // In future, open privacy modal
  alert('Privacy Policy will be displayed here');
});

// Form submission
registerForm.addEventListener('submit', async function(e) {
  e.preventDefault();
  hideAlert();
  
  // Get all form values
  const firstName = firstNameInput.value.trim();
  const lastName = lastNameInput.value.trim();
  const email = emailInput.value.trim();
  const phone = phoneInput.value.trim();
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;
  const termsAccepted = termsCheckbox.checked;
  
  // Final validation
  let isValid = true;
  
  if (!isValidName(firstName)) {
    validateInput(firstNameInput, false, 'Please enter a valid first name (min 2 characters)');
    isValid = false;
  }
  
  if (!isValidName(lastName)) {
    validateInput(lastNameInput, false, 'Please enter a valid last name (min 2 characters)');
    isValid = false;
  }
  
  if (!isValidEmail(email)) {
    validateInput(emailInput, false, 'Please enter a valid email address');
    isValid = false;
  }
  
  if (!isValidPhone(phone)) {
    validateInput(phoneInput, false, 'Please enter a valid 10-digit phone number');
    isValid = false;
  }
  
  const { strength } = calculatePasswordStrength(password);
  const passwordStrong = strength === 'good' || strength === 'strong';
  
  if (!password || password.length < 8 || !passwordStrong) {
    validateInput(passwordInput, false, 'Password must meet the requirements below');
    isValid = false;
  }
  
  if (password !== confirmPassword) {
    validateInput(confirmPasswordInput, false, 'Passwords do not match');
    isValid = false;
  }
  
  if (!termsAccepted) {
    showAlert('Please accept the Terms of Service and Privacy Policy', 'danger');
    isValid = false;
  }
  
  if (!isValid) {
    return;
  }
  
  // Show loading state
  const registerBtn = document.getElementById('registerBtn');
  const registerBtnText = document.getElementById('registerBtnText');
  const registerBtnIcon = document.getElementById('registerBtnIcon');
  const registerSpinner = document.getElementById('registerSpinner');
  
  registerBtn.disabled = true;
  registerBtnText.textContent = 'Creating...';
  registerBtnIcon.style.display = 'none';
  registerSpinner.style.display = 'inline-block';
  
  try {
    const response = await fetch('http://localhost:8000/api/users/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password,
        first_name: firstName,
        last_name: lastName,
        phone: phone
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Success
      showAlert('Account created successfully! Redirecting to login...', 'success');
      
      // Clear form
      registerForm.reset();
      clearValidation(firstNameInput);
      clearValidation(lastNameInput);
      clearValidation(emailInput);
      clearValidation(phoneInput);
      clearValidation(passwordInput);
      clearValidation(confirmPasswordInput);
      document.getElementById('passwordStrengthMeter').classList.remove('show');
      
      // Redirect to login page after 2 seconds
      setTimeout(() => {
        window.location.href = 'login.html';
      }, 2000);
    } else {
      // Error from server
      showAlert(data.detail || 'Registration failed. Please try again.', 'danger');
      
      // Reset button
      registerBtn.disabled = false;
      registerBtnText.textContent = 'Create Account';
      registerBtnIcon.style.display = 'inline-block';
      registerSpinner.style.display = 'none';
    }
  } catch (error) {
    console.error('Registration error:', error);
    showAlert('Network error. Please check your connection and try again.', 'danger');
    
    // Reset button
    registerBtn.disabled = false;
    registerBtnText.textContent = 'Create Account';
    registerBtnIcon.style.display = 'inline-block';
    registerSpinner.style.display = 'none';
  }
});

// Initialize form state
checkFormValidity();
