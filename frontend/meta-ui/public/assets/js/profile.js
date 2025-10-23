// Profile Page - User Profile Management

// Check authentication
const token = localStorage.getItem('token');
if (!token) {
  window.location.href = 'login.html';
}

// Global state
let originalProfileData = {};
let currentSkills = [];

// Initialize profile
document.addEventListener('DOMContentLoaded', function() {
  loadUserProfile();
  setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
  // Logout button
  document.getElementById('logoutBtn').addEventListener('click', logout);
  
  // Save button
  document.getElementById('saveBtn').addEventListener('click', saveProfile);
  
  // Cancel button
  document.getElementById('cancelBtn').addEventListener('click', resetForm);
  
  // Skills management
  document.getElementById('addSkillBtn').addEventListener('click', addSkill);
  document.getElementById('skillInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSkill();
    }
  });
  
  // Character counters
  document.getElementById('bio').addEventListener('input', function() {
    document.getElementById('bioCount').textContent = this.value.length;
  });
  
  document.getElementById('experience').addEventListener('input', function() {
    document.getElementById('experienceCount').textContent = this.value.length;
  });
  
  document.getElementById('education').addEventListener('input', function() {
    document.getElementById('educationCount').textContent = this.value.length;
  });
  
  // Avatar upload (placeholder)
  document.getElementById('profileAvatar').addEventListener('click', function() {
    alert('Photo upload feature coming soon!');
  });
}

// Load user profile from API
async function loadUserProfile() {
  try {
    const response = await fetch('http://localhost:8000/api/users/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const user = await response.json();
      originalProfileData = { ...user };
      populateForm(user);
      
      // Load application count
      loadApplicationCount();
    } else if (response.status === 401) {
      // Token expired
      localStorage.removeItem('token');
      window.location.href = 'login.html';
    } else {
      throw new Error('Failed to load profile');
    }
  } catch (error) {
    showAlert('Failed to load profile. Please try again.', 'danger');
  }
}

// Populate form with user data
function populateForm(user) {
  // Header
  const fullName = `${user.first_name} ${user.last_name}`;
  document.getElementById('profileName').textContent = fullName;
  document.getElementById('profileEmail').textContent = user.email;
  document.getElementById('avatarInitial').textContent = user.first_name.charAt(0).toUpperCase();
  
  // Joined date
  const joinedDate = new Date(user.created_at);
  document.getElementById('joinedDate').textContent = joinedDate.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short' 
  });
  
  // Personal Info
  document.getElementById('firstName').value = user.first_name;
  document.getElementById('lastName').value = user.last_name;
  document.getElementById('email').value = user.email;
  document.getElementById('phone').value = user.phone || '';
  document.getElementById('bio').value = user.bio || '';
  document.getElementById('bioCount').textContent = (user.bio || '').length;
  
  // Professional
  if (user.skills) {
    currentSkills = user.skills.split(',').map(s => s.trim()).filter(s => s);
    renderSkills();
  }
  document.getElementById('experience').value = user.experience || '';
  document.getElementById('experienceCount').textContent = (user.experience || '').length;
  document.getElementById('education').value = user.education || '';
  document.getElementById('educationCount').textContent = (user.education || '').length;
  
  // Links
  document.getElementById('linkedinUrl').value = user.linkedin_url || '';
  document.getElementById('githubUrl').value = user.github_url || '';
}

// Load application count
async function loadApplicationCount() {
  try {
    const response = await fetch('http://localhost:8000/api/applications/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const applications = await response.json();
      document.getElementById('applicationCount').textContent = applications.length;
      document.getElementById('applicationCount').textContent = applications.length;
    }
  } catch (error) {
    // Silently fail - application count is not critical
  }
}
// Add skill
function addSkill() {
  const skillInput = document.getElementById('skillInput');
  const skill = skillInput.value.trim();
  
  if (skill && !currentSkills.includes(skill)) {
    currentSkills.push(skill);
    renderSkills();
    skillInput.value = '';
  }
}

// Remove skill
function removeSkill(skill) {
  currentSkills = currentSkills.filter(s => s !== skill);
  renderSkills();
}

