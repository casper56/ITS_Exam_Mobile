const CACHE_NAME = 'its-exam-v18'; // 升級版本以強制重新快取
const URLS_TO_CACHE = [
  './index.html',
  './www/ITS_Python/ITS_Python.html',
  './www/ITS_Database/ITS_Database.html',
  './www/ITS_AI/ITS_AI.html',
  './www/ITS_JAVA/ITS_JAVA.html',
  './www/ITS_softdevelop/ITS_softdevelop.html',
  './www/Generative_AI/Generative_AI.html',
  './www/AZ900/AZ900.html',
  './www/AI900/AI900.html',
  './www/assets/icon.png',
  './www/js/choicelist_patch_v2.js',
  './www/js/sync_manager.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://cdn.jsdelivr.net/npm/marked/marked.min.js'
];

// Install
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching files...');
        return Promise.allSettled(
          URLS_TO_CACHE.map(url => {
            return cache.add(url).catch(err => {
              if (err.name !== 'SecurityError') {
                console.warn(`Failed to cache: ${url}`, err);
              }
            });
          })
        );
      })
      .catch(err => {
        if (err.name === 'SecurityError') {
          console.warn('Service Worker: Storage access blocked by browser security (Tracking Prevention).');
        } else {
          console.error('Service Worker: Cache open failed', err);
        }
      })
  );
});

// Activate - Clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Clearing old cache', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
