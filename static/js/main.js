/* =====================================
   GOLD SHOP MAIN JS
===================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       Elements
    ========================== */

    const navbar = document.getElementById("navbar");
    const stickyMenu = document.getElementById("stickyMenu");

    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const hamburgerBtn = document.getElementById("hamburgerBtn");
    const sidebarClose = document.getElementById("sidebarClose");

    const loading = document.getElementById("loading");

    const notificationBtn = document.getElementById("notificationBtn");
    const cartBtn = document.getElementById("cartBtn");

    /* ==========================
       Loading Screen
    ========================== */

    window.addEventListener("load", () => {

        setTimeout(() => {

            loading.classList.remove("show");

        }, 600);

    });

    /* ==========================
       Sidebar
    ========================== */

    function openSidebar() {

        sidebar.classList.add("open");
        sidebarOverlay.classList.add("active");

        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {

        sidebar.classList.remove("open");
        sidebarOverlay.classList.remove("active");

        document.body.style.overflow = "";
    }

    if (hamburgerBtn)
        hamburgerBtn.addEventListener("click", openSidebar);

    if (sidebarClose)
        sidebarClose.addEventListener("click", closeSidebar);

    if (sidebarOverlay)
        sidebarOverlay.addEventListener("click", closeSidebar);

    document.addEventListener("keydown", (e) => {

        if (e.key === "Escape") {
            closeSidebar();
        }

    });

    /* ==========================
       Navbar Scroll Effect
    ========================== */

    window.addEventListener("scroll", () => {

        if (window.scrollY > 50) {

            navbar.classList.add("scrolled");

            if (stickyMenu) {
                stickyMenu.classList.add("sticky");
            }

        } else {

            navbar.classList.remove("scrolled");

            if (stickyMenu) {
                stickyMenu.classList.remove("sticky");
            }
        }

    });

    /* ==========================
       Survey Cards Click
    ========================== */

    document.querySelectorAll(".survey-card")
        .forEach(card => {

            card.addEventListener("click", () => {

                const href = card.dataset.href;

                if (href) {
                    window.location.href = href;
                }

            });

        });

    /* ==========================
       Notification
    ========================== */

    if (notificationBtn) {

        notificationBtn.addEventListener("click", () => {

            showToast(
                "اعلان جدیدی وجود ندارد 🔔"
            );

        });

    }

    /* ==========================
       Cart Demo
    ========================== */

    let cartCount = 0;

    if (cartBtn) {

        cartBtn.addEventListener("click", () => {

            cartCount++;

            const amount =
                document.querySelector(".cart-amount");

            if (amount) {

                amount.innerText =
                    `${cartCount} محصول`;

            }

            showToast(
                "محصول به سبد خرید اضافه شد 🛒"
            );

        });

    }

    /* ==========================
       Dropdown User Menu
    ========================== */

    const userBtn =
        document.querySelector(".user-btn");

    const dropdownMenu =
        document.querySelector(".dropdown-menu");

    if (userBtn && dropdownMenu) {

        userBtn.addEventListener("click", (e) => {

            e.stopPropagation();

            dropdownMenu.classList.toggle("active");

        });

        document.addEventListener("click", () => {

            dropdownMenu.classList.remove("active");

        });

    }

    /* ==========================
       Ripple Effect
    ========================== */

    document
        .querySelectorAll(
            ".btn-auth,.search-button,.hamburger-btn"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                function (e) {

                    const ripple =
                        document.createElement("span");

                    const rect =
                        this.getBoundingClientRect();

                    const size =
                        Math.max(
                            rect.width,
                            rect.height
                        );

                    ripple.style.width =
                        ripple.style.height =
                        size + "px";

                    ripple.style.left =
                        e.clientX -
                        rect.left -
                        size / 2 +
                        "px";

                    ripple.style.top =
                        e.clientY -
                        rect.top -
                        size / 2 +
                        "px";

                    ripple.classList.add("ripple");

                    this.appendChild(ripple);

                    setTimeout(() => {

                        ripple.remove();

                    }, 600);

                }
            );

        });

    /* ==========================
       Scroll Reveal
    ========================== */

    const revealElements =
        document.querySelectorAll(
            ".survey-card,.section-title,.footer-section"
        );

    const observer =
        new IntersectionObserver(

            entries => {

                entries.forEach(entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "revealed"
                        );

                    }

                });

            },

            {
                threshold: 0.15
            }

        );

    revealElements.forEach(el => {

        observer.observe(el);

    });

    /* ==========================
       Toast Function
    ========================== */

    function showToast(message) {

        const toast =
            document.createElement("div");

        toast.className = "toast-message";

        toast.innerText = message;

        document.body.appendChild(toast);

        setTimeout(() => {

            toast.classList.add("show");

        }, 50);

        setTimeout(() => {

            toast.classList.remove("show");

            setTimeout(() => {

                toast.remove();

            }, 400);

        }, 2500);

    }

});