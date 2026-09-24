/* Felpudos Argentinos — interacciones minimas */
(function () {
  'use strict';

  // ------------------------------------------------------------ menu movil
  var burger = document.querySelector('.nav__burger');
  var mnav = document.getElementById('mnav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      burger.setAttribute('aria-label', open ? 'Abrir menú' : 'Cerrar menú');
      mnav.classList.toggle('is-open', !open);
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        burger.setAttribute('aria-expanded', 'false');
        mnav.classList.remove('is-open');
      }
    });
  }

  // ------------------------------------------- aparicion al hacer scroll
  var targets = document.querySelectorAll('.card, .rubros li, .whys li, .stats div, .ph, .sec__head');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-on');
        io.unobserve(en.target);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -40px' });

    targets.forEach(function (el, i) {
      el.classList.add('in-view');
      el.style.transitionDelay = (i % 6) * 60 + 'ms';
      io.observe(el);
    });
  }

  // ------------------------------------------------------------- año pie
  var y = document.getElementById('y');
  if (y) y.textContent = new Date().getFullYear();

  // --------------------------------------- formulario -> WhatsApp (demo)
  // En produccion esto pasa a envio por correo desde el servidor.
  var form = document.querySelector('.form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var txt = 'Hola! Soy ' + (d.get('nombre') || '') +
        (d.get('negocio') ? ' de ' + d.get('negocio') : '') +
        '. Me interesa: ' + (d.get('producto') || '') +
        (d.get('mensaje') ? '. ' + d.get('mensaje') : '') +
        (d.get('tel') ? '. Mi WhatsApp: ' + d.get('tel') : '');
      window.open('https://wa.me/5491100000000?text=' + encodeURIComponent(txt), '_blank', 'noopener');
    });
  }
})();
