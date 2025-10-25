// Admin Dashboard JavaScript
const API_BASE = 'http://localhost:8000';
let currentFilter = 'all';
let allApplications = [];

// Utility function to escape HTML
function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return unsafe
    .toString()
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Check authentication and admin role
document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  const userName = localStorage.getItem('userName');
  
  if (!token) {
    window.location.href = 'login.html';
    return;
  }
  
  // Load dashboard data
  loadStats();
  loadApplications();
  
  // Setup event listeners
  setupFilters();
  document.getElementById('logoutBtn').addEventListener('click', logout);
});

// Load dashboard statistics
async function loadStats() {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/stats`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.status === 403) {
      alert('Admin access required');
      window.location.href = 'jobs.html';
      return;
    }
    
    if (response.ok) {
      const stats = await response.json();
      document.getElementById('totalApplications').textContent = stats.total_applications;
      document.getElementById('totalJobs').textContent = stats.total_jobs;
      document.getElementById('totalUsers').textContent = stats.total_users;
      document.getElementById('interviewCount').textContent = stats.by_status.interview;
    }
  } catch (error) {
    console.error('Error loading stats:', error);
  }
}

// Load applications
async function loadApplications(status = 'all') {
  const token = localStorage.getItem('token');
  const tableBody = document.getElementById('applicationsTable');
  
  try {
    const url = status === 'all' 
      ? `${API_BASE}/api/admin/applications`
      : `${API_BASE}/api/admin/applications?status=${status}`;
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.status === 403) {
      alert('Admin access required');
      window.location.href = 'jobs.html';
      return;
    }
    
    if (response.ok) {
      allApplications = await response.json();
      renderApplicationsTable(allApplications);
    }
  } catch (error) {
    console.error('Error loading applications:', error);
    tableBody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error loading applications</td></tr>';
  }
}

// Render applications table
function renderApplicationsTable(applications) {
  const tableBody = document.getElementById('applicationsTable');
  
  if (applications.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="7" class="text-center py-4">No applications found</td></tr>';
    return;
  }
  
  tableBody.innerHTML = applications.map(app => `
    <tr>
      <td>${app.id}</td>
      <td>
        <strong>${app.user.name}</strong><br>
        <small class="text-muted">${app.user.email}</small>
      </td>
      <td>
        <strong>${app.job.title}</strong><br>
        <small class="text-muted">${app.job.company && app.job.company.name ? app.job.company.name : 'N/A'}</small>
      </td>
      <td>${app.job.department || 'N/A'}</td>
      <td>${formatDate(app.applied_at)}</td>
      <td><span class="status-badge status-${app.status}">${formatStatus(app.status)}</span></td>
      <td>
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
            Change Status
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" onclick="updateStatus(${app.id}, 'submitted')">Submitted</a></li>
            <li><a class="dropdown-item" href="#" onclick="updateStatus(${app.id}, 'in_review')">In Review</a></li>
            <li><a class="dropdown-item" href="#" onclick="updateStatus(${app.id}, 'interview')">Interview</a></li>
            <li><a class="dropdown-item" href="#" onclick="updateStatus(${app.id}, 'accepted')">Accepted</a></li>
            <li><a class="dropdown-item" href="#" onclick="updateStatus(${app.id}, 'rejected')">Rejected</a></li>
          </ul>
        </div>
      </td>
    </tr>
  `).join('');
}

// Update application status
async function updateStatus(appId, newStatus) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/applications/${appId}/status`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: newStatus })
    });
    
    if (response.ok) {
      // Reload data
      loadStats();
      loadApplications(currentFilter);
    } else {
      alert('Failed to update status');
    }
  } catch (error) {
    console.error('Error updating status:', error);
    alert('Error updating status');
  }
}

// Setup filter buttons
function setupFilters() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const status = btn.getAttribute('data-status');
      currentFilter = status;
      
      // Update active state
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      // Load filtered applications
      loadApplications(status);
    });
  });
  
  // Set first button as active
  filterButtons[0].classList.add('active');
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// Format status
function formatStatus(status) {
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Logout
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('userName');
  window.location.href = 'login.html';
}

// ==================== JOB MANAGEMENT FUNCTIONS ====================

let allJobs = [];
let currentJob = null;

// ==================== USER MANAGEMENT FUNCTIONS ====================

let allUsers = [];
let filteredUsers = [];

