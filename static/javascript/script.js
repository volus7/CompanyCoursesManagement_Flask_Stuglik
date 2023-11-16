const timeoutElement = document.getElementById('timeout');
let lastActivity = Date.now();


document.addEventListener('click', () => {
    lastActivity = Date.now();
});

setInterval(function () {
    // Sprawdź, czy minęło więcej niż 5 minut od ostatniej aktywności
    if (Date.now() - lastActivity > 5 * 60 * 1000 - 1000) {
        // Przekieruj użytkownika na stronę wylogowania
        
        window.location.href = '/logout';
    }

    // Oblicz pozostały czas do wylogowania w sekundach
    const remainingTimeInSeconds = Math.ceil((5 * 60 * 1000 - 1000 - (Date.now() - lastActivity)) / 1000);

    // Oblicz minutę i sekundy
    const minutes = Math.floor(remainingTimeInSeconds / 60);
    const seconds = remainingTimeInSeconds % 60;

    // Zaktualizuj treść diva z pozostałym czasem
    timeoutElement.innerHTML = `${minutes}:${seconds}`;
}, 1000); 