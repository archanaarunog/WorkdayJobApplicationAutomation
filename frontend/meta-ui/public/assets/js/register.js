document.getElementById('registerForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    email: form.email.value,
    password: form.password.value,
    first_name: form.first_name.value,
    last_name: form.last_name.value,
    phone: form.phone.value
  };
  const res = await fetch('http://localhost:8000/api/users/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const msg = document.getElementById('message');
  if (res.ok) {
    msg.style.color = 'green';
    msg.textContent = 'Registration successful! Please login.';
    form.reset();
  } else {
    const err = await res.json();
    msg.style.color = 'red';
    msg.textContent = err.detail || 'Registration failed.';
  }
});
