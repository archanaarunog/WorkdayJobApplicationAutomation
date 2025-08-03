document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    email: form.email.value,
    password: form.password.value
  };
  const res = await fetch('http://localhost:8000/api/users/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const msg = document.getElementById('message');
  if (res.ok) {
    const result = await res.json();
    msg.style.color = 'green';
    msg.textContent = 'Login successful!';
    localStorage.setItem('token', result.access_token);
    window.location.href = 'jobs.html';
  } else {
    const err = await res.json();
    msg.style.color = 'red';
    msg.textContent = err.detail || 'Login failed.';
  }
});
