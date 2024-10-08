document.addEventListener('DOMContentLoaded', function() {
    const textContainer = document.getElementById('tpg');
    const imageContainers = document.querySelectorAll('.image-container');

    if (textContainer) {
        textContainer.style.animation = 'slideUp 2s forwards';
    } else {
        console.error('Elemento con ID "text-container" no encontrado.');
    }

    imageContainers.forEach((container, index) => {
        container.style.animation = `fadeIn 2s forwards ${2 + index * 0.5}s`;
    });

    document.getElementById('darkBackground').addEventListener('click', closePopup);
    document.getElementById('darkBackground2').addEventListener('click', closePopup2);
   
});
function openPopup(event) {
    event.preventDefault(); 
    const darkBackground = document.getElementById('darkBackground');
    const popup = darkBackground.querySelector('.popup');
    darkBackground.style.display = 'flex';
    setTimeout(() => {
        darkBackground.style.opacity = '1';
        popup.style.opacity = '1';
        popup.style.transform = 'scale(1)';
    }, 10); 
}

function closePopup() {
    const darkBackground = document.getElementById('darkBackground');
    const popup = darkBackground.querySelector('.popup');
    darkBackground.style.opacity = '0';
    popup.style.opacity = '0';
    popup.style.transform = 'scale(0.9)';
    setTimeout(() => {
        darkBackground.style.display = 'none';
    }, 500); 
}

function openPopup2(event) {
    event.preventDefault(); 
    const darkBackground2 = document.getElementById('darkBackground2');
    const popup2 = darkBackground2.querySelector('.popup2');
    darkBackground2.style.display = 'flex';
    setTimeout(() => {
        darkBackground2.style.opacity = '1';
        popup2.style.opacity = '1';
        popup2.style.transform = 'scale(1)';
    }, 10); 
}

function closePopup2() {
    const darkBackground2 = document.getElementById('darkBackground2');
    const popup2 = darkBackground2.querySelector('.popup2');
    darkBackground2.style.opacity = '0';
    popup2.style.opacity = '0';
    popup2.style.transform = 'scale(0.9)';
    setTimeout(() => {
        darkBackground2.style.display = 'none';
    }, 500);
}