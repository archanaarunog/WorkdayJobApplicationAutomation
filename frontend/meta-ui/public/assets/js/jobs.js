

// Helper: Create and show a Bootstrap modal for job application
function showApplicationModal(jobId, jobTitle, onSubmit) {
  // Remove any existing modal
  const existing = document.getElementById('applyModal');
  if (existing) existing.remove();

  // Modal HTML (Bootstrap 5)
  const modalHtml = `
    <div class="modal fade" id="applyModal" tabindex="-1" aria-labelledby="applyModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="applyModalLabel">Apply for: ${jobTitle}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form id="applicationForm">
              <div class="mb-3">
                <label for="coverLetter" class="form-label">Cover Letter <span class="text-danger">*</span></label>
                <textarea class="form-control" id="coverLetter" rows="4" required></textarea>
              </div>
              <div class="mb-3">
                <label for="additionalInfo" class="form-label">Additional Info</label>
                <textarea class="form-control" id="additionalInfo" rows="2"></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Submit Application</button>
            </form>
            <div id="applicationMsg" class="mt-3"></div>
          </div>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);

  // Bootstrap modal show
  const modal = new bootstrap.Modal(document.getElementById('applyModal'));
  modal.show();

  // Handle form submit
  document.getElementById('applicationForm').onsubmit = async function(e) {
    e.preventDefault();
    const coverLetter = document.getElementById('coverLetter').value.trim();
    const additionalInfo = document.getElementById('additionalInfo').value.trim();
    if (!coverLetter) {
      document.getElementById('applicationMsg').innerHTML = '<span class="text-danger">Cover letter is required.</span>';
      return;
    }
    // Call the provided onSubmit callback
    await onSubmit({ job_id: jobId, cover_letter: coverLetter, additional_info: additionalInfo });
  };

  // Remove modal from DOM on close
  document.getElementById('applyModal').addEventListener('hidden.bs.modal', function() {
    document.getElementById('applyModal').remove();
  });
}

// Fetch and render jobs, and handle Apply button logic
async function fetchJobs() {
  const token = localStorage.getItem('token');
  const res = await fetch('http://localhost:8000/api/jobs', {
    headers: token ? { 'Authorization': 'Bearer ' + token } : {}
  });
  const container = document.getElementById('jobsContainer');
  if (res.ok) {
    const jobs = await res.json();
    if (jobs.length === 0) {
      container.textContent = 'No jobs available.';
      return;
    }
    container.innerHTML = jobs.map(job => `
      <div class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">${job.title}</h5>
          <p class="card-text">${job.description}</p>
          <p class="card-text"><strong>Location:</strong> ${job.location}</p>
          <button class="btn btn-primary apply-btn" data-jobid="${job.id}" data-jobtitle="${job.title}">Apply</button>
        </div>
      </div>
    `).join('');
    // Add event listeners for Apply buttons
    document.querySelectorAll('.apply-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const jobId = btn.getAttribute('data-jobid');
        const jobTitle = btn.getAttribute('data-jobtitle');
        showApplicationModal(jobId, jobTitle, async (appData) => {
          // POST application to backend
          const token = localStorage.getItem('token');
          const resp = await fetch('http://localhost:8000/api/applications/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...(token ? { 'Authorization': 'Bearer ' + token } : {})
            },
            body: JSON.stringify(appData)
          });
          const msgDiv = document.getElementById('applicationMsg');
          if (resp.ok) {
            msgDiv.innerHTML = '<span class="text-success">Application submitted successfully!</span>';
            btn.disabled = true;
            btn.textContent = 'Applied';
            setTimeout(() => {
              const modal = bootstrap.Modal.getInstance(document.getElementById('applyModal'));
              modal.hide();
            }, 1200);
          } else {
            const err = await resp.json();
            msgDiv.innerHTML = `<span class="text-danger">${err.detail || 'Failed to apply.'}</span>`;
          }
        });
      });
    });
  } else {
    container.textContent = 'Failed to load jobs.';
  }
}

// Logout button handler
document.addEventListener('DOMContentLoaded', function() {
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      localStorage.removeItem('token');
      window.location.href = 'login.html';
    });
  }
  fetchJobs();
});
