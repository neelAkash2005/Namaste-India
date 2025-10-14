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
  const monthInput = document.getElementById('month-input');
  const durationInput = document.getElementById('duration-input');
  const go = document.getElementById('go');
  const status = document.getElementById('status');
  const results = document.getElementById('results');

  // Safety check - ensure all elements exist
  if (!monthInput || !durationInput || !go || !status || !results) {
    console.error('Recommender elements not found!', {
      monthInput: !!monthInput,
      durationInput: !!durationInput,
      go: !!go,
      status: !!status,
      results: !!results
    });
    return;
  }

  console.log('✅ Recommender initialized successfully!');

  go.addEventListener('click', async () => {
    console.log('🔍 Button clicked!');
    const month = monthInput.value.trim();
    const duration = durationInput.value.trim();
    
    console.log('Search params:', { month, duration });
    
    if (!month) {
      status.textContent = '⚠️ Please enter a month to get recommendations.';
      return;
    }
    
    status.textContent = '🔍 Finding the best destinations for you...';
    results.innerHTML = '';
    
    try {
      let url = `/recommend?month=${encodeURIComponent(month)}`;
      if (duration) {
        url += `&duration=${encodeURIComponent(duration)}`;
      }
      url += '&topn=10'; // Always show top 10 results
      
      console.log('API URL:', url);
      
      const resp = await fetch(url);
      
      console.log('Response status:', resp.status);
      
      if (!resp.ok) {
        const err = await resp.json();
        status.textContent = err.error || '❌ Request failed';
        return;
      }
      
      const data = await resp.json();
      
      console.log('API Response:', data);
      
      if (!data.results || data.results.length === 0) {
        status.textContent = '😔 No cities found matching your criteria. Try a different month or duration.';
        results.innerHTML = '';
        return;
      }
      
      // Show note if exists (e.g., duration too long)
      if (data.note) {
        status.textContent = `ℹ️ ${data.note}`;
      } else {
        status.textContent = `✨ Found ${data.count} amazing destination${data.count > 1 ? 's' : ''} for ${data.query.month}${data.query.duration ? ' (' + data.query.duration + ' days)' : ''}`;
      }
      
      // Create beautiful cards for each result
      const container = document.createElement('div');
      container.className = 'results-grid';
      
      data.results.forEach((r, idx) => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
          <div class="card-rank">#${idx + 1}</div>
          <h3>${r.city}</h3>
          <div class="card-rating">⭐ ${r.rating.toFixed(1)}</div>
          <div class="card-info">
            <div><strong>📅 Best Time:</strong> ${r.best_time}</div>
            <div><strong>⏱️ Ideal Duration:</strong> ${r.ideal_duration}</div>
          </div>
          <p class="card-desc">${r.description}</p>
        `;
        container.appendChild(card);
      });
      
      results.appendChild(container);
      console.log('✅ Results displayed!');
    } catch (e) {
      console.error('Error:', e);
      status.textContent = '❌ ' + (e.message || 'Request failed. Please try again.');
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
