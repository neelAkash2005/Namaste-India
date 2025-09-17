document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  async function postJson(url, data){
  const resp = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data), credentials: 'same-origin'});
  return resp;
  }

  if (loginForm){
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = loginForm.username.value.trim();
      const password = loginForm.password.value;
      const resp = await postJson('/auth/login', {username, password});
      const j = await resp.json();
      if (resp.ok && j.ok){
        alert('Login successful');
        window.location = '/';
      } else {
        alert(j.error || 'Login failed');
      }
    });
  }

  if (signupForm){
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
  const username = signupForm.username.value.trim();
  const password = signupForm.password.value;
  const firstName = signupForm.firstName ? signupForm.firstName.value.trim() : '';
  const lastName = signupForm.lastName ? signupForm.lastName.value.trim() : '';
  const email = signupForm.email ? signupForm.email.value.trim() : '';
  const country = signupForm.country ? signupForm.country.value.trim() : '';
  const resp = await postJson('/auth/signup', {username, password, firstName, lastName, email, country});
      const j = await resp.json();
      if (resp.ok && j.ok){
        alert('Signup successful — you can now login');
        window.location = '/login';
      } else {
        alert(j.error || 'Signup failed');
      }
    });
  }
});
