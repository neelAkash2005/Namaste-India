// Check authentication status
function checkAuth() {
    const userData = JSON.parse(localStorage.getItem('userData'));
    if (!userData) {
        window.location.href = 'login.html';
        return null;
    }
    return userData;
}

// Profile Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const userData = checkAuth();
    if (!userData) return;

    // Initialize profile
    initializeProfile(userData);
    setupEventListeners();
    loadWishlist();
    loadTrips();
    updateStats();
});

function initializeProfile(userData) {
    // Update profile header
    document.querySelector('.profile-name').textContent = `${userData.firstName} ${userData.lastName}`;
    document.querySelector('.profile-email').textContent = userData.email;
    document.getElementById('userCountry').textContent = userData.country || 'Not specified';

    // Update personal information
    document.getElementById('firstName').textContent = userData.firstName;
    document.getElementById('lastName').textContent = userData.lastName;
    document.getElementById('email').textContent = userData.email;
    document.getElementById('username').textContent = userData.username;

    // Set theme based on user preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    document.body.classList.toggle('dark-mode', isDarkMode);
    if (document.getElementById('darkModeToggle')) {
        document.getElementById('darkModeToggle').checked = isDarkMode;
    }
}

function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Logout button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

function toggleTheme() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    if (document.getElementById('darkModeToggle')) {
        document.getElementById('darkModeToggle').checked = isDarkMode;
    }
}

function handleLogout() {
    localStorage.removeItem('userData');
    window.location.href = 'login.html';
}

function openEditModal() {
    const userData = checkAuth();
    if (!userData) return;

    const modal = document.getElementById('editProfileModal');
    const form = document.getElementById('editProfileForm');

    // Pre-fill form
    form.firstName.value = userData.firstName;
    form.lastName.value = userData.lastName;
    form.email.value = userData.email;
    form.country.value = userData.country || '';

    modal.classList.add('active');
}

function closeEditModal() {
    document.getElementById('editProfileModal').classList.remove('active');
}

function handleProfileUpdate(e) {
    e.preventDefault();
    const userData = checkAuth();
    if (!userData) return;

    const formData = new FormData(e.target);
    const updatedData = {
        ...userData,
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
        email: formData.get('email'),
        country: formData.get('country')
    };

    localStorage.setItem('userData', JSON.stringify(updatedData));
    initializeProfile(updatedData);
    closeEditModal();
}

function loadWishlist() {
    const wishlistGrid = document.querySelector('.wishlist-grid');
    if (!wishlistGrid) return;

    // Example wishlist data - replace with actual data
    const wishlistItems = [
        { id: 1, name: 'Taj Mahal, Agra', image: 'images/delhi.jpg', description: 'Symbol of eternal love' },
        { id: 2, name: 'Beaches of Goa', image: 'images/goa.jpg', description: 'Sun, sand and serenity' }
    ];

    wishlistGrid.innerHTML = wishlistItems.map(item => `
        <div class="wishlist-card" data-id="${item.id}">
            <img src="${item.image}" alt="${item.name}">
            <div class="wishlist-content">
                <h3>${item.name}</h3>
                <p>${item.description}</p>
                <button class="remove-wishlist" onclick="removeFromWishlist(${item.id})">
                    <span class="material-icons">delete</span>
                    Remove
                </button>
            </div>
        </div>
    `).join('');
}

function loadTrips() {
    const tripsTimeline = document.querySelector('.trips-timeline');
    if (!tripsTimeline) return;

    // Example trips data - replace with actual data
    const trips = [
        { id: 1, destination: 'Mumbai', date: '2025-10-15', status: 'upcoming' },
        { id: 2, destination: 'Delhi', date: '2025-09-01', status: 'completed' }
    ];

    tripsTimeline.innerHTML = trips.map(trip => `
        <div class="trip-card ${trip.status}">
            <div class="trip-date">${formatDate(trip.date)}</div>
            <div class="trip-content">
                <h3>${trip.destination}</h3>
                <span class="trip-status">${trip.status}</span>
            </div>
        </div>
    `).join('');
}

function updateStats() {
    // Example stats - replace with actual data
    const stats = {
        placesVisited: 5,
        wishlistItems: 8,
        reviews: 12
    };

    document.querySelectorAll('.stat-value').forEach((stat, index) => {
        const value = Object.values(stats)[index];
        animateNumber(stat, 0, value, 1500);
    });
}

function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const animate = () => {
        current += increment;
        element.textContent = Math.round(current);
        
        if (current < end) {
            requestAnimationFrame(animate);
        } else {
            element.textContent = end;
        }
    };

    animate();
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Initialize event listeners for forms
document.getElementById('editProfileForm')?.addEventListener('submit', handleProfileUpdate);

function updateProfileInfo(userData) {
    // Update profile header
    document.querySelector('.profile-name').textContent = `${userData.firstName} ${userData.lastName}`;
    document.querySelector('.profile-email').textContent = userData.email;
    document.querySelector('.profile-location').textContent = userData.country || 'Location not set';

    // Update details tab
    document.getElementById('firstName').textContent = userData.firstName;
    document.getElementById('lastName').textContent = userData.lastName;
    document.getElementById('email').textContent = userData.email;
    document.getElementById('country').textContent = userData.country || 'Not specified';
}

function handleEditProfile() {
    const userData = JSON.parse(localStorage.getItem('userData'));
    
    // Create modal HTML
    const modalHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <h2>Edit Profile</h2>
                <form id="edit-profile-form">
                    <div class="field">
                        <label>First Name</label>
                        <input type="text" name="firstName" value="${userData.firstName}" required>
                    </div>
                    <div class="field">
                        <label>Last Name</label>
                        <input type="text" name="lastName" value="${userData.lastName}" required>
                    </div>
                    <div class="field">
                        <label>Email</label>
                        <input type="email" name="email" value="${userData.email}" required>
                    </div>
                    <div class="field">
                        <label>Country</label>
                        <input type="text" name="country" value="${userData.country || ''}">
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="btn-ghost" onclick="closeEditModal()">Cancel</button>
                        <button type="submit" class="btn-primary">Save Changes</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Add form submit handler
    const form = document.getElementById('edit-profile-form');
    form.addEventListener('submit', handleProfileUpdate);
}

function closeEditModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.remove();
    }
}

function handleProfileUpdate(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const updatedData = Object.fromEntries(formData.entries());
    
    // Update localStorage
    const userData = JSON.parse(localStorage.getItem('userData'));
    const newUserData = { ...userData, ...updatedData };
    localStorage.setItem('userData', JSON.stringify(newUserData));

    // Update the UI
    updateProfileInfo(newUserData);

    // Close modal
    closeEditModal();
}

function loadWishlist() {
    const wishlistContainer = document.querySelector('.wishlist-grid');
    
    // Example wishlist data - replace with actual data from your backend
    const wishlistItems = [
        {
            image: 'images/delhi.jpg',
            title: 'Delhi',
            description: 'The capital city with rich history'
        },
        {
            image: 'images/goa.jpg',
            title: 'Goa',
            description: 'Beautiful beaches and vibrant culture'
        }
    ];

    wishlistItems.forEach(item => {
        const itemHTML = `
            <div class="wishlist-item">
                <img src="${item.image}" alt="${item.title}" class="wishlist-img">
                <div class="wishlist-info">
                    <h3 class="wishlist-title">${item.title}</h3>
                    <p class="muted">${item.description}</p>
                    <button class="btn-ghost">Remove from Wishlist</button>
                </div>
            </div>
        `;
        wishlistContainer.insertAdjacentHTML('beforeend', itemHTML);
    });
}

function loadTrips() {
    const tripsContainer = document.querySelector('.trips-timeline');
    
    // Example trips data - replace with actual data from your backend
    const trips = [
        {
            destination: 'Mumbai',
            date: '2025-08-15',
            status: 'Upcoming'
        },
        {
            destination: 'Jaipur',
            date: '2025-07-01',
            status: 'Completed'
        }
    ];

    trips.forEach(trip => {
        const tripHTML = `
            <div class="trip-item">
                <h3>${trip.destination}</h3>
                <p class="muted">Date: ${trip.date}</p>
                <span class="status-badge ${trip.status.toLowerCase()}">${trip.status}</span>
            </div>
        `;
        tripsContainer.insertAdjacentHTML('beforeend', tripHTML);
    });
}
