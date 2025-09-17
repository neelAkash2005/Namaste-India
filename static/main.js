document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  const mobileToggle = document.getElementById('mobile-nav-toggle');
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      const nav = document.querySelector('.main-nav');
      if (nav) nav.classList.toggle('open');
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href.length > 1) {
        e.preventDefault();
        const el = document.querySelector(href);
        if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
      }
    });
  });

  /* ---------- Recommender ---------- */
  const cityInput = document.getElementById('city-input');
  const topnInput = document.getElementById('topn-input');
  const go = document.getElementById('go');
  const status = document.getElementById('status');
  const results = document.getElementById('results');

  go.addEventListener('click', async () => {
    const city = cityInput.value.trim();
    const topn = Math.max(1, parseInt(topnInput.value) || 5);
    if (!city) {
      status.textContent = 'Please enter a city name.';
      return;
    }
    status.textContent = 'Loading...';
    results.innerHTML = '';
    try {
      const resp = await fetch(`/recommend?city=${encodeURIComponent(city)}&topn=${topn}`);
      if (!resp.ok) {
        const err = await resp.json();
        status.textContent = err.error || 'Request failed';
        return;
      }
      const data = await resp.json();
      status.textContent = `Results for ${data.query_city}`;
      if (!data.results || data.results.length === 0) {
        results.innerHTML = '<p>No recommendations found.</p>';
        return;
      }
      const ul = document.createElement('ol');
      data.results.forEach(r => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${r.city}</strong> — ${r.Score || r.score}
                        (${r[Object.keys(r).find(k => k !== 'city' && k !== 'score')] || ''})`;
        ul.appendChild(li);
      });
      results.appendChild(ul);
    } catch (e) {
      status.textContent = e.message || 'Request failed';
    }
  });

  /* ---------- Settings (Dark Mode & Zoom) ---------- */
  const settingsBtn = document.getElementById('settings-btn');
  const settingsMenu = document.getElementById('settings-menu');
  const darkToggle = document.getElementById('dark-toggle');
  const zoomIn = document.getElementById('zoom-in');
  const zoomOut = document.getElementById('zoom-out');

  if (settingsBtn && settingsMenu) {
    settingsBtn.addEventListener('click', () => {
      const isHidden = settingsMenu.classList.toggle('hidden');
      settingsMenu.setAttribute('aria-hidden', isHidden ? 'true' : 'false');
    });
  }

  // initialize dark mode from localStorage
  const saved = localStorage.getItem('site-dark-mode');
  if (saved !== null) {
    const enabled = saved === '1';
    document.body.classList.toggle('dark-mode', enabled);
    if (darkToggle) darkToggle.checked = enabled;
  }

  if (darkToggle) {
    darkToggle.addEventListener('change', () => {
      const enabled = !!darkToggle.checked;
      document.body.classList.toggle('dark-mode', enabled);
      try { localStorage.setItem('site-dark-mode', enabled ? '1' : '0'); } catch (e) { /* ignore */ }
    });
  }

  let zoomLevel = 100;
  function setZoom() { document.body.style.zoom = zoomLevel + '%'; }
  if (zoomIn) zoomIn.addEventListener('click', () => { zoomLevel += 10; setZoom(); });
  if (zoomOut) zoomOut.addEventListener('click', () => { zoomLevel = Math.max(50, zoomLevel - 10); setZoom(); });

  /* ---------- Dummy Chat Bot ---------- */
  const chatToggle = document.getElementById('chat-toggle');
  const chatWindow = document.getElementById('chat-window');
  chatToggle.addEventListener('click', () => {
    chatWindow.classList.toggle('hidden');
  });

  /* ---------- Auth header (show Sign out when logged in) ---------- */
  async function refreshAuthArea(){
    try{
      const resp = await fetch('/auth/whoami', {credentials:'same-origin'});
      const j = await resp.json();
      const authArea = document.getElementById('auth-area');
      if (!authArea) return;
      authArea.innerHTML = '';
      if (j && j.ok){
        // show username and sign out
        const span = document.createElement('span');
        span.textContent = j.username;
        span.style.marginRight = '8px';
        const outBtn = document.createElement('button');
        outBtn.className = 'btn btn-ghost';
        outBtn.textContent = 'Sign out';
        outBtn.addEventListener('click', async () => {
          await fetch('/auth/logout', {method:'POST', credentials:'same-origin'});
          // refresh the header
          refreshAuthArea();
          // optionally redirect to home
          window.location = '/';
        });
        authArea.appendChild(span);
        authArea.appendChild(outBtn);
      } else {
        const a1 = document.createElement('a'); a1.className='btn btn-ghost'; a1.href='/login'; a1.textContent='Login';
        const a2 = document.createElement('a'); a2.className='btn btn-primary'; a2.href='/signup'; a2.textContent='Sign up';
        authArea.appendChild(a1); authArea.appendChild(a2);
        // keep settings button separate in the header (do not recreate it here)
      }
    }catch(e){
      // ignore
    }
  }

  refreshAuthArea();
});
