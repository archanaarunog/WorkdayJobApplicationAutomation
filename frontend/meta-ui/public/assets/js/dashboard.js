// Dashboard Page - Application Tracking & Management

// Check authentication
const token = localStorage.getItem('token');
if (!token) {
  window.location.href = 'login.html';
}

// Global state
let allApplications = [];
let filteredApplications = [];
let currentFilter = 'all';
let currentSort = 'newest';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
  loadUserInfo();
  loadApplications();
  setupEventListeners();
});

// Load user information
function loadUserInfo() {
  const userEmail = localStorage.getItem('userEmail');
  const userName = localStorage.getItem('userName');
  
  if (userName) {
    document.getElementById('userName').textContent = userName;
  } else if (userEmail) {
    document.getElementById('userName').textContent = userEmail.split('@')[0];
  }
}

// Setup event listeners
function setupEventListeners() {
  // Logout button
  document.getElementById('logoutBtn').addEventListener('click', logout);
  
  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      currentFilter = this.dataset.status;
      filterAndSortApplications();
    });
  });
  
  // Sort select
  document.getElementById('sortSelect').addEventListener('change', function() {
    currentSort = this.value;
    filterAndSortApplications();
  });
}

// Load applications from API
async function loadApplications() {
  const loadingState = document.getElementById('loadingState');
  const applicationsContainer = document.getElementById('applicationsContainer');
  const emptyState = document.getElementById('emptyState');
  
  loadingState.style.display = 'block';
  applicationsContainer.style.display = 'none';
  emptyState.style.display = 'none';
  
  try {
    const response = await fetch('http://localhost:8000/api/applications/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      allApplications = await response.json();
      
      if (allApplications.length === 0) {
        loadingState.style.display = 'none';
        emptyState.style.display = 'block';
      } else {
        updateStatistics();
        filterAndSortApplications();
        loadingState.style.display = 'none';
        applicationsContainer.style.display = 'grid';
      }
    } else if (response.status === 401) {
      // Token expired
      localStorage.removeItem('token');
      window.location.href = 'login.html';
    } else {
      throw new Error('Failed to load applications');
    }
  } catch (error) {
    console.error('Error loading applications:', error);
    loadingState.innerHTML = `
      <div class="text-center">
        <i class="bi bi-exclamation-circle" style="font-size: 3rem; color: #C41E3A;"></i>
        <p class="mt-3" style="color: #666;">Failed to load applications. Please try again.</p>
        <button class="btn btn-browse-jobs" onclick="location.reload()">Retry</button>
      </div>
    `;
  }
}

// Update statistics
function updateStatistics() {
  const total = allApplications.length;
  const inReview = allApplications.filter(app => app.status === 'in_review' || app.status === 'submitted').length;
  const interview = allApplications.filter(app => app.status === 'interview').length;
  const rejected = allApplications.filter(app => app.status === 'rejected').length;
  
  document.getElementById('totalApplications').textContent = total;
  document.getElementById('pendingApplications').textContent = inReview;
  document.getElementById('interviewApplications').textContent = interview;
  document.getElementById('rejectedApplications').textContent = rejected;
}

// Filter and sort applications
function filterAndSortApplications() {
  // Filter
  if (currentFilter === 'all') {
    filteredApplications = [...allApplications];
  } else {
    filteredApplications = allApplications.filter(app => app.status === currentFilter);
  }
  
  // Sort
  switch (currentSort) {
    case 'newest':
      filteredApplications.sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at));
      break;
    case 'oldest':
      filteredApplications.sort((a, b) => new Date(a.applied_at) - new Date(b.applied_at));
      break;
    case 'company':
      filteredApplications.sort((a, b) => a.job.company.localeCompare(b.job.company));
      break;
    case 'status':
      const statusOrder = { 'interview': 1, 'in_review': 2, 'submitted': 3, 'accepted': 4, 'rejected': 5 };
      filteredApplications.sort((a, b) => (statusOrder[a.status] || 99) - (statusOrder[b.status] || 99));
      break;
  }
  
  renderApplications();
}

// Render applications
function renderApplications() {
  const container = document.getElementById('applicationsContainer');
  const emptyState = document.getElementById('emptyState');
  
  if (filteredApplications.length === 0) {
    container.style.display = 'none';
    emptyState.style.display = 'block';
    emptyState.querySelector('.empty-title').textContent = 'No Applications Found';
    emptyState.querySelector('.empty-text').textContent = 'No applications match your current filter.';
  } else {
    container.style.display = 'grid';
    emptyState.style.display = 'none';
    
    container.innerHTML = filteredApplications.map(app => createApplicationCard(app)).join('');
    
    // Add event listeners to view details buttons
    container.querySelectorAll('.btn-view-details').forEach(btn => {
      btn.addEventListener('click', function() {
        const jobId = this.dataset.jobId;
        window.location.href = `jobs.html?jobId=${jobId}`;
      });
    });
  }
}

// Create application card HTML
function createApplicationCard(app) {
  const appliedDate = formatDate(app.applied_at);
  const updatedDate = app.updated_at ? formatDate(app.updated_at) : appliedDate;
  const statusLabel = formatStatus(app.status);
  const salary = formatSalary(app.job.salary_min, app.job.salary_max);
  
  return `
    <div class="application-card">
      <div class="application-info">
        <div class="job-title">
          ${app.job.title}
          <span class="status-badge ${app.status}">${statusLabel}</span>
        </div>
        <div class="company-name">
          <i class="bi bi-building"></i>
          ${app.job.company}
        </div>
        <div class="job-details">
          <div class="job-detail-item">
            <i class="bi bi-geo-alt-fill"></i>
            ${app.job.location}
          </div>
          <div class="job-detail-item">
            <i class="bi bi-diagram-3-fill"></i>
            ${app.job.department}
          </div>
          <div class="job-detail-item">
            <i class="bi bi-briefcase-fill"></i>
            ${app.job.job_type}
          </div>
          ${salary ? `
          <div class="job-detail-item">
            <i class="bi bi-cash-stack"></i>
            ${salary}
          </div>
          ` : ''}
        </div>
        <div class="application-dates">
          <div class="date-item">
            <i class="bi bi-calendar-check"></i>
            Applied: ${appliedDate}
          </div>
          <div class="date-item">
            <i class="bi bi-clock-history"></i>
            Updated: ${updatedDate}
          </div>
        </div>
      </div>
      <div class="application-actions">
        <button class="btn-view-details" data-job-id="${app.job_id}">
          <i class="bi bi-eye me-1"></i>View Job
        </button>
      </div>
    </div>
  `;
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return date.toLocaleDateString('en-US', options);
}

// Format status
function formatStatus(status) {
  const statusMap = {
    'submitted': 'Submitted',
    'in_review': 'In Review',
    'interview': 'Interview',
    'rejected': 'Rejected',
    'accepted': 'Accepted'
  };
  return statusMap[status] || status;
}

// Format salary
function formatSalary(min, max) {
  if (!min && !max) return null;
  if (min && max) {
    return `$${(min / 1000).toFixed(0)}K - $${(max / 1000).toFixed(0)}K`;
  }
  if (min) return `$${(min / 1000).toFixed(0)}K+`;
  if (max) return `Up to $${(max / 1000).toFixed(0)}K`;
}

// Logout function
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('userName');
  window.location.href = 'login.html';
}
