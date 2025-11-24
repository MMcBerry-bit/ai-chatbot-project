// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all feature cards and demo items
document.querySelectorAll('.feature-card, .demo-item, .doc-card, .step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Copy code to clipboard
document.querySelectorAll('code').forEach(code => {
    code.style.cursor = 'pointer';
    code.title = 'Click to copy';
    
    code.addEventListener('click', () => {
        navigator.clipboard.writeText(code.textContent);
        
        // Visual feedback
        const originalText = code.textContent;
        code.textContent = '✓ Copied!';
        setTimeout(() => {
            code.textContent = originalText;
        }, 1500);
    });
});

// Track download clicks
document.querySelectorAll('a[href*="download"], a[href*="archive"]').forEach(link => {
    link.addEventListener('click', () => {
        console.log('Download initiated:', link.href);
        // You can add analytics here
    });
});
