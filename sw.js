const CACHE_NAME = 'its-exam-prod-v1'; // 固定的快取名稱
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
    caches.open(CACHE_NAME).then(cache => {
      console.log('Service Worker: Initial Caching...');
      return cache.addAll(URLS_TO_CACHE);
    })
  );
});

// Activate
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch - Network First Strategy (網路優先)
self.addEventListener('fetch', event => {
  // 只針對 GET 請求進行快取處理
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // 如果網路抓取成功，將其複製一份存入快取
        const responseClone = networkResponse.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });
        return networkResponse;
      })
      .catch(() => {
        // 如果網路失敗（離線），則從快取中尋找
        return caches.match(event.request);
      })
  );
});
