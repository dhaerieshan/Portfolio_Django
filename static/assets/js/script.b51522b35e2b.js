// ==========================
// SMOOTH SCROLLING
// ==========================
$(document).ready(function () {
    $(".nav-link").on("click", function (event) {
        if (this.hash !== "") {
            event.preventDefault();
            const hash = this.hash;
            $("html, body").animate(
                { scrollTop: $(hash).offset().top },
                1000,
                "easeInOutExpo",
                function () {
                    window.location.hash = hash;
                }
            );
        }
    });

    $(".overlay-link").click(function () {
        const target = $(this).data("target");
        $("html, body").animate(
            { scrollTop: $(target).offset().top },
            1000
        );
    });
});

// ==========================
// PARTICLES (DARK / LIGHT)
// ==========================
function loadParticles(isDark) {
    particlesJS("particles-js", {
        particles: {
            number: {
                value: 80,
                density: { enable: true, value_area: 800 }
            },
            color: {
                value: isDark ? "#ffffff" : "#000000"
            },
            shape: { type: "circle" },
            opacity: { value: 0.8 },
            size: { value: 6, random: true },
            line_linked: {
                enable: true,
                distance: 150,
                color: isDark ? "#ffffff" : "#000000",
                opacity: 0.7,
                width: 1
            },
            move: {
                enable: true,
                speed: 5,
                out_mode: "out"
            }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: { enable: true, mode: "repulse" },
                onclick: { enable: true, mode: "push" },
                resize: true
            },
            modes: {
                repulse: { distance: 150 },
                push: { particles_nb: 4 }
            }
        },
        retina_detect: true
    });
}

// ==========================
// NAVBAR SHOW / HIDE
// ==========================
let lastScrollTop = 0;
const navbar = document.querySelector(".navbar");

document.addEventListener("mousemove", e => {
    if (e.clientY <= 50) navbar.classList.remove("navbar-hidden");
});

document.addEventListener("scroll", () => {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    navbar.classList.toggle("navbar-hidden", scrollTop > lastScrollTop);
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// ==========================
// SECTION HIGHLIGHT
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll(".section");
    const navLinks = document.querySelectorAll(".nav-link");

    function highlightSection() {
        let current = "";
        sections.forEach(section => {
            if (pageYOffset >= section.offsetTop - section.clientHeight / 3) {
                current = section.id;
                section.classList.add("active");
            } else {
                section.classList.remove("active");
            }
        });

        navLinks.forEach(link => {
            link.classList.toggle(
                "active",
                link.getAttribute("href") === `#${current}`
            );
        });
    }

    window.addEventListener("scroll", highlightSection);
    highlightSection();
});

// ==========================
// PROGRESS BARS
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    function animateBar(bar, target) {
        let width = 0;
        const interval = setInterval(() => {
            if (width >= target) clearInterval(interval);
            else bar.style.width = ++width + "%";
        }, 10);
    }

    function inViewport(el) {
        const r = el.getBoundingClientRect();
        return r.top >= 0 && r.bottom <= window.innerHeight;
    }

    function fillBars() {
        document.querySelectorAll(".progress-bar").forEach(bar => {
            if (inViewport(bar) && !bar.classList.contains("filled")) {
                animateBar(bar, bar.dataset.width);
                bar.classList.add("filled");
            }
        });
    }

    window.addEventListener("scroll", fillBars);
    fillBars();
});

// ==========================
// MOBILE NAV CLOSE
// ==========================
$(document).ready(function () {
    $(".navbar-nav>li>a").on("click", function () {
        $(".navbar-collapse").collapse("hide");
    });
});

// ==========================
// DARK MODE TOGGLE
// ==========================
const isDark = localStorage.getItem("theme") === "dark";

if (isDark) document.body.classList.add("dark-mode");
loadParticles(isDark);

document.getElementById("themeToggle")?.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    const dark = document.body.classList.contains("dark-mode");
    localStorage.setItem("theme", dark ? "dark" : "light");

    document.getElementById("particles-js").innerHTML = "";
    loadParticles(dark);
});