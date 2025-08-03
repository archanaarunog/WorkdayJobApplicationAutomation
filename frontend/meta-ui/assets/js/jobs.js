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
      <div class="card mb-3 shadow-sm">
        <div class="card-body">
          <h3 class="card-title">${job.title}</h3>
          <p class="card-text">${job.description}</p>
          <p class="card-text"><strong>Location:</strong> ${job.location}</p>
          <button class="btn btn-primary apply-btn" data-jobid="${job.id}">Apply</button>
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
