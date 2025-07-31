// This script handles login, place listing, place details, and review submission.

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const reviewForm = document.getElementById('review-form');
  const currentPath = window.location.pathname;

  // === [TASK 1] Handle Login Form ===
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault(); // Prevent form default submission

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          // Save JWT token in cookies
          document.cookie = `token=${data.access_token}; path=/`;
          // Redirect to index page
          window.location.href = 'index.html';
        } else {
          alert('Login failed: Invalid credentials');
        }
      } catch (error) {
        alert('Login failed: Network error');
      }
    });
  }

  // === [TASK 2] Load Places on Home Page ===
  if (currentPath.includes('index.html')) {
    checkAuthAndLoadPlaces();
    setupPriceFilter();
  }

  // === [TASK 3] Display Place Details ===
  if (currentPath.includes('place.html')) {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById('add-review');

    if (!token && addReviewSection) {
      addReviewSection.style.display = 'none'; // Hide review form for unauthenticated users
    } else if (addReviewSection) {
      addReviewSection.style.display = 'block';
    }

    fetchPlaceDetails(token, placeId);
  }

  // === [TASK 4] Submit Review for a Place ===
  if (currentPath.includes('add_review.html') && reviewForm) {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const reviewText = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            comment: reviewText,
            rating: parseInt(rating),
            place_id: placeId
          })
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          reviewForm.reset();
        } else {
          alert('Failed to submit review');
        }
      } catch (error) {
        alert('Network error while submitting review');
      }
    });
  }
});

// === Helper Functions ===

// Get cookie value by name
function getCookie(name) {
  const cookies = document.cookie.split('; ');
  for (let cookie of cookies) {
    const [key, value] = cookie.split('=');
    if (key === name) return value;
  }
  return null;
}

// Redirect to index.html if no token is found
function checkAuthentication() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
  }
  return token;
}

// Extract place ID from the URL query string
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// Fetch and display details of a single place
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      alert('Failed to load place details');
    }
  } catch (error) {
    alert('Network error while loading details');
  }
}

// Dynamically insert place details and reviews into the page
function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  const reviewsSection = document.getElementById('reviews');
  detailsSection.innerHTML = '';
  reviewsSection.innerHTML = '';

  const container = document.createElement('div');
  container.classList.add('place-details');
  container.innerHTML = `
    <h2>${place.title}</h2>
    <p class="place-info">Host: ${place.host}</p>
    <p class="place-info">Price: $${place.price} / night</p>
    <p class="place-info">${place.description}</p>
    <p class="place-info"><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
  `;
  detailsSection.appendChild(container);

  if (place.reviews && place.reviews.length > 0) {
    place.reviews.forEach((review) => {
      const reviewCard = document.createElement('div');
      reviewCard.classList.add('review-card');
      reviewCard.innerHTML = `
        <p><strong>User ${review.user_id}</strong> - Rating: ${review.rating}</p>
        <p>${review.text}</p>
      `;
      reviewsSection.appendChild(reviewCard);
    });
  } else {
    reviewsSection.innerHTML = `<p>No reviews yet.</p>`;
  }
}


// Fetch and display all places on the homepage
async function checkAuthAndLoadPlaces() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
    return;
  } else {
    if (loginLink) loginLink.style.display = 'none';
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      alert('Failed to fetch places');
    }
  } catch (error) {
    alert('Network error while fetching places');
  }
}

// Create and display place cards dynamically
function displayPlaces(places) {
  console.log('Loaded places:', places);
  const container = document.getElementById('places-list');
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.classList.add('place-card');
    card.setAttribute('data-price', place.price);

    // Use default image if image_url is missing
    const imageUrl = place.image_url || 'images/placeholder.jpg';

    card.innerHTML = `
  <img src="${imageUrl}" alt="${place.title}">
  <span class="place-name">${place.title}</span>
  <div class="place-info">
    <span class="price">$${place.price} / night</span>
    <a class="btn" href="place.html?id=${place.id}">View Details</a>
  </div>
`;

    
    container.appendChild(card);
  });
}


// Setup the price filter dropdown
function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  const options = [10, 50, 100, 'All'];
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt;
    option.textContent = opt;
    filter.appendChild(option);
  });

  filter.addEventListener('change', () => {
    const selected = filter.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseFloat(card.getAttribute('data-price'));
      if (selected === 'All' || price <= parseFloat(selected)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}