// Initialize job management when tab is clicked
document.addEventListener('DOMContentLoaded', () => {
  // Add tab event listeners
  const jobTab = document.getElementById('jobs-tab');
  if (jobTab) {
    jobTab.addEventListener('click', () => {
      loadJobs();
      loadJobAnalytics();
    });
  }
  
  const userTab = document.getElementById('users-tab');
  if (userTab) {
    userTab.addEventListener('click', () => {
      loadUsers(); // This will call loadUserAnalytics() automatically
    });
  }
  
  // Job management button listeners
  const createJobBtn = document.getElementById('createJobBtn');
  const saveJobBtn = document.getElementById('saveJobBtn');
  const refreshJobsBtn = document.getElementById('refreshJobsBtn');
  
  if (createJobBtn) createJobBtn.addEventListener('click', () => openJobModal());
  if (saveJobBtn) saveJobBtn.addEventListener('click', saveJob);
  if (refreshJobsBtn) refreshJobsBtn.addEventListener('click', loadJobs);
  
  // User management button listeners
  const refreshUsersBtn = document.getElementById('refreshUsersBtn');
  const userSearch = document.getElementById('userSearch');
  
  if (refreshUsersBtn) refreshUsersBtn.addEventListener('click', loadUsers);
  if (userSearch) {
    userSearch.addEventListener('input', (e) => {
      filterUsers(e.target.value);
    });
  }
});

// Load job analytics
async function loadJobAnalytics() {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/jobs/analytics`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const analytics = await response.json();
      
      document.getElementById('totalJobsCount').textContent = analytics.total_jobs;
      document.getElementById('activeJobsCount').textContent = analytics.active_jobs;
      document.getElementById('jobsWithoutApps').textContent = analytics.jobs_without_applications;
      
      // Calculate average applications per job
      const avgApps = analytics.total_jobs > 0 ? 
        Math.round((analytics.total_jobs - analytics.jobs_without_applications) / analytics.total_jobs * 100) / 100 : 0;
      document.getElementById('avgApplications').textContent = avgApps;
    }
  } catch (error) {
    console.error('Error loading job analytics:', error);
  }
}

// Load all jobs
async function loadJobs() {
  const token = localStorage.getItem('token');
  const tableBody = document.getElementById('jobsTable');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/jobs`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      allJobs = await response.json();
      renderJobsTable(allJobs);
    }
  } catch (error) {
    console.error('Error loading jobs:', error);
    tableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error loading jobs</td></tr>';
  }
}

// Render jobs table
function renderJobsTable(jobs) {
  const tableBody = document.getElementById('jobsTable');
  
  if (jobs.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="8" class="text-center py-4">No jobs found</td></tr>';
    return;
  }
  
  tableBody.innerHTML = jobs.map(job => `
    <tr>
      <td>${job.id}</td>
      <td>
        <strong>${job.title}</strong>
        <br><small class="text-muted">${job.job_type}</small>
      </td>
      <td>${job.company && job.company.name ? job.company.name : 'N/A'}</td>
      <td>
        ${job.location}
        <br><small class="text-muted">${job.remote_options}</small>
      </td>
      <td>${job.department || 'N/A'}</td>
      <td>
        <span class="badge bg-info">${job.application_count}</span>
      </td>
      <td>
        <span class="badge ${job.is_active ? 'bg-success' : 'bg-secondary'}">
          ${job.is_active ? 'Active' : 'Inactive'}
        </span>
      </td>
      <td>
        <div class="btn-group btn-group-sm" role="group">
          <button class="btn btn-outline-primary btn-sm" onclick="editJob(${job.id})" title="Edit">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-outline-${job.is_active ? 'warning' : 'success'} btn-sm" 
                  onclick="toggleJobStatus(${job.id}, ${!job.is_active})" 
                  title="${job.is_active ? 'Deactivate' : 'Activate'}">
            <i class="bi bi-${job.is_active ? 'pause' : 'play'}"></i>
          </button>
          ${job.application_count === 0 ? `
          <button class="btn btn-outline-danger btn-sm" onclick="deleteJob(${job.id})" title="Delete">
            <i class="bi bi-trash"></i>
          </button>
          ` : `
          <button class="btn btn-outline-secondary btn-sm" disabled title="Cannot delete: has applications">
            <i class="bi bi-trash"></i>
          </button>
          `}
        </div>
      </td>
    </tr>
  `).join('');
}

// Open job modal for create/edit
function openJobModal(job = null) {
  currentJob = job;
  const modal = new bootstrap.Modal(document.getElementById('jobModal'));
  const modalTitle = document.getElementById('jobModalLabel');
  const form = document.getElementById('jobForm');
  
  if (job) {
    // Edit mode
    modalTitle.textContent = 'Edit Job';
    document.getElementById('jobId').value = job.id;
    document.getElementById('jobTitle').value = job.title;
    document.getElementById('jobCompany').value = job.company && job.company.name ? job.company.name : '';
    document.getElementById('jobDepartment').value = job.department || '';
    document.getElementById('jobLocation').value = job.location;
    document.getElementById('jobDescription').value = job.description;
    document.getElementById('jobRequirements').value = job.requirements || '';
    document.getElementById('jobBenefits').value = job.benefits || '';
    document.getElementById('salaryMin').value = job.salary_min || '';
    document.getElementById('salaryMax').value = job.salary_max || '';
    document.getElementById('jobType').value = job.job_type;
    document.getElementById('remoteOptions').value = job.remote_options;
    document.getElementById('jobActive').checked = job.is_active;
  } else {
    // Create mode
    modalTitle.textContent = 'Create New Job';
    form.reset();
    document.getElementById('jobActive').checked = true;
  }
  
  modal.show();
}

// Edit job
function editJob(jobId) {
  const job = allJobs.find(j => j.id === jobId);
  if (job) {
    openJobModal(job);
  }
}

// Save job (create or update)
async function saveJob() {
  const token = localStorage.getItem('token');
  const jobId = document.getElementById('jobId').value;
  const isEdit = jobId && jobId !== '';
  
  const jobData = {
    title: document.getElementById('jobTitle').value,
    company: document.getElementById('jobCompany').value,
    department: document.getElementById('jobDepartment').value,
    location: document.getElementById('jobLocation').value,
    description: document.getElementById('jobDescription').value,
    requirements: document.getElementById('jobRequirements').value,
    benefits: document.getElementById('jobBenefits').value,
    salary_min: parseInt(document.getElementById('salaryMin').value) || null,
    salary_max: parseInt(document.getElementById('salaryMax').value) || null,
    job_type: document.getElementById('jobType').value,
    remote_options: document.getElementById('remoteOptions').value,
    is_active: document.getElementById('jobActive').checked
  };
  
  try {
    const url = isEdit ? 
      `${API_BASE}/api/admin/jobs/${jobId}` : 
      `${API_BASE}/api/admin/jobs`;
    
    const method = isEdit ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jobData)
    });
    
    if (response.ok) {
      const result = await response.json();
      
      // Show success message
      showAlert(`Job ${isEdit ? 'updated' : 'created'} successfully!`, 'success');
      
      // Close modal
      const modal = bootstrap.Modal.getInstance(document.getElementById('jobModal'));
      modal.hide();
      
      // Reload data
      loadJobs();
      loadJobAnalytics();
      loadStats(); // Update main dashboard stats
      
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || 'Failed to save job'}`, 'error');
    }
  } catch (error) {
    console.error('Error saving job:', error);
    showAlert('Error saving job', 'error');
  }
}

// Toggle job status
async function toggleJobStatus(jobId, newStatus) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/jobs/${jobId}/status`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_active: newStatus })
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(result.message, 'success');
      
      // Reload data
      loadJobs();
      loadJobAnalytics();
      loadStats();
      
    } else {
      showAlert('Failed to update job status', 'error');
    }
  } catch (error) {
    console.error('Error updating job status:', error);
    showAlert('Error updating job status', 'error');
  }
}

// Delete job
async function deleteJob(jobId) {
  if (!confirm('Are you sure you want to delete this job? This action cannot be undone.')) {
    return;
  }
  
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/jobs/${jobId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(result.message, 'success');
      
      // Reload data
      loadJobs();
      loadJobAnalytics();
      loadStats();
      
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || 'Failed to delete job'}`, 'error');
    }
  } catch (error) {
    console.error('Error deleting job:', error);
    showAlert('Error deleting job', 'error');
  }
}

// Show alert messages
function showAlert(message, type = 'info') {
  // Create alert element
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  // Insert at top of container
  const container = document.querySelector('.container');
  container.insertBefore(alertDiv, container.firstChild);
  
  // Auto dismiss after 3 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove();
    }
  }, 3000);
}

// ==================== USER MANAGEMENT FUNCTIONS ====================

// Load user analytics - Calculate from user data
function loadUserAnalytics() {
  if (allUsers.length === 0) return;
  
  const totalUsers = allUsers.length;
  const adminCount = allUsers.filter(user => user.is_admin).length;
  const activeUsers = allUsers.filter(user => user.application_count > 0).length;
  const newThisMonth = totalUsers; // All registered recently
  
  document.getElementById('totalUsersCount').textContent = totalUsers;
  document.getElementById('newUsersMonth').textContent = newThisMonth;
  document.getElementById('activeUsersCount').textContent = activeUsers;
  document.getElementById('adminUsersCount').textContent = adminCount;
}

// Load all users
async function loadUsers() {
  const token = localStorage.getItem('token');
  const tableBody = document.getElementById('usersTable');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/users`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      allUsers = await response.json();
      filteredUsers = [...allUsers]; // Copy for filtering
      renderUsersTable(filteredUsers);
      loadUserAnalytics(); // Calculate analytics after loading users
    }
  } catch (error) {
    console.error('Error loading users:', error);
    tableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error loading users</td></tr>';
  }
}

