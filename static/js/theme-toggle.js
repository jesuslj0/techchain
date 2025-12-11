document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;
    const storageKey = 'themePreference';
    const darkClass = 'dark-mode';
    const toggleNavBar = document.getElementById('navbar-icon');
    
    // Función para aplicar la clase y guardar en localStorage
    const setTheme = (isDark) => {
        if (isDark) {
            body.classList.add(darkClass);
            localStorage.setItem(storageKey, 'dark');
            toggleNavBar.style.filter = 'invert(1)';
        } else {
            body.classList.remove(darkClass);
            localStorage.setItem(storageKey, 'light');
        }
    };

    // Función para cargar la preferencia al iniciar
    const loadTheme = () => {
        const storedTheme = localStorage.getItem(storageKey);
        
        if (storedTheme) {
            // Cargar la preferencia guardada
            setTheme(storedTheme === 'dark');
        } else {
            // Opcional: Usar la preferencia del sistema operativo si no hay una guardada
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            setTheme(prefersDark);
        }
    };

    loadTheme();

    // Event listener para el botón de cambio
    if (toggleButton) {
        toggleButton.addEventListener('click', (ev) => {
            const isCurrentlyDark = body.classList.contains(darkClass);
            setTheme(!isCurrentlyDark);

            if (isCurrentlyDark) {
                const btnContent = '<i class="bi bi-toggle-off"></i> Modo oscuro'
                toggleButton.innerHTML = btnContent
            } else {
                const btnContent = '<i class="bi bi-toggle-on"></i> Modo oscuro'
                toggleButton.innerHTML = btnContent
            }

            
        });
    }
});