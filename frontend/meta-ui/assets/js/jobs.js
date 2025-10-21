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
      <div class="card mb-4 card-shadow" style="border: 1px solid var(--border-light); border-radius: var(--radius-lg); transition: transform var(--transition-normal), box-shadow var(--transition-normal);">
        <div class="card-body" style="background-color: var(--background-white);">
          <h3 class="card-title" style="color: var(--text-purple); font-weight: 600;">${job.title}</h3>
          <p class="card-text" style="color: var(--text-dark); margin: var(--spacing-sm) 0;">${job.description}</p>
          <p class="card-text" style="color: var(--text-light); font-size: 0.9rem;"><strong style="color: var(--text-purple);">Location:</strong> ${job.location}</p>
          <button class="btn btn-primary apply-btn mt-2" data-jobid="${job.id}">Apply Now</button>
        </div>
      </div>
    `).join('');
    // Add event listeners for Apply buttons
    document.querySelectorAll('.apply-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        alert('Apply functionality coming in v1.1!');
      });
    });
  } else {
    container.textContent = 'Failed to load jobs.';
  }
// End of file

// Add logout button to navbar or top of page
function addLogoutButton() {
  const container = document.querySelector('.container');
  if (!container) return;
  const logoutBtn = document.createElement('button');
  logoutBtn.textContent = 'Logout';
  logoutBtn.className = 'btn btn-danger float-end mb-3';
  logoutBtn.onclick = function() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
  };
  container.prepend(logoutBtn);
}

addLogoutButton();
}
fetchJobs();
