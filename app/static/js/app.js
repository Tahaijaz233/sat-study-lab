document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Theme toggle logic
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                localStorage.setItem('sat_lab_theme', 'light');
            } else {
                html.classList.add('dark');
                localStorage.setItem('sat_lab_theme', 'dark');
            }
        });
    }
});

// Global toast helper
window.showToast = function(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    const colors = {
        info: 'bg-blue-500',
        success: 'bg-emerald-500',
        error: 'bg-red-500',
        warning: 'bg-amber-500'
    };
    
    toast.className = `${colors[type] || colors.info} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 transform translate-y-10 opacity-0 transition-all duration-300`;
    toast.innerHTML = `
        <span class="font-medium text-sm">${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
    });

    // Remove after 3s
    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
};