// Render users table
function renderUsersTable(users) {
  const tableBody = document.getElementById('usersTable');
  
  if (users.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="8" class="text-center py-4">No users found</td></tr>';
    return;
  }
  
  tableBody.innerHTML = users.map(user => `
    <tr>
      <td>${user.id}</td>
      <td>
        <strong>${user.full_name}</strong>
      </td>
      <td>${user.email}</td>
      <td>${user.phone || 'N/A'}</td>
      <td>${formatDate(user.created_at)}</td>
      <td>
        <span class="badge bg-info">${user.application_count}</span>
      </td>
      <td>
        <span class="badge ${user.is_admin ? 'bg-danger' : 'bg-primary'}">
          ${user.is_admin ? 'Admin' : 'User'}
        </span>
      </td>
      <td>
        <div class="btn-group btn-group-sm" role="group">
          <button class="btn btn-outline-info btn-sm" onclick="viewUserDetails(${user.id})" title="View Details">
            <i class="bi bi-eye"></i>
          </button>
          <button class="btn btn-outline-${user.is_admin ? 'warning' : 'success'} btn-sm" 
                  onclick="toggleUserAdmin(${user.id}, ${!user.is_admin})" 
                  title="${user.is_admin ? 'Remove Admin' : 'Make Admin'}">
            <i class="bi bi-${user.is_admin ? 'person-dash' : 'person-plus'}"></i>
          </button>
          <button class="btn btn-outline-secondary btn-sm" onclick="toggleUserStatus(${user.id}, false)" title="Disable Account">
            <i class="bi bi-person-x"></i>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

// Filter users based on search
function filterUsers(searchTerm) {
  if (!searchTerm) {
    filteredUsers = [...allUsers];
  } else {
    const term = searchTerm.toLowerCase();
    filteredUsers = allUsers.filter(user => 
      user.full_name.toLowerCase().includes(term) ||
      user.email.toLowerCase().includes(term) ||
      user.phone?.includes(term)
    );
  }
  renderUsersTable(filteredUsers);
}

// View user details
async function viewUserDetails(userId) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const user = await response.json();
      
      // Populate modal with user data
      document.getElementById('userId').textContent = user.id;
      document.getElementById('userFullName').textContent = `${user.first_name} ${user.last_name}`;
      document.getElementById('userEmail').textContent = user.email;
      document.getElementById('userPhone').textContent = user.phone || 'Not provided';
      document.getElementById('userRole').textContent = user.is_admin ? 'Administrator' : 'User';
      document.getElementById('userRegistered').textContent = formatDate(user.created_at);
      document.getElementById('userStatus').textContent = user.is_active ? 'Active' : 'Inactive';
      document.getElementById('userApplicationCount').textContent = user.application_count;
      
      // Populate applications
      const applicationsDiv = document.getElementById('userApplications');
      if (user.applications.length === 0) {
        applicationsDiv.innerHTML = '<p class="text-muted">No applications submitted yet.</p>';
      } else {
        applicationsDiv.innerHTML = `
          <div class="table-responsive">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>Job</th>
                  <th>Company</th>
                  <th>Status</th>
                  <th>Applied</th>
                </tr>
              </thead>
              <tbody>
                ${user.applications.map(app => `
                  <tr>
                    <td>${app.job_title}</td>
                    <td>${app.company && app.company.name ? app.company.name : 'N/A'}</td>
                    <td><span class="badge bg-secondary">${formatStatus(app.status)}</span></td>
                    <td>${formatDate(app.applied_at)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
      }
      
      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('userModal'));
      modal.show();
      
    } else {
      showAlert('Failed to load user details', 'error');
    }
  } catch (error) {
    console.error('Error loading user details:', error);
    showAlert('Error loading user details', 'error');
  }
}

// Toggle user admin privileges
async function toggleUserAdmin(userId, makeAdmin) {
  if (!confirm(`Are you sure you want to ${makeAdmin ? 'grant admin privileges to' : 'remove admin privileges from'} this user?`)) {
    return;
  }
  
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/users/${userId}/admin`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_admin: makeAdmin })
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(result.message, 'success');
      
      // Reload data
      loadUsers();
      loadUserAnalytics();
      loadStats(); // Update main dashboard stats
      
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || 'Failed to update admin privileges'}`, 'error');
    }
  } catch (error) {
    console.error('Error updating admin privileges:', error);
    showAlert('Error updating admin privileges', 'error');
  }
}

// Toggle user account status
async function toggleUserStatus(userId, isActive) {
  const action = isActive ? 'enable' : 'disable';
  if (!confirm(`Are you sure you want to ${action} this user account?`)) {
    return;
  }
  
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/users/${userId}/status`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_active: isActive })
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(result.message, 'success');
      
      // Note: Since we don't have is_active column yet, this is simulated
      if (result.note) {
        showAlert(result.note, 'info');
      }
      
      // Reload data
      loadUsers();
      loadUserAnalytics();
      
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || 'Failed to update account status'}`, 'error');
    }
  } catch (error) {
    console.error('Error updating account status:', error);
    showAlert('Error updating account status', 'error');
  }
}

// ==================== COMPANY MANAGEMENT FUNCTIONS ====================

let allCompanies = [];
let currentCompanyId = null;

// Load company management data
async function loadCompanies() {
  const token = localStorage.getItem('token');
  
  if (!token) {
    console.error('No token found');
    window.location.href = 'login.html';
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/companies`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      allCompanies = await response.json();
      console.log('Companies loaded:', allCompanies);
      displayCompanies();
      updateCompanyStatistics();
    } else if (response.status === 401) {
      console.error('Unauthorized - redirecting to login');
      localStorage.removeItem('token');
      window.location.href = 'login.html';
    } else {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      console.error('Error response:', error);
      showAlert(`Error loading companies: ${error.detail}`, 'error');
    }
  } catch (error) {
    console.error('Network error loading companies:', error);
    showAlert('Network error loading companies. Please check if the server is running.', 'error');
  }
}

// Display companies in table
function displayCompanies() {
  const tbody = document.getElementById('companiesTableBody');
  
  if (allCompanies.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" class="text-center">No companies found</td>
      </tr>
    `;
    return;
  }
  
  tbody.innerHTML = allCompanies.map(company => `
    <tr>
      <td>
        <div class="d-flex align-items-center">
          <div>
            <strong>${escapeHtml(company.name)}</strong>
            <div class="text-muted small">${escapeHtml(company.slug)}</div>
          </div>
        </div>
      </td>
      <td>
        ${company.domain ? `<a href="https://${escapeHtml(company.domain)}" target="_blank">${escapeHtml(company.domain)}</a>` : '-'}
      </td>
      <td>${escapeHtml(company.industry || '-')}</td>
      <td>
        ${company.admin_user ? `
          <div>
            <strong>${escapeHtml(company.admin_user.name)}</strong>
            <div class="text-muted small">${escapeHtml(company.admin_user.email)}</div>
          </div>
        ` : '<span class="text-muted">No admin assigned</span>'}
      </td>
      <td>
        <span class="badge bg-info">${company.statistics.user_count}</span>
      </td>
      <td>
        <span class="badge bg-success">${company.statistics.active_job_count}</span>
        <span class="text-muted">/${company.statistics.job_count}</span>
      </td>
      <td>
        <span class="badge ${company.is_active ? 'bg-success' : 'bg-secondary'}">
          ${company.is_active ? 'Active' : 'Inactive'}
        </span>
      </td>
      <td>${formatDate(company.created_at)}</td>
      <td>
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown">
            Actions
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" onclick="viewCompanyDetails(${company.id})">
              <i class="bi bi-eye me-1"></i>View Details
            </a></li>
            <li><a class="dropdown-item" href="#" onclick="editCompany(${company.id})">
              <i class="bi bi-pencil me-1"></i>Edit
            </a></li>
            <li><a class="dropdown-item" href="#" onclick="toggleCompanyStatus(${company.id}, ${!company.is_active})">
              <i class="bi bi-power me-1"></i>${company.is_active ? 'Deactivate' : 'Activate'}
            </a></li>
            ${company.slug !== 'default' ? `
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item text-danger" href="#" onclick="deleteCompany(${company.id})">
              <i class="bi bi-trash me-1"></i>Delete
            </a></li>
            ` : ''}
          </ul>
        </div>
      </td>
    </tr>
  `).join('');
}

// Update company statistics cards
function updateCompanyStatistics() {
  const totalCompanies = allCompanies.length;
  const activeCompanies = allCompanies.filter(c => c.is_active).length;
  const companiesWithJobs = allCompanies.filter(c => c.statistics.job_count > 0).length;
  const averageUsers = totalCompanies > 0 ? Math.round(
    allCompanies.reduce((sum, c) => sum + c.statistics.user_count, 0) / totalCompanies
  ) : 0;
  
  document.getElementById('totalCompanies').textContent = totalCompanies;
  document.getElementById('activeCompanies').textContent = activeCompanies;
  document.getElementById('companiesWithJobs').textContent = companiesWithJobs;
  document.getElementById('averageCompanyUsers').textContent = averageUsers;
}

// Open company modal for creating new company
async function openCompanyModal() {
  currentCompanyId = null;
  document.getElementById('companyModalLabel').textContent = 'Add New Company';
  document.getElementById('saveCompanyBtn').innerHTML = '<i class="bi bi-building-check me-1"></i>Save Company';
  
  // Reset form
  document.getElementById('companyForm').reset();
  
  // Load admin users for dropdown
  await loadAdminUsers();
}

// Load admin users for company admin dropdown
async function loadAdminUsers() {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/users`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const users = await response.json();
      const adminUsers = users.filter(user => user.is_admin);
      
      const select = document.getElementById('companyAdminUser');
      select.innerHTML = '<option value="">Select Admin User</option>' + 
        adminUsers.map(user => 
          `<option value="${user.id}">${escapeHtml(user.full_name)} (${escapeHtml(user.email)})</option>`
        ).join('');
    }
  } catch (error) {
    console.error('Error loading admin users:', error);
  }
}

