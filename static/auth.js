document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const passwordInput = document.querySelector('#signup-form input[name="password"], #login-form input[name="password"]');
  const resultEl = document.createElement('p');

  // Attach result paragraph just below the password field (only if passwordInput exists)
  if (passwordInput) {
    resultEl.id = 'password-strength';
    resultEl.style.fontWeight = 'bold';
    passwordInput.insertAdjacentElement('afterend', resultEl);

    passwordInput.addEventListener('input', () => {
      checkStrength(passwordInput.value);
    });
  }

  function checkStrength(password) {
    const lengthError = password.length < 8;
    const uppercaseError = !/[A-Z]/.test(password);
    const lowercaseError = !/[a-z]/.test(password);
    const digitError = !/[0-9]/.test(password);
    const specialCharError = !/[!@#$%^&*(),.?":{}|<>]/.test(password);

    const score = 5 - [
      lengthError,
      uppercaseError,
      lowercaseError,
      digitError,
      specialCharError
    ].filter(Boolean).length;

    let resultText = "";
    let color = "";

    if (!password) {
      resultEl.textContent = "";
      return;
    }

    if (score === 5) {
      resultText = "Strong Password";
      color = "green";
    } else if (score >= 3) {
      resultText = "Medium Password. Use special characters and numbers.";
      color = "orange";
    } else {
      resultText = "Weak Password. Consider using a longer password with a mix of characters and numbers.";
      color = "red";
    }

    resultEl.textContent = resultText;
    resultEl.style.color = color;
  }

  async function postJson(url, data){
    const resp = await fetch(url, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(data),
      credentials: 'same-origin'
    });
    return resp;
  }

  if (loginForm){
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = loginForm.username.value.trim();
      const password = loginForm.password.value;
      const resp = await postJson('/auth/login', {username, password});
      const j = await resp.json().catch(()=>({}));
      if (resp.ok && j.ok){
        alert('Login successful');
        // === NEW: store username locally so index.html can show it immediately ===
        try { localStorage.setItem('username', username); } catch (err) { /* ignore */ }
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
      const j = await resp.json().catch(()=>({}));
      if (resp.ok && j.ok){
        alert('Signup successful — you can now login');
        window.location = '/login';
      } else {
        alert(j.error || 'Signup failed');
      }
    });
  }
});
