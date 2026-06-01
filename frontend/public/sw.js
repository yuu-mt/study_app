const CACHE_NAME = 'monster-study-v1'
const urlsToCache = [
    '/',
    '/index.html',
    ]

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
    )
})

self.addEventListener('fetch', event => {
    const requestUrl = new URL(event.request.url)

    if (event.request.method !== 'GET' || requestUrl.origin !== self.location.origin) {
        return
    }

    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request)
        })
    )
})