// Auto-generate slug from company name
document.addEventListener('DOMContentLoaded', () => {
  const companyNameInput = document.getElementById('companyName');
  const companySlugInput = document.getElementById('companySlug');
  
  if (companyNameInput && companySlugInput) {
    companyNameInput.addEventListener('input', (e) => {
      if (!currentCompanyId) { // Only auto-generate for new companies
        const slug = e.target.value
          .toLowerCase()
          .replace(/[^a-z0-9]/g, '-')
          .replace(/-+/g, '-')
          .replace(/^-|-$/g, '');
        companySlugInput.value = slug;
      }
    });
  }
});

// Save company (create or update)
document.addEventListener('DOMContentLoaded', () => {
  const saveBtn = document.getElementById('saveCompanyBtn');
  if (saveBtn) {
    saveBtn.addEventListener('click', saveCompany);
  }
});

async function saveCompany() {
  const formData = {
    name: document.getElementById('companyName').value.trim(),
    slug: document.getElementById('companySlug').value.trim(),
    domain: document.getElementById('companyDomain').value.trim() || null,
    industry: document.getElementById('companyIndustry').value || null,
    website: document.getElementById('companyWebsite').value.trim() || null,
    headquarters: document.getElementById('companyHeadquarters').value.trim() || null,
    size: document.getElementById('companySize').value || null,
    description: document.getElementById('companyDescription').value.trim() || null,
    admin_user_id: parseInt(document.getElementById('companyAdminUser').value) || null
  };
  
  // Validation
  if (!formData.name || !formData.slug) {
    showAlert('Company name and slug are required', 'error');
    return;
  }
  
  const token = localStorage.getItem('token');
  const url = currentCompanyId ? 
    `${API_BASE}/api/admin/companies/${currentCompanyId}` : 
    `${API_BASE}/api/admin/companies`;
  const method = currentCompanyId ? 'PATCH' : 'POST';
  
  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(result.message, 'success');
      
      // Close modal and reload data
      const modal = bootstrap.Modal.getInstance(document.getElementById('companyModal'));
      modal.hide();
      
      loadCompanies();
      
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || 'Failed to save company'}`, 'error');
    }
  } catch (error) {
    console.error('Error saving company:', error);
    showAlert('Error saving company', 'error');
  }
}

// View company details
async function viewCompanyDetails(companyId) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/companies/${companyId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const company = await response.json();
      currentCompanyId = companyId;
      
      // Populate company information
      document.getElementById('detailCompanyName').textContent = company.name;
      document.getElementById('detailCompanyDomain').textContent = company.domain || 'N/A';
      document.getElementById('detailCompanyIndustry').textContent = company.industry || 'N/A';
      document.getElementById('detailCompanyHeadquarters').textContent = company.headquarters || 'N/A';
      document.getElementById('detailCompanySize').textContent = company.size || 'N/A';
      document.getElementById('detailCompanyDescription').textContent = company.description || 'No description available.';
      
      // Website link
      const websiteLink = document.getElementById('detailCompanyWebsite');
      if (company.website) {
        websiteLink.href = company.website;
        websiteLink.textContent = company.website;
        websiteLink.style.display = 'inline';
      } else {
        websiteLink.style.display = 'none';
        websiteLink.parentNode.innerHTML = '<strong>Website:</strong> N/A';
      }
      
      // Statistics
      document.getElementById('detailCompanyUsers').textContent = company.statistics.total_users;
      document.getElementById('detailCompanyJobs').textContent = `${company.statistics.active_jobs}/${company.statistics.total_jobs}`;
      document.getElementById('detailCompanyApplications').textContent = company.statistics.total_applications;
      document.getElementById('detailCompanyStatus').innerHTML = 
        `<span class="badge ${company.is_active ? 'bg-success' : 'bg-secondary'}">${company.is_active ? 'Active' : 'Inactive'}</span>`;
      document.getElementById('detailCompanyCreated').textContent = formatDate(company.created_at);
      
      // Admin info
      if (company.admin_user) {
        document.getElementById('detailCompanyAdmin').innerHTML = 
          `${escapeHtml(company.admin_user.name)}<br><small class="text-muted">${escapeHtml(company.admin_user.email)}</small>`;
      } else {
        document.getElementById('detailCompanyAdmin').textContent = 'No admin assigned';
      }
      
      // Recent activity
      displayRecentActivity(company.recent_activity);
      
      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('companyDetailsModal'));
      modal.show();
      
    } else {
      const error = await response.json();
      showAlert(`Error loading company details: ${error.detail}`, 'error');
    }
  } catch (error) {
    console.error('Error loading company details:', error);
    showAlert('Error loading company details', 'error');
  }
}

// Display recent activity in company details modal
function displayRecentActivity(activity) {
  // Recent users
  const usersContainer = document.getElementById('detailRecentUsers');
  if (activity.recent_users && activity.recent_users.length > 0) {
    usersContainer.innerHTML = activity.recent_users.map(user => `
      <div class="border-bottom py-1">
        <small><strong>${escapeHtml(user.name)}</strong><br>
        <span class="text-muted">${formatDate(user.created_at)}</span></small>
      </div>
    `).join('');
  } else {
    usersContainer.innerHTML = '<small class="text-muted">No recent users</small>';
  }
  
  // Recent jobs
  const jobsContainer = document.getElementById('detailRecentJobs');
  if (activity.recent_jobs && activity.recent_jobs.length > 0) {
    jobsContainer.innerHTML = activity.recent_jobs.map(job => `
      <div class="border-bottom py-1">
        <small><strong>${escapeHtml(job.title)}</strong><br>
        <span class="text-muted">${escapeHtml(job.location)} - ${formatDate(job.posted_date)}</span></small>
      </div>
    `).join('');
  } else {
    jobsContainer.innerHTML = '<small class="text-muted">No recent jobs</small>';
  }
  
  // Recent applications
  const appsContainer = document.getElementById('detailRecentApplications');
  if (activity.recent_applications && activity.recent_applications.length > 0) {
    appsContainer.innerHTML = activity.recent_applications.map(app => `
      <div class="border-bottom py-1">
        <small><strong>${escapeHtml(app.user_name)}</strong><br>
        <span class="text-muted">${escapeHtml(app.job_title)} - ${formatDate(app.applied_at)}</span></small>
      </div>
    `).join('');
  } else {
    appsContainer.innerHTML = '<small class="text-muted">No recent applications</small>';
  }
}

// Edit company
async function editCompany(companyId) {
  const company = allCompanies.find(c => c.id === companyId);
  if (!company) return;
  
  currentCompanyId = companyId;
  document.getElementById('companyModalLabel').textContent = 'Edit Company';
  document.getElementById('saveCompanyBtn').innerHTML = '<i class="bi bi-building-check me-1"></i>Update Company';
  
  // Populate form
  document.getElementById('companyName').value = company.name;
  document.getElementById('companySlug').value = company.slug;
  document.getElementById('companyDomain').value = company.domain || '';
  document.getElementById('companyIndustry').value = company.industry || '';
  document.getElementById('companyWebsite').value = company.website || '';
  document.getElementById('companyHeadquarters').value = company.headquarters || '';
  document.getElementById('companySize').value = company.size || '';
  document.getElementById('companyDescription').value = company.description || '';
  
  // Load admin users and set current admin
  await loadAdminUsers();
  if (company.admin_user) {
    document.getElementById('companyAdminUser').value = company.admin_user.id;
  }
  
  // Show modal
  const modal = new bootstrap.Modal(document.getElementById('companyModal'));
  modal.show();
}

// Toggle company status
async function toggleCompanyStatus(companyId, newStatus) {
  const company = allCompanies.find(c => c.id === companyId);
  const action = newStatus ? 'activate' : 'deactivate';
  
  if (!confirm(`Are you sure you want to ${action} "${company.name}"?`)) {
    return;
  }
  
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/companies/${companyId}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_active: newStatus })
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(result.message, 'success');
      loadCompanies();
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || `Failed to ${action} company`}`, 'error');
    }
  } catch (error) {
    console.error(`Error ${action}ing company:`, error);
    showAlert(`Error ${action}ing company`, 'error');
  }
}

