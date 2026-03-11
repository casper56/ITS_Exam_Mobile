const CACHE_NAME = 'its-exam-v15';
const URLS_TO_CACHE = [
  '../index.html',
  './ITS_Python/ITS_Python.html',
  './ITS_Database/ITS_Database.html',
  './ITS_AI/ITS_AI.html',
  './ITS_JAVA/ITS_JAVA.html',
  './ITS_softdevelop/ITS_softdevelop.html',
  './Generative_AI/Generative_AI.html',
  './AZ900/AZ900.html',
  './AI900/AI900.html',
  './assets/icon.png',
  './js/choicelist_patch_v2.js',
  './js/sync_manager.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://cdn.jsdelivr.net/npm/marked/marked.min.js'
];

// Install
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Service Worker: Caching files...');
      // 使用 Promise.allSettled 替代 addAll，確保個別檔案失敗不影響整體安裝
      return Promise.allSettled(
        URLS_TO_CACHE.map(url => {
          return cache.add(url).catch(err => console.error(`Failed to cache: ${url}`, err));
        })
      );
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
