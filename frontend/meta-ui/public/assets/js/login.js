/**
 * Meta Portal - Login Page JavaScript
 * Phase 2.1: Enhanced Login with Validation and Professional UI
 */

// ==================== Email Validation ====================
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// ==================== Input Validation UI ====================
function validateInput(input, isValid, errorMessage = '') {
  const wrapper = input.closest('.input-group-custom');
  const errorDiv = wrapper.querySelector('.error-message');
  const validIcon = wrapper.querySelector('.bi-check-circle-fill');
  const invalidIcon = wrapper.querySelector('.bi-x-circle-fill');
  
  if (isValid) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
    errorDiv.classList.remove('show');
    validIcon.classList.add('valid');
    invalidIcon.classList.remove('invalid');
  } else {
    input.classList.remove('is-valid');
    input.classList.add('is-invalid');
    if (errorMessage) {
      errorDiv.textContent = errorMessage;
    }
    errorDiv.classList.add('show');
    validIcon.classList.remove('valid');
    invalidIcon.classList.add('invalid');
  }
}

function clearValidation(input) {
  const wrapper = input.closest('.input-group-custom');
  const errorDiv = wrapper.querySelector('.error-message');
  const validIcon = wrapper.querySelector('.bi-check-circle-fill');
  const invalidIcon = wrapper.querySelector('.bi-x-circle-fill');
  
  input.classList.remove('is-valid', 'is-invalid');
  errorDiv.classList.remove('show');
  validIcon.classList.remove('valid');
  invalidIcon.classList.remove('invalid');
}

// ==================== Alert Messages ====================
function showAlert(message, type = 'danger') {
  const alertDiv = document.getElementById('alertMessage');
  alertDiv.className = `alert alert-custom alert-${type} show`;
  alertDiv.innerHTML = `
    <i class="bi bi-${type === 'success' ? 'check-circle-fill' : 'exclamation-circle-fill'} me-2"></i>
    ${message}
  `;
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    alertDiv.classList.remove('show');
  }, 5000);
}

function hideAlert() {
  const alertDiv = document.getElementById('alertMessage');
  alertDiv.classList.remove('show');
}

// ==================== Real-time Validation ====================
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

// Email validation on blur
emailInput.addEventListener('blur', function() {
  const email = this.value.trim();
  if (email === '') {
    validateInput(this, false, 'Email address is required');
  } else if (!isValidEmail(email)) {
    validateInput(this, false, 'Please enter a valid email address');
  } else {
    validateInput(this, true);
  }
});

// Email validation on input (clear errors when typing)
emailInput.addEventListener('input', function() {
  const email = this.value.trim();
  if (email === '') {
    clearValidation(this);
  } else if (isValidEmail(email)) {
    validateInput(this, true);
  }
});

// Password validation on blur
passwordInput.addEventListener('blur', function() {
  const password = this.value;
  if (password === '') {
    validateInput(this, false, 'Password is required');
  } else if (password.length < 6) {
    validateInput(this, false, 'Password must be at least 6 characters');
  } else {
    validateInput(this, true);
  }
});

// Password validation on input (clear errors when typing)
passwordInput.addEventListener('input', function() {
  const password = this.value;
  if (password === '') {
    clearValidation(this);
  } else if (password.length >= 6) {
    validateInput(this, true);
  }
});

// ==================== Remember Me Functionality ====================
const rememberMeCheckbox = document.getElementById('rememberMe');

// Load saved email if "Remember Me" was checked previously
window.addEventListener('DOMContentLoaded', function() {
  const savedEmail = localStorage.getItem('rememberedEmail');
  const rememberMeStatus = localStorage.getItem('rememberMe');
  
  if (savedEmail && rememberMeStatus === 'true') {
    emailInput.value = savedEmail;
    rememberMeCheckbox.checked = true;
    validateInput(emailInput, true);
  }
});

// ==================== Forgot Password Modal ====================
const forgotPasswordLink = document.getElementById('forgotPasswordLink');
const forgotPasswordModal = new bootstrap.Modal(document.getElementById('forgotPasswordModal'));

forgotPasswordLink.addEventListener('click', function(e) {
  e.preventDefault();
  forgotPasswordModal.show();
});

// Forgot Password Form Submission
document.getElementById('forgotPasswordForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const resetEmail = document.getElementById('resetEmail').value.trim();
  
  if (!isValidEmail(resetEmail)) {
    alert('Please enter a valid email address');
    return;
  }
  
  // Simulate password reset (replace with actual API call)
  showAlert('Password reset link has been sent to your email!', 'success');
  forgotPasswordModal.hide();
  document.getElementById('forgotPasswordForm').reset();
});

// ==================== Form Submission ====================
const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const loginBtnText = document.getElementById('loginBtnText');
const loginBtnIcon = document.getElementById('loginBtnIcon');
const loginSpinner = document.getElementById('loginSpinner');

loginForm.addEventListener('submit', async function(e) {
  e.preventDefault();
  
  // Hide any existing alerts
  hideAlert();
  
  // Get form values
  const email = emailInput.value.trim();
  const password = passwordInput.value;
  const rememberMe = rememberMeCheckbox.checked;
  
  // Validate inputs
  let isValid = true;
  
  if (email === '') {
    validateInput(emailInput, false, 'Email address is required');
    isValid = false;
  } else if (!isValidEmail(email)) {
    validateInput(emailInput, false, 'Please enter a valid email address');
    isValid = false;
  } else {
    validateInput(emailInput, true);
  }
  
  if (password === '') {
    validateInput(passwordInput, false, 'Password is required');
    isValid = false;
  } else if (password.length < 6) {
    validateInput(passwordInput, false, 'Password must be at least 6 characters');
    isValid = false;
  } else {
    validateInput(passwordInput, true);
  }
  
  if (!isValid) {
    return;
  }
  
  // Show loading state
  loginBtn.disabled = true;
  loginBtnText.textContent = 'Signing in...';
  loginBtnIcon.style.display = 'none';
  loginSpinner.style.display = 'inline-block';
  
  try {
    // API call
    const response = await fetch('http://localhost:8000/api/users/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
      const result = await response.json();
      
      // Save token and user info
      localStorage.setItem('token', result.access_token);
      localStorage.setItem('userEmail', email);
      
      // Try to fetch user's full name from the API (if available)
      // For now, we'll extract from email
      const userName = email.split('@')[0];
      localStorage.setItem('userName', userName);
      
      // Handle "Remember Me"
      if (rememberMe) {
        localStorage.setItem('rememberedEmail', email);
        localStorage.setItem('rememberMe', 'true');
      } else {
        localStorage.removeItem('rememberedEmail');
        localStorage.removeItem('rememberMe');
      }
      
      // Show success message
      showAlert('Login successful! Redirecting...', 'success');
      
      // Redirect after short delay
      setTimeout(() => {
        window.location.href = 'jobs.html';
      }, 1000);
      
    } else {
      const error = await response.json();
      showAlert(error.detail || 'Invalid email or password. Please try again.', 'danger');
      
      // Reset button state
      loginBtn.disabled = false;
      loginBtnText.textContent = 'Sign In';
      loginBtnIcon.style.display = 'inline-block';
      loginSpinner.style.display = 'none';
    }
    
  } catch (error) {
    console.error('Login error:', error);
    showAlert('Unable to connect to server. Please try again later.', 'danger');
    
    // Reset button state
    loginBtn.disabled = false;
    loginBtnText.textContent = 'Sign In';
    loginBtnIcon.style.display = 'inline-block';
    loginSpinner.style.display = 'none';
  }
});
