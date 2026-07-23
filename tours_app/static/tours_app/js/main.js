// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
});

// Auto dismiss alerts
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// Seat validation
document.querySelector('input[name="number_of_seats"]')?.addEventListener('change', function() {
    const available = parseInt(this.dataset.available || 10);
    if (parseInt(this.value) > available) {
        alert(`Only ${available} seats available!`);
        this.value = available;
    }
    if (parseInt(this.value) < 1) {
        this.value = 1;
    }
});
