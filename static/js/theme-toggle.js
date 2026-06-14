
const toggleButton = document.getElementById('theme-toggle');
const html = document.documentElement; // Uso el documento html directamente
const storageKey = 'themePreference';
const darkClass = 'dark-mode';

// Función para aplicar la clase y guardar en localStorage
const setTheme = (isDark) => {
    if (isDark) {
        html.classList.add(darkClass);
        localStorage.setItem(storageKey, 'dark');
    } else {
        html.classList.remove(darkClass);
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
    checkCurrentlyTheme = () => {
        const isCurrentlyDark = html.classList.contains(darkClass);
        setTheme(!isCurrentlyDark);

        if (isCurrentlyDark) {
            const btnContent = '<i class="bi bi-lightbulb-fill"></i>'
            toggleButton.innerHTML = btnContent
        } else {
            const btnContent = '<i class="bi bi-lightbulb"></i>'
            toggleButton.innerHTML = btnContent
        }
        return isCurrentlyDark;
    }

    toggleButton.addEventListener('click', (ev) => {    
        checkCurrentlyTheme();
    });
}
