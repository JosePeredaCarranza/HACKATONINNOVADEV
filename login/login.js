document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('mode').addEventListener('click', function(event) {
        event.preventDefault();

        var body = document.body;
        var img = document.getElementById('fondo-pag');
        var imgLogin = document.getElementById('Imagen-login');

        img.style.opacity = 0;
        imgLogin.style.opacity = 0;

        setTimeout(function() {
            if (body.classList.contains('light-mode')) {
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                img.src = 'fondo-pag-dark.jpg';
                imgLogin.src = 'Imagen-login-dark.png';
            } else {
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                img.src = 'fondo-pag.jpg';
                imgLogin.src = 'Imagen-login.png';
            }

            img.style.opacity = 1;
            imgLogin.style.opacity = 1;
        }, 500);
        var currentInvisibleSvg = document.querySelector('svg#invisible');
        
        if (currentInvisibleSvg) {
            var nextSvg = currentInvisibleSvg.nextElementSibling;
            if (!nextSvg || nextSvg.tagName.toLowerCase() !== 'svg') {
                nextSvg = document.querySelector('svg');
            }
            if (nextSvg) {
                currentInvisibleSvg.removeAttribute('id');
                nextSvg.setAttribute('id', 'invisible');
            }
        }
    });
});