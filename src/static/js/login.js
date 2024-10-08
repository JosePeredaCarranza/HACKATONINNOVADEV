document.addEventListener('DOMContentLoaded', function() {

    if (localStorage.getItem('theme') === 'dark-mode') {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        document.getElementById('fondo-pag').src = document.getElementById('fondo-pag').getAttribute('data-dark');
        document.getElementById('Imagen-login').src = document.getElementById('Imagen-login').getAttribute('data-dark');
    }
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
                    img.src = img.getAttribute('data-dark');;
                    imgLogin.src = imgLogin.getAttribute('data-dark');
                    localStorage.setItem('theme', 'dark-mode');
                } else {
                    body.classList.remove('dark-mode');
                    body.classList.add('light-mode');
                    img.src = img.getAttribute('data-light');
                    imgLogin.src = imgLogin.getAttribute('data-light');
                    localStorage.setItem('theme', 'light-mode');
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
                    // Quita el ID 'invisible' del SVG actual
                    currentInvisibleSvg.removeAttribute('id');
                    
                    // Añade el ID 'invisible' al siguiente SVG
                    nextSvg.setAttribute('id', 'invisible');
                }
            }
        });
    });