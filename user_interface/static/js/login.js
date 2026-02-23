const modalOverlay = document.getElementById('modalOverlay');
        const modalContainer = document.getElementById('modalContainer');
        const mainPage = document.getElementById('mainPage');
        const openBtn = document.getElementById('openAuth');
        const closeBtn = document.getElementById('closeBtn');
        const indicator = document.getElementById('indicator');

        // Open Modal logic
        openBtn.addEventListener('click', () => {
            modalOverlay.classList.add('active');
            mainPage.classList.add('blur-active');
        });

        // Close Modal logic
        const closeModal = () => {
            modalOverlay.classList.remove('active');
            mainPage.classList.remove('blur-active');
        };

        closeBtn.addEventListener('click', closeModal);

        // Close on Outside Click
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });

        // Tab Switching logic
        function switchTab(type) {
            const loginForm = document.getElementById('loginForm');
            const registerForm = document.getElementById('registerForm');
            const btns = document.querySelectorAll('.tab-btn');

            if (type === 'login') {
                loginForm.classList.add('active');
                registerForm.classList.remove('active');
                indicator.style.left = '5px';
                btns[0].classList.add('active');
                btns[1].classList.remove('active');
            } else {
                loginForm.classList.remove('active');
                registerForm.classList.add('active');
                indicator.style.left = 'calc(50% - 0px)';
                btns[1].classList.add('active');
                btns[0].classList.remove('active');
            }
        }

        // Password View Toggle
        function togglePass(id) {
            const input = document.getElementById(id);
            const icon = input.nextElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        }

        // Auth Handler
        function handleAuth(e) {
            e.preventDefault();
            console.log("Form Submitted Successfully");
            closeModal();
            return false;
        }