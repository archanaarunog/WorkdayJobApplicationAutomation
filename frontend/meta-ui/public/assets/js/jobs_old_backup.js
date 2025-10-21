/**
 * Meta Job Portal - Jobs Page JavaScript
 * Phase 3.1: Professional Job Portal with Tabs, Filters, and Grid Layout
 */

// ==================== Global State ====================
let allJobs = [];
let filteredJobs = [];
let allApplications = [];
const API_BASE = 'http://localhost:8000/api';

// ==================== Utility Functions ====================

function getToken() {
  return localStorage.getItem('token');
}

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatSalary(salary) {
  if (!salary) return 'Not specified';
  return `$${salary.toLocaleString()}`;
}

function getCompanyInitial(companyName) {
  return companyName ? companyName.charAt(0).toUpperCase() : 'C';
}

// ==================== API Calls ====================

async function fetchJobsFromAPI() {
  try {
    const token = getToken();
    const res = await fetch(`${API_BASE}/jobs/`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    
    if (res.ok) {
      allJobs = await res.json();
      filteredJobs = [...allJobs];
      return allJobs;
    } else {
      console.error('Failed to fetch jobs:', res.status);
      return [];
    }
  } catch (error) {
    console.error('Network error fetching jobs:', error);
    return [];
  }
}

async function fetchApplicationsFromAPI() {
  try {
    const token = getToken();
    if (!token) {
      return [];
    }
    
    const res = await fetch(`${API_BASE}/applications/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      allApplications = await res.json();
      return allApplications;
    } else {
      console.error('Failed to fetch applications:', res.status);
      return [];
    }
  } catch (error) {
    console.error('Network error fetching applications:', error);
    return [];
  }
}

async function submitApplication(applicationData) {
  try {
    const token = getToken();
    if (!token) {
      throw new Error('Please login to apply');
    }
    
    const res = await fetch(`${API_BASE}/applications/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(applicationData)
    });
    
    if (res.ok) {
      return { success: true, data: await res.json() };
    } else {
      const error = await res.json();
      return { success: false, error: error.detail || 'Failed to submit application' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ==================== Dashboard Stats ====================

function updateDashboardStats() {
  // Total Jobs
  document.getElementById('totalJobsCount').textContent = allJobs.length;
  
  // Applications Count
  document.getElementById('applicationsCount').textContent = allApplications.length;
  
  // Response Rate (mock calculation)
  const responseRate = allApplications.length > 0 
    ? Math.floor((allApplications.filter(app => app.status !== 'pending').length / allApplications.length) * 100)
    : 0;
  document.getElementById('responseRate').textContent = `${responseRate}%`;
  
  // Profile Views (mock data)
  document.getElementById('profileViews').textContent = '24';
}

// ==================== Job Card Rendering ====================

function renderJobCard(job) {
  const companyInitial = getCompanyInitial(job.company || 'Company');
  const isApplied = allApplications.some(app => app.job_id === job.id);
  
  return `
    <div class="col-lg-6">
      <div class="card job-card">
        <!-- Header with Logo and Title -->
        <div class="job-card-header">
          <div class="d-flex gap-3">
            <div class="company-logo">
              ${companyInitial}
            </div>
            <div class="flex-grow-1">
              <h3 class="job-title mb-2">${job.title}</h3>
              <p class="company-name mb-2">${job.company || 'Company Name'}</p>
              <div class="d-flex gap-2 flex-wrap">
                <span class="badge badge-location">
                  <i class="bi bi-geo-alt me-1"></i>${job.location || 'Remote'}
                </span>
                <span class="badge badge-type">
                  <i class="bi bi-briefcase me-1"></i>${job.job_type || 'Full-time'}
                </span>
              </div>
            </div>
            <button class="btn-save" title="Save job" data-job-id="${job.id}">
              <i class="bi bi-bookmark"></i>
            </button>
          </div>
        </div>
        
        <!-- Body with Description and Metadata -->
        <div class="job-card-body">
          <p class="text-body mb-3">${job.description || 'No description available'}</p>
          
          <div class="job-meta mb-3">
            <div class="job-meta-item">
              <i class="bi bi-currency-dollar"></i>
              <span>${job.salary ? formatSalary(job.salary) : '$50k - $100k'}</span>
            </div>
            <div class="job-meta-item">
              <i class="bi bi-clock"></i>
              <span>${job.experience || '2-5 years'}</span>
            </div>
            <div class="job-meta-item">
              <i class="bi bi-calendar3"></i>
              <span>Posted ${formatDate(job.created_at)}</span>
            </div>
            <div class="job-meta-item">
              <i class="bi bi-people"></i>
              <span>${job.applicants || Math.floor(Math.random() * 50 + 10)} applicants</span>
            </div>
          </div>
          
          <div class="d-flex gap-2 flex-wrap">
            ${(job.skills || ['Python', 'JavaScript', 'React']).map(skill => 
              `<span class="job-tag">${skill}</span>`
            ).join('')}
          </div>
        </div>
        
        <!-- Footer with Actions -->
        <div class="job-card-footer">
          <div class="d-flex justify-content-between align-items-center">
            <button class="btn btn-sm btn-outline-secondary view-details-btn" data-job-id="${job.id}">
              <i class="bi bi-eye me-1"></i>View Details
            </button>
            ${isApplied 
              ? '<button class="btn btn-sm btn-success" disabled><i class="bi bi-check-circle me-1"></i>Applied</button>'
              : `<button class="btn btn-sm btn-primary apply-btn" data-job-id="${job.id}" data-job-title="${job.title}">
                  <i class="bi bi-send me-1"></i>Apply Now
                 </button>`
            }
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderJobs() {
  const container = document.getElementById('jobsContainer');
  const loadingState = document.getElementById('loadingState');
  const emptyState = document.getElementById('emptyState');
  
  // Hide loading and empty states
  loadingState.style.display = 'none';
  emptyState.style.display = 'none';
  
  if (filteredJobs.length === 0) {
    container.innerHTML = '';
    emptyState.style.display = 'block';
    document.getElementById('jobsDisplayCount').textContent = '0';
    return;
  }
  
  container.innerHTML = filteredJobs.map(job => renderJobCard(job)).join('');
  document.getElementById('jobsDisplayCount').textContent = filteredJobs.length;
  
  // Attach event listeners to Apply buttons
  document.querySelectorAll('.apply-btn').forEach(btn => {
    btn.addEventListener('click', handleApplyClick);
  });
  
  // Attach event listeners to Save buttons
  document.querySelectorAll('.btn-save').forEach(btn => {
    btn.addEventListener('click', handleSaveClick);
  });
  
  // Attach event listeners to View Details buttons
  document.querySelectorAll('.view-details-btn').forEach(btn => {
    btn.addEventListener('click', handleViewDetailsClick);
  });
}

// ==================== Filter Functions ====================

function applyFilters() {
  const searchQuery = document.getElementById('searchInput').value.toLowerCase();
  const locationFilter = document.getElementById('locationFilter').value;
  const experienceFilter = document.getElementById('experienceFilter').value;
  const salaryFilter = document.getElementById('salaryFilter').value;
  
  const jobTypeCheckboxes = {
    'full-time': document.getElementById('fullTime')?.checked,
    'part-time': document.getElementById('partTime')?.checked,
    'contract': document.getElementById('contract')?.checked,
    'internship': document.getElementById('internship')?.checked
  };
  
  const selectedJobTypes = Object.keys(jobTypeCheckboxes).filter(key => jobTypeCheckboxes[key]);
  
  filteredJobs = allJobs.filter(job => {
    // Search filter
    if (searchQuery && !job.title.toLowerCase().includes(searchQuery) && 
        !job.description?.toLowerCase().includes(searchQuery)) {
      return false;
    }
    
    // Location filter
    if (locationFilter && job.location?.toLowerCase() !== locationFilter.toLowerCase()) {
      return false;
    }
    
    // Job type filter
    if (selectedJobTypes.length > 0 && !selectedJobTypes.includes(job.job_type?.toLowerCase())) {
      return false;
    }
    
    // Experience filter
    if (experienceFilter) {
      // Simplified experience filtering
      const jobExperience = job.experience?.toLowerCase() || '';
      if (experienceFilter === 'entry' && !jobExperience.includes('entry') && !jobExperience.includes('0-2')) {
        return false;
      }
      if (experienceFilter === 'mid' && !jobExperience.includes('mid') && !jobExperience.includes('2-5')) {
        return false;
      }
      if (experienceFilter === 'senior' && !jobExperience.includes('senior') && !jobExperience.includes('5-10')) {
        return false;
      }
      if (experienceFilter === 'lead' && !jobExperience.includes('lead') && !jobExperience.includes('10+')) {
        return false;
      }
    }
    
    // Salary filter
    if (salaryFilter && job.salary) {
      const salary = job.salary;
      if (salaryFilter === '0-50k' && (salary < 0 || salary > 50000)) return false;
      if (salaryFilter === '50k-100k' && (salary < 50000 || salary > 100000)) return false;
      if (salaryFilter === '100k-150k' && (salary < 100000 || salary > 150000)) return false;
      if (salaryFilter === '150k+' && salary < 150000) return false;
    }
    
    return true;
  });
  
  renderJobs();
}

function clearFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('locationFilter').value = '';
  document.getElementById('experienceFilter').value = '';
  document.getElementById('salaryFilter').value = '';
  document.getElementById('fullTime').checked = false;
  document.getElementById('partTime').checked = false;
  document.getElementById('contract').checked = false;
  document.getElementById('internship').checked = false;
  
  filteredJobs = [...allJobs];
  renderJobs();
}

// ==================== Sort Function ====================

function sortJobs() {
  const sortBy = document.getElementById('sortSelect').value;
  
  switch(sortBy) {
    case 'recent':
      filteredJobs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      break;
    case 'salary-high':
      filteredJobs.sort((a, b) => (b.salary || 0) - (a.salary || 0));
      break;
    case 'salary-low':
      filteredJobs.sort((a, b) => (a.salary || 0) - (b.salary || 0));
      break;
    case 'applicants':
      filteredJobs.sort((a, b) => (b.applicants || 0) - (a.applicants || 0));
      break;
  }
  
  renderJobs();
}

// ==================== Application Modal ====================

function showApplicationModal(jobId, jobTitle) {
  const modal = new bootstrap.Modal(document.getElementById('applicationModal'));
  document.getElementById('modalJobId').value = jobId;
  document.getElementById('modalJobTitle').value = jobTitle;
  document.getElementById('coverLetter').value = '';
  document.getElementById('resumeLink').value = '';
  modal.show();
}

async function handleApplicationSubmit() {
  const jobId = document.getElementById('modalJobId').value;
  const coverLetter = document.getElementById('coverLetter').value.trim();
  const resumeLink = document.getElementById('resumeLink').value.trim();
  
  if (!coverLetter) {
    alert('Please provide a cover letter');
    return;
  }
  
  const submitBtn = document.getElementById('submitApplicationBtn');
  const originalText = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
  
  const result = await submitApplication({
    job_id: parseInt(jobId),
    cover_letter: coverLetter,
    additional_info: resumeLink
  });
  
  if (result.success) {
    alert('Application submitted successfully!');
    const modal = bootstrap.Modal.getInstance(document.getElementById('applicationModal'));
    modal.hide();
    
    // Refresh applications
    await fetchApplicationsFromAPI();
    updateApplicationsTab();
    updateDashboardStats();
    renderJobs(); // Re-render to update Applied status
  } else {
    alert(`Error: ${result.error}`);
  }
  
  submitBtn.disabled = false;
  submitBtn.innerHTML = originalText;
}

// ==================== Event Handlers ====================

function handleApplyClick(event) {
  const btn = event.currentTarget;
  const jobId = btn.getAttribute('data-job-id');
  const jobTitle = btn.getAttribute('data-job-title');
  showApplicationModal(jobId, jobTitle);
}

function handleSaveClick(event) {
  const btn = event.currentTarget;
  btn.classList.toggle('saved');
  const icon = btn.querySelector('i');
  if (btn.classList.contains('saved')) {
    icon.classList.remove('bi-bookmark');
    icon.classList.add('bi-bookmark-fill');
  } else {
    icon.classList.remove('bi-bookmark-fill');
    icon.classList.add('bi-bookmark');
  }
}

function handleViewDetailsClick(event) {
  const jobId = event.currentTarget.getAttribute('data-job-id');
  alert(`Job Details Modal Coming Soon (Job ID: ${jobId})\n\nThis will be implemented in Phase 3.2`);
}

// ==================== Applications Tab ====================

function updateApplicationsTab() {
  const tableBody = document.getElementById('applicationsTableBody');
  const emptyState = document.getElementById('applicationsEmptyState');
  
  // Update stats
  const totalApps = allApplications.length;
  const pending = allApplications.filter(app => app.status === 'pending' || !app.status).length;
  const accepted = allApplications.filter(app => app.status === 'accepted').length;
  const rejected = allApplications.filter(app => app.status === 'rejected').length;
  
  document.getElementById('totalApplications').textContent = totalApps;
  document.getElementById('pendingApplications').textContent = pending;
  document.getElementById('acceptedApplications').textContent = accepted;
  document.getElementById('rejectedApplications').textContent = rejected;
  
  if (allApplications.length === 0) {
    tableBody.innerHTML = '';
    emptyState.style.display = 'block';
    return;
  }
  
  emptyState.style.display = 'none';
  
  tableBody.innerHTML = allApplications.map(app => {
    const job = allJobs.find(j => j.id === app.job_id);
    const status = app.status || 'pending';
    const statusClass = `status-${status}`;
    
    return `
      <tr>
        <td>
          <strong>${job?.title || `Job #${app.job_id}`}</strong>
        </td>
        <td>${job?.company || 'N/A'}</td>
        <td>${formatDate(app.created_at)}</td>
        <td>
          <span class="status-badge ${statusClass}">${status.toUpperCase()}</span>
        </td>
        <td>
          <button class="btn btn-sm btn-outline-primary" onclick="alert('View Application Details - Coming Soon')">
            <i class="bi bi-eye"></i>
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

// ==================== Initialization ====================

async function loadJobsTab() {
  const loadingState = document.getElementById('loadingState');
  loadingState.style.display = 'block';
  
  await fetchJobsFromAPI();
  renderJobs();
  updateDashboardStats();
}

async function loadApplicationsTab() {
  await fetchApplicationsFromAPI();
  updateApplicationsTab();
  updateDashboardStats();
}

// ==================== Page Load ====================

document.addEventListener('DOMContentLoaded', async function() {
  // Logout button
  document.getElementById('logoutBtn')?.addEventListener('click', function() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
  });
  
  // Load initial data
  await loadJobsTab();
  await loadApplicationsTab();
  
  // Filter event listeners
  document.getElementById('searchBtn')?.addEventListener('click', applyFilters);
  document.getElementById('searchInput')?.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') applyFilters();
  });
  document.getElementById('locationFilter')?.addEventListener('change', applyFilters);
  document.getElementById('experienceFilter')?.addEventListener('change', applyFilters);
  document.getElementById('salaryFilter')?.addEventListener('change', applyFilters);
  document.getElementById('fullTime')?.addEventListener('change', applyFilters);
  document.getElementById('partTime')?.addEventListener('change', applyFilters);
  document.getElementById('contract')?.addEventListener('change', applyFilters);
  document.getElementById('internship')?.addEventListener('change', applyFilters);
  document.getElementById('clearFiltersBtn')?.addEventListener('click', clearFilters);
  
  // Sort event listener
  document.getElementById('sortSelect')?.addEventListener('change', sortJobs);
  
  // Application modal submit
  document.getElementById('submitApplicationBtn')?.addEventListener('click', handleApplicationSubmit);
  
  // Refresh applications button
  document.getElementById('refreshApplicationsBtn')?.addEventListener('click', loadApplicationsTab);
  
  // Tab change events
  document.getElementById('job-listings-tab')?.addEventListener('shown.bs.tab', loadJobsTab);
  document.getElementById('my-applications-tab')?.addEventListener('shown.bs.tab', loadApplicationsTab);
});