// Render skills
function renderSkills() {
  const container = document.getElementById('skillsContainer');
  
  if (currentSkills.length === 0) {
    container.innerHTML = '<p class="text-muted mt-2">No skills added yet. Add your skills above.</p>';
  } else {
    container.innerHTML = currentSkills.map(skill => `
      <div class="skill-tag">
        ${skill}
        <span class="remove-skill" onclick="removeSkill('${skill.replace(/'/g, "\\'")}')">&times;</span>
      </div>
    `).join('');
  }
  
  // Update hidden input
  document.getElementById('skills').value = currentSkills.join(', ');
}

// Save profile
async function saveProfile() {
  const saveBtn = document.getElementById('saveBtn');
  const saveSpinner = document.getElementById('saveSpinner');
  const saveIcon = document.getElementById('saveIcon');
  const saveBtnText = document.getElementById('saveBtnText');
  
  const firstName = document.getElementById('firstName').value.trim();
  const lastName = document.getElementById('lastName').value.trim();
  const phone = document.getElementById('phone').value.trim();
  
  if (!firstName || !lastName || !phone) {
    showAlert('Please fill in all required fields (First Name, Last Name, Phone)', 'danger');
    return;
  }
  
  saveBtn.disabled = true;
  saveIcon.style.display = 'none';
  saveSpinner.style.display = 'inline-block';
  saveBtnText.textContent = 'Saving...';
  hideAlert();
  
  const updateData = {
    first_name: firstName,
    last_name: lastName,
    phone: phone,
    bio: document.getElementById('bio').value.trim() || null,
    skills: currentSkills.length > 0 ? currentSkills.join(', ') : null,
    experience: document.getElementById('experience').value.trim() || null,
    education: document.getElementById('education').value.trim() || null,
    linkedin_url: document.getElementById('linkedinUrl').value.trim() || null,
    github_url: document.getElementById('githubUrl').value.trim() || null
  };
  
  try {
    const response = await fetch('http://localhost:8000/api/users/me', {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updateData)
    });
    
    if (response.ok) {
      const updatedUser = await response.json();
      originalProfileData = { ...updatedUser };
      
      // Update header
      const fullName = `${updatedUser.first_name} ${updatedUser.last_name}`;
      document.getElementById('profileName').textContent = fullName;
      document.getElementById('avatarInitial').textContent = updatedUser.first_name.charAt(0).toUpperCase();
      
      // Update localStorage
      localStorage.setItem('userName', fullName);
      
      // Show success state
      saveIcon.classList.remove('bi-check-lg');
      saveIcon.classList.add('bi-check-circle-fill');
      saveIcon.style.display = 'inline-block';
      saveSpinner.style.display = 'none';
      saveBtnText.textContent = 'Saved!';
      
      showAlert('Profile updated successfully!', 'success');
      
      // Scroll to top to show success message
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
      // Reset button after 2 seconds
      setTimeout(() => {
        saveIcon.classList.remove('bi-check-circle-fill');
        saveIcon.classList.add('bi-check-lg');
        saveBtnText.textContent = 'Save Changes';
      }, 2000);
    } else {
      const error = await response.json();
      showAlert(error.detail || 'Failed to update profile. Please try again.', 'danger');
      
      // Reset button state
      saveIcon.style.display = 'inline-block';
      saveSpinner.style.display = 'none';
      saveBtnText.textContent = 'Save Changes';
    }
  } catch (error) {
    showAlert('Network error. Please check your connection and try again.', 'danger');
    
    // Reset button state
    saveIcon.style.display = 'inline-block';
    saveSpinner.style.display = 'none';
    saveBtnText.textContent = 'Save Changes';
  } finally {
    // Reset button state
    saveBtn.disabled = false;
  }
}

// Reset form to original data
function resetForm() {
  if (confirm('Are you sure you want to discard all changes?')) {
    populateForm(originalProfileData);
    hideAlert();
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

// Logout function
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('userName');
  window.location.href = 'login.html';
}

// Make removeSkill globally accessible
window.removeSkill = removeSkill;
