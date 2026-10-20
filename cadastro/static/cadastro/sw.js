const CACHE_NAME = 'turismo-picui-v3';

const ASSETS = [
  '/static/cadastro/manifest.webmanifest',
  '/static/cadastro/imagem/app-icon-192.png',
  '/static/cadastro/imagem/app-icon-512.png',
  '/static/cadastro/imagem/app-icon-maskable-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
      .catch(() => undefined)
  );

  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter(
            (key) =>
              key.startsWith('turismo-picui-') &&
              key !== CACHE_NAME
          )
          .map((key) => caches.delete(key))
      )
    )
  );

  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Só trabalha com requisições GET do próprio site.
  if (
    request.method !== 'GET' ||
    url.origin !== self.location.origin
  ) {
    return;
  }

  // IMPORTANTE:
  // Não interceptamos páginas/navegação.
  // O Django/Render recebe diretamente:
  // /, /guia/, /cadastro/, /chatbot/, etc.
  if (request.mode === 'navigate') {
    return;
  }

  // Cache somente arquivos estáticos.
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) {
          return cached;
        }

        return fetch(request).then((response) => {
          if (
            response.ok &&
            response.type === 'basic'
          ) {
            const copy = response.clone();

            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, copy);
            });
          }

          return response;
        });
      })
    );
  }
});