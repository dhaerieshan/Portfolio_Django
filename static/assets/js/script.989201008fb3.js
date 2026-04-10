
// Smooth scrolling for navigation links
$(document).ready(function(){
    $(".nav-link").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 1000, 'easeInOutExpo', function(){
                window.location.hash = hash;
            });
        }
    });

    // Smooth scrolling for overlay links
    $(".overlay-link").click(function() {
        var target = $(this).data('target');
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 1000);
    });
});

// ParticlesJS configuration
particlesJS("particles-js", {
    "particles": {
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

// Hide and show navbar on scroll
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

document.addEventListener('mousemove', function (e) {
    if (e.clientY <= 50) {
        navbar.classList.remove('navbar-hidden');
    }
});

document.addEventListener('scroll', function () {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        // Scroll Down
        navbar.classList.add('navbar-hidden');
    } else {
        // Scroll Up
        navbar.classList.remove('navbar-hidden');
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
});

document.addEventListener('touchmove', function (e) {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        // Scroll Down
        navbar.classList.add('navbar-hidden');
    } else {
        // Scroll Up
        navbar.classList.remove('navbar-hidden');
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
}, { passive: true });

// Section highlight on scroll
document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    function revealSection() {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (pageYOffset >= sectionTop - sectionHeight / 3) {
                current = section.getAttribute('id');
                section.classList.add('active');
            } else {
                section.classList.remove('active');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', revealSection);

    // Initial reveal for sections in the viewport
    revealSection();
});

// Scroll arrow visibility
document.addEventListener('DOMContentLoaded', function () {
    const arrow = document.querySelector('.scroll-arrow');

    if (arrow) { // Ensure the arrow element exists
        function checkScroll() {
            const homeSection = document.getElementById('home');
            const rect = homeSection.getBoundingClientRect();

            if (rect.top <= 0 && rect.bottom >= window.innerHeight) {
                arrow.style.display = 'block';
            } else {
                arrow.style.display = 'none';
            }
        }

        window.addEventListener('scroll', checkScroll);
        window.addEventListener('resize', checkScroll);

        checkScroll();  // Initial check
    }
});

// Smooth scroll for hash links
document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll('a[href^="#"]');

    for (const link of links) {
      link.addEventListener('click', function(event) {
        event.preventDefault();

        const targetId = link.getAttribute("href").substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop,
            behavior: "smooth"
          });
        }
      });
    }
});

// Progress bars fill on scroll into view
document.addEventListener("DOMContentLoaded", function() {
    function move(bar, targetWidth) {
        let width = 1;
        let id = setInterval(frame, 10);
        function frame() {
            if (width >= targetWidth) {
                clearInterval(id);
            } else {
                width++;
                bar.style.width = width + "%";
            }
        }
    }

    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function handleScroll() {
        const skillContainers = document.querySelectorAll(".skill-container .progress-bar");
        skillContainers.forEach(function(bar) {
            if (isElementInViewport(bar) && !bar.classList.contains('filled')) {
                const targetWidth = parseInt(bar.getAttribute('data-width'));
                move(bar, targetWidth);
                bar.classList.add('filled'); // Add class to mark as filled
            }
        });
    }

    window.addEventListener("scroll", handleScroll);
    handleScroll();  // Trigger once to check the initial viewport
});
$(document).ready(function () {
    $('.navbar-nav>li>a').on('click', function(){
        $('.navbar-collapse').collapse('hide');
    });
});