// Простой скрипт для демонстрации
document.addEventListener('DOMContentLoaded', function() {
    console.log('Mastodontco приложение загружено!');
    
    // Анимация элементов при загрузке страницы
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transition = 'opacity 1s ease';
        setTimeout(() => {
            section.style.opacity = '1';
        }, 300);
    });
}); 