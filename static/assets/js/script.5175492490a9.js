/* =========================================
   1. PARTICLES & NAVIGATION (jQuery)
   ========================================= */
$(document).ready(function() {
    // Close mobile navbar when a link is clicked
    $('.navbar-nav>li>a').on('click', function() {
        $('.navbar-collapse').collapse('hide');
    });

    // NOTE: I removed the jQuery smooth scroll that was likely crashing your code
    // because 'easeInOutExpo' was missing. The "Vanilla JS" version below is safer.
});

/* =========================================
   2. PARTICLES JS CONFIGURATION
   ========================================= */
// Wrap in try-catch to prevent crashing if particles.js isn't loaded
try {
    particlesJS("particles-js", {    "particles": {
        "number": {
            "value": 80,
            "density": {
                "enable": true,
                "value_area": 800
            }
        },
        "color": {
            "value": "#ffffff"
        },
        "shape": {
            "type": "circle",
            "stroke": {
                "width": 0,
                "color": "#000000"
            },
            "polygon": {
                "nb_sides": 5
            },
            "image": {
                "src": "img/github.svg",
                "width": 100,
                "height": 100
            }
        },
        "opacity": {
            "value": 2,
            "random": false,
            "anim": {
                "enable": false,
                "speed": 1,
                "opacity_min": 0.1,
                "sync": false
            }
        },
        "size": {
            "value": 7,
            "random": true,
            "anim": {
                "enable": false,
                "speed": 40,
                "size_min": 0.1,
                "sync": false
            }
        },
        "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 1.9,
            "width": 1.5
        },
        "move": {
            "enable": true,
            "speed": 6,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": false,
            "attract": {
                "enable": false,
                "rotateX": 600,
                "rotateY": 1200
            }
        }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": {
                "enable": true,
                "mode": "repulse"
            },
            "onclick": {
                "enable": true,
                "mode": "push"
            },
            "resize": true
        },
        "modes": {
            "grab": {
                "distance": 400,
                "line_linked": {
                    "opacity": 1
                }
            },
            "bubble": {
                "distance": 400,
                "size": 40,
                "duration": 2,
                "opacity": 8,
                "speed": 3
            },
            "repulse": {
                "distance": 200,
                "duration": 0.4
            },
            "push": {
                "particles_nb": 4
            },
            "remove": {
                "particles_nb": 2
            }
        }
    },
    "retina_detect": true
});

} catch (e) {
    console.log("Particles.js not loaded, skipping.");
}

/* =========================================
   3. MAIN INTERACTIVITY (Vanilla JS)
   ========================================= */
document.addEventListener("DOMContentLoaded", () => {

    // --- A. Navbar Hide/Show on Scroll ---
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');

    if (navbar) { // Safety check
        window.addEventListener('scroll', function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollTop > lastScrollTop) {
                navbar.classList.add('navbar-hidden'); // Scroll Down
            } else {
                navbar.classList.remove('navbar-hidden'); // Scroll Up
            }
            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        });

        // Show navbar when mouse is near top
        document.addEventListener('mousemove', function(e) {
            if (e.clientY <= 50) navbar.classList.remove('navbar-hidden');
        });
    }


    // --- B. Smooth Scroll (The Working Version) ---
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            const targetId = link.getAttribute("href").substring(1);
            if (!targetId) return; // Skip if href="#"

            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                event.preventDefault();
                const offsetTop = targetElement.getBoundingClientRect().top + window.scrollY; // More reliable calculation
                window.scrollTo({
                    top: offsetTop,
                    behavior: "smooth"
                });
            }
        });
    });


    // --- C. Scroll Arrow Visibility ---
    const arrow = document.querySelector('.scroll-arrow');
    const homeSection = document.getElementById('home');
    if (arrow && homeSection) {
        function checkScroll() {
            const rect = homeSection.getBoundingClientRect();
            // Show arrow if home is still somewhat visible
            if (rect.bottom >= 0) {
                arrow.style.display = 'block';
            } else {
                arrow.style.display = 'none';
            }
        }
        window.addEventListener('scroll', checkScroll);
        checkScroll();
    }


    // --- D. Section Highlighting ---
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    function revealSection() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - sectionHeight / 3) {
                current = section.getAttribute('id');
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current) && current !== '') {
                link.classList.add('active');
            }
        });
    }
    window.addEventListener('scroll', revealSection);


    // --- E. Progress Bars ---
    const skillContainers = document.querySelectorAll(".skill-container .progress-bar");

    function handleProgressBar() {
        skillContainers.forEach(function(bar) {
            const rect = bar.getBoundingClientRect();
            const inView = (rect.top >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight));

            if (inView && !bar.classList.contains('filled')) {
                bar.classList.add('filled');
                const targetWidth = bar.getAttribute('data-width'); // e.g. "80%"
                // Simple CSS transition is better than setInterval for performance
                bar.style.width = targetWidth + "%";
            }
        });
    }
    window.addEventListener("scroll", handleProgressBar);


    // --- F. NUMBER COUNTERS (The Fix) ---
    const counters = document.querySelectorAll(".counter");
    const animationDuration = 1000; // 2 seconds

    const startCounter = (counter) => {
        // Safe check for data-target
        const targetAttr = counter.getAttribute('data-target');
        if (!targetAttr) return; // Skip if no number provided

        const target = +targetAttr;
        const startTime = performance.now();

        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / animationDuration, 1);

            // Calculate current number
            counter.innerText = Math.floor(progress * target);

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                counter.innerText = target;
            }
        };
        requestAnimationFrame(update);
    };

    const observer = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    counters.forEach(counter => observer.observe(counter));

});