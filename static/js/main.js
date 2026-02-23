// main.js - адаптивные функции

document.addEventListener('DOMContentLoaded', function() {

    // 1. Определение устройства
    const isMobile = window.innerWidth <= 768;
    const isTablet = window.innerWidth > 768 && window.innerWidth <= 992;
    const isDesktop = window.innerWidth > 992;

    document.body.classList.toggle('is-mobile', isMobile);
    document.body.classList.toggle('is-tablet', isTablet);
    document.body.classList.toggle('is-desktop', isDesktop);

    // 2. Адаптивное меню
    setupMobileMenu();

    // 3. Оптимизация изображений
    optimizeImages();

    // 4. Обработка touch-событий
    if (isMobile || isTablet) {
        setupTouchEvents();
    }

    // 5. Плавная прокрутка
    setupSmoothScroll();

    // 6. Адаптивные таблицы
    makeTablesResponsive();
});

// Настройка мобильного меню
function setupMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        // Закрытие меню после выбора пункта
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 768 && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });

        // Закрытие по клику вне меню
        document.addEventListener('click', (e) => {
            if (window.innerWidth < 768 &&
                navbarCollapse.classList.contains('show') &&
                !navbarCollapse.contains(e.target) &&
                !navbarToggler.contains(e.target)) {
                navbarToggler.click();
            }
        });
    }
}

// Оптимизация изображений
function optimizeImages() {
    // Ленивая загрузка
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Адаптивные изображения для мобильных
    if (window.innerWidth <= 576) {
        document.querySelectorAll('.card-img-top').forEach(img => {
            if (img.naturalWidth > 400) {
                img.style.height = '150px';
            }
        });
    }
}

// Touch-события для мобильных
function setupTouchEvents() {
    // Предотвращение двойного тапа для зума
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (e) => {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) {
            e.preventDefault();
        }
        lastTouchEnd = now;
    }, false);

    // Добавление активного состояния при тапе
    document.querySelectorAll('.btn, .nav-link, .list-group-item').forEach(el => {
        el.addEventListener('touchstart', () => {
            el.classList.add('touch-active');
        });

        el.addEventListener('touchend', () => {
            setTimeout(() => {
                el.classList.remove('touch-active');
            }, 150);
        });
    });
}

// Плавная прокрутка
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const offset = 80; // высота navbar
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Адаптивные таблицы
function makeTablesResponsive() {
    document.querySelectorAll('table').forEach(table => {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

// Обработка изменения размера окна
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Обновление классов устройства
        const width = window.innerWidth;
        document.body.classList.toggle('is-mobile', width <= 768);
        document.body.classList.toggle('is-tablet', width > 768 && width <= 992);
        document.body.classList.toggle('is-desktop', width > 992);
    }, 250);
});