/**
 * AI SHOP - Main JavaScript
 * Interactive features and enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    // ====== Sticky Navbar Shadow ======
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ====== Smooth Scroll for Navigation Links ======
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ====== Star Rating Input Animation ======
    const starLabels = document.querySelectorAll('.star-label');
    starLabels.forEach(label => {
        label.addEventListener('mouseover', function() {
            const index = Array.from(starLabels).indexOf(this);
            starLabels.forEach((l, i) => {
                if (i >= index) {
                    l.style.color = '#ffc107';
                } else {
                    l.style.color = '#ddd';
                }
            });
        });
    });

    document.querySelector('.rating-input')?.addEventListener('mouseout', function() {
        starLabels.forEach(l => {
            l.style.color = '#ddd';
        });
        const checkedIndex = Array.from(document.querySelectorAll('.rating-input input')).findIndex(i => i.checked);
        if (checkedIndex !== -1) {
            starLabels.forEach((l, i) => {
                if (i >= checkedIndex) {
                    l.style.color = '#ffc107';
                }
            });
        }
    });

    // ====== Wishlist Button Toggle ======
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            icon.classList.toggle('bi-heart');
            icon.classList.toggle('bi-heart-fill');
        });
    });

    // ====== Product Image Zoom on Hover ======
    const productImages = document.querySelectorAll('.product-image-wrapper');
    productImages.forEach(wrapper => {
        wrapper.addEventListener('mousemove', function(e) {
            const img = this.querySelector('.product-image');
            if (img) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const xPercent = (x / rect.width) * 100;
                const yPercent = (y / rect.height) * 100;
                
                img.style.transformOrigin = `${xPercent}% ${yPercent}%`;
            }
        });

        wrapper.addEventListener('mouseleave', function() {
            const img = this.querySelector('.product-image');
            if (img) {
                img.style.transformOrigin = 'center center';
            }
        });
    });

    // ====== Gallery Thumbnail Click ======
    document.querySelectorAll('.gallery-thumb').forEach(thumb => {
        thumb.addEventListener('click', function() {
            const src = this.querySelector('img').src;
            const mainImg = document.querySelector('.product-detail-image');
            if (mainImg) {
                mainImg.src = src;
                mainImg.style.animation = 'none';
                setTimeout(() => {
                    mainImg.style.animation = 'fadeInUp 0.4s ease';
                }, 10);
            }
            
            // Update active state
            document.querySelectorAll('.gallery-thumb').forEach(t => {
                t.style.borderColor = 'transparent';
            });
            this.style.borderColor = 'var(--primary-color)';
        });
    });

    // ====== Add To Cart Button Animation ======
    document.querySelectorAll('.btn-primary, .btn-success').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (this.textContent.includes('Add to Cart') || this.textContent.includes('Cart')) {
                // Create ripple effect
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            }
        });
    });

    // ====== Form Validation ======
    const forms = document.querySelectorAll('.review-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const textarea = this.querySelector('textarea');
            if (!textarea || textarea.value.trim() === '') {
                e.preventDefault();
                alert('Please write a review before submitting.');
                textarea?.focus();
            }
        });
    });

    // ====== Search Input Focus Animation ======
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.parentElement.style.boxShadow = '0 0 0 0.2rem rgba(13, 110, 253, 0.15)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.parentElement.style.boxShadow = 'none';
        });
    }

    // ====== Product Card Lazy Load ======
    if ('IntersectionObserver' in window) {
        const images = document.querySelectorAll('.product-image');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.style.opacity = '1';
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => {
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.3s ease';
            imageObserver.observe(img);
        });
    }

    // ====== Number Input Spinner ======
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            if (this.value > 999) this.value = 999;
        });
    });

    // ====== Alert Auto Dismiss ======
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    console.log('AI Shop - Platform loaded successfully! 🎉');
});

// ====== Ripple Effect CSS (via JavaScript) ======
if (!document.querySelector('style[data-ripple]')) {
    const style = document.createElement('style');
    style.setAttribute('data-ripple', 'true');
    style.textContent = `
        .btn {
            position: relative;
        }
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}