// Delete company
async function deleteCompany(companyId) {
  const company = allCompanies.find(c => c.id === companyId);
  
  if (company.slug === 'default') {
    showAlert('Cannot delete the default company', 'error');
    return;
  }
  
  const confirmation = prompt(
    `WARNING: This will permanently delete "${company.name}" and ALL associated data (users, jobs, applications).\n\n` +
    `Type the company name "${company.name}" to confirm deletion:`
  );
  
  if (confirmation !== company.name) {
    if (confirmation !== null) {
      showAlert('Company name did not match. Deletion cancelled.', 'error');
    }
    return;
  }
  
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_BASE}/api/admin/companies/${companyId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const result = await response.json();
      showAlert(`${result.message}\nDeleted: ${result.deleted_data.users} users, ${result.deleted_data.jobs} jobs, ${result.deleted_data.applications} applications`, 'success');
      loadCompanies();
    } else {
      const error = await response.json();
      showAlert(`Error: ${error.detail || 'Failed to delete company'}`, 'error');
    }
  } catch (error) {
    console.error('Error deleting company:', error);
    showAlert('Error deleting company', 'error');
  }
}

// Filter companies by status
function filterCompanies() {
  const filter = document.getElementById('companyStatusFilter').value;
  let filteredCompanies = allCompanies;
  
  if (filter === 'active') {
    filteredCompanies = allCompanies.filter(c => c.is_active);
  } else if (filter === 'inactive') {
    filteredCompanies = allCompanies.filter(c => !c.is_active);
  }
  
  const searchTerm = document.getElementById('companySearch').value.toLowerCase();
  if (searchTerm) {
    filteredCompanies = filteredCompanies.filter(c => 
      c.name.toLowerCase().includes(searchTerm) ||
      (c.domain && c.domain.toLowerCase().includes(searchTerm)) ||
      (c.industry && c.industry.toLowerCase().includes(searchTerm))
    );
  }
  
  displayFilteredCompanies(filteredCompanies);
}

// Search companies
function searchCompanies() {
  filterCompanies(); // Reuse the same filtering logic
}

// Display filtered companies
function displayFilteredCompanies(companies) {
  const tbody = document.getElementById('companiesTableBody');
  
  if (companies.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" class="text-center">No companies match the current filter</td>
      </tr>
    `;
    return;
  }
  
  // Use the same display logic but with filtered companies
  const originalCompanies = allCompanies;
  allCompanies = companies;
  displayCompanies();
  allCompanies = originalCompanies;
}

// Load companies when Companies tab is activated
document.addEventListener('DOMContentLoaded', () => {
  // Add event listener for tab changes
  const companiesTab = document.getElementById('companies-tab');
  if (companiesTab) {
    companiesTab.addEventListener('shown.bs.tab', () => {
      console.log('Companies tab activated');
      loadCompanies();
    });
    
    // Also add click event as backup
    companiesTab.addEventListener('click', () => {
      console.log('Companies tab clicked');
      setTimeout(() => {
        loadCompanies();
      }, 200);
    });
  }
  
  // Add manual debug function to window
  window.debugLoadCompanies = loadCompanies;
  console.log('Debug: window.debugLoadCompanies() available for testing');
});
