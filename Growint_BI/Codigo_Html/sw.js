const CACHE_NAME = 'GROWINT'; // Nombre específico para tu caché
const URLS_TO_CACHE = [
  'https://app.powerbi.com' // URL que deseas cachear
  // Puedes agregar más URLs aquí si lo necesitas
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache abierta:', CACHE_NAME);
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Devuelve la respuesta desde la caché si existe
        if (response) {
          return response;
        }
        // Realiza la solicitud a la red si no está en la caché
        return fetch(event.request);
      })
  );
});
