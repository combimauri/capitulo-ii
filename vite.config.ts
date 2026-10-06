import { defineConfig } from 'vitest/config';
import { VitePWA } from 'vite-plugin-pwa';
import ink from './tools/vite-plugin-ink.ts';

export default defineConfig({
  plugins: [
    ink(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/*.png'],
      manifest: {
        name: 'Capítulo II',
        short_name: 'Capítulo II',
        description: 'Aventura narrativa en pixel art basada libremente en 1984',
        lang: 'es',
        display: 'fullscreen',
        orientation: 'landscape',
        background_color: '#0b0c0f',
        theme_color: '#0b0c0f',
        icons: [
          { src: 'icons/icono-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icono-512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
        ],
      },
      workbox: { globPatterns: ['**/*.{js,css,html,png,woff2,json}'], maximumFileSizeToCacheInBytes: 8 * 1024 * 1024 },
    }),
  ],
  build: { target: 'es2022', chunkSizeWarningLimit: 2000 },
  test: { environment: 'node' },
});
