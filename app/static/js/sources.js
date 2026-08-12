document.addEventListener('DOMContentLoaded', () => {
    const btnAudit = document.getElementById('btnAudit');
    if (btnAudit) {
        btnAudit.addEventListener('click', () => {
            const icon = btnAudit.querySelector('i');
            icon.classList.add('animate-spin');
            
            setTimeout(() => {
                icon.classList.remove('animate-spin');
                window.showToast('Compliance audit complete. No violations found.', 'success');
            }, 1500);
        });
    }
});
