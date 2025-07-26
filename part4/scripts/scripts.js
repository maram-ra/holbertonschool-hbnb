// Helper function to get JWT token from cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';')[0];
  return null;
}

// Login functionality (used in login.html)
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

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
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed: ' + response.statusText);
        }
      } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed: Could not connect to server');
      }
    });
  }
});

// Behavior on index.html
document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'inline-block';
  }

  if (token) {
    fetchPlaces(token);
  }

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', () => {
      const selectedPrice = priceFilter.value;
      const cards = document.querySelectorAll('.place-card');

      cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        if (selectedPrice === 'All' || price <= parseFloat(selectedPrice)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    const places = await response.json();
    displayPlaces(places);
  } catch (err) {
    console.error(err);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price;

    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price}</p>
      <p>${place.description || ''}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;

    container.appendChild(card);
  });
}
