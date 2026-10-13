/**
 * Middleware de enrutado de Vercel: el juego solo se abre desde los países de la lista blanca.
 * Corre antes de la caché en cada petición (página, recursos y service worker), así que nada
 * del juego se descarga desde fuera. Sin país conocido, tampoco se deja pasar.
 */
import { geolocation, next } from '@vercel/functions';

/**
 * Códigos ISO 3166-1 alfa-2: países donde *1984* ya es de dominio público. Orwell murió el 21 de enero de 1950,
 * así que con vida + 70 años o menos lo es desde el 1 de enero de 2021, y con vida + 75 desde el 1 de enero de 2026.
 * Fuera: México (vida + 100), Colombia (vida + 80) y Puerto Rico (ley de EE. UU.: protegido hasta 2044).
 */
export const PAISES = new Set([
  // Latinoamérica
  'AR', 'BO', 'BR', 'CL', 'CR', 'DO', 'EC', 'GT', 'HN', 'NI', 'PA', 'PE', 'PY', 'SV', 'UY', 'VE',
  // Unión Europea (vida + 70; España, ver README)
  'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV',
  'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK',
  // resto de Europa
  'AD', 'AL', 'BA', 'BY', 'CH', 'GB', 'IS', 'LI', 'MC', 'MD', 'ME', 'MK', 'NO', 'RS', 'RU', 'SM', 'UA', 'VA', 'XK',
  // territorios europeos con código propio (Åland, Feroe, Gibraltar, Guernsey, Jersey, Man)
  'AX', 'FO', 'GG', 'GI', 'IM', 'JE',
]);

export const permitido = (pais: string | undefined) => !!pais && PAISES.has(pais.toUpperCase());

const DENEGADO = `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Capítulo II</title>
<style>
  html, body { margin: 0; height: 100%; background: #0b0c0f; color: #d8d2bd; }
  body { display: flex; align-items: center; justify-content: center; text-align: center; padding: 24px; box-sizing: border-box;
    font: 18px/1.5 ui-monospace, "SF Mono", Menlo, Consolas, monospace; }
  h1 { font-size: 28px; letter-spacing: 2px; color: #eeead9; margin: 0 0 8px; }
  hr { border: 0; border-top: 3px solid #a4262a; width: 220px; margin: 0 auto 24px; }
  p { margin: 0; max-width: 32em; }
</style>
</head>
<body>
  <div>
    <h1>CAPÍTULO II</h1>
    <hr>
    <p>Este registro no está disponible en su sector.</p>
  </div>
</body>
</html>`;

export default function middleware(request: Request) {
  if (permitido(geolocation(request).country)) return next();
  return new Response(DENEGADO, {
    status: 403,
    headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' },
  });
}
