// Admin Dashboard JavaScript
const API_BASE = 'http://localhost:8000';
let currentFilter = 'all';
let allApplications = [];

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
        <small class="text-muted">${app.job.company}</small>
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
