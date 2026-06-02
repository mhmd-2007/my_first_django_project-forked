// ========================================
// توابع پیشرفته صفحه لاگین
// ========================================

// تولید ذرات طلایی در پس‌زمینه
function createParticles() {
    const particlesContainer = document.querySelector('.particles');
    if (!particlesContainer) return;
    
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        const size = Math.random() * 6 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDuration = `${Math.random() * 8 + 4}s`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        
        particlesContainer.appendChild(particle);
    }
}

// نمایش/مخفی کردن رمز عبور با انیمیشن
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.textContent = '🙈';
        toggleBtn.style.transform = 'scale(1.1)';
        setTimeout(() => {
            toggleBtn.style.transform = 'scale(1)';
        }, 200);
    } else {
        passwordInput.type = 'password';
        toggleBtn.textContent = '👁️';
        toggleBtn.style.transform = 'scale(1.1)';
        setTimeout(() => {
            toggleBtn.style.transform = 'scale(1)';
        }, 200);
    }
}

// اعتبارسنجی فرم لاگین
function validateLoginForm() {
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const submitBtn = document.querySelector('.auth-btn');
    
    if (!username.value.trim()) {
        showError(username, 'لطفاً نام کاربری را وارد کنید');
        return false;
    }
    
    if (!password.value.trim()) {
        showError(password, 'لطفاً رمز عبور را وارد کنید');
        return false;
    }
    
    // افکت لودینگ روی دکمه
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '⏳ در حال ورود...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 3000);
    
    return true;
}

// نمایش خطا با انیمیشن
function showError(input, message) {
    input.style.borderColor = '#e74c3c';
    input.style.animation = 'shake 0.3s ease';
    
    setTimeout(() => {
        input.style.borderColor = '';
        input.style.animation = '';
    }, 1000);
    
    alert(message);
}

// دکمه‌های اجتماعی
function socialLogin(provider) {
    const btn = event.currentTarget;
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '⏳ در حال اتصال...';
    btn.disabled = true;
    
    setTimeout(() => {
        alert(`✨ ورود با ${provider} به زودی فعال خواهد شد!`);
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 1500);
}

// انیمیشن ورود با Enter
function setupEnterKey() {
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('loginForm').submit();
            }
        });
    }
}

// افکت فوکوس روی فیلدها
function setupFocusEffects() {
    const inputs = document.querySelectorAll('.input-wrapper input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.01)';
        });
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
}

// اجرا بعد از لود صفحه
document.addEventListener('DOMContentLoaded', function() {
    createParticles();
    setupEnterKey();
    setupFocusEffects();
    
    // اضافه کردن حلقه‌های نورانی
    const glowRings = document.querySelector('.glow-rings');
    if (glowRings) {
        for (let i = 1; i <= 4; i++) {
            const ring = document.createElement('div');
            ring.classList.add('ring');
            glowRings.appendChild(ring);
        }
    }
});