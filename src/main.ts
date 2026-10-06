import Phaser from 'phaser';
import '@fontsource/pixelify-sans/400.css';
import '@fontsource/vt323/400.css';
import { registerSW } from 'virtual:pwa-register';
import { BootScene } from './scenes/BootScene';
import { PreloadScene } from './scenes/PreloadScene';
import { MenuScene } from './scenes/MenuScene';
import { LocationScene } from './scenes/LocationScene';
import { UIScene } from './scenes/UIScene';
import { RESOLUCION } from './core/juego';

registerSW({ immediate: true });

new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'juego',
  width: RESOLUCION.ancho,
  height: RESOLUCION.alto,
  backgroundColor: '#0b0c0f',
  pixelArt: true,
  roundPixels: true,
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  input: { activePointers: 2 },
  scene: [BootScene, PreloadScene, MenuScene, LocationScene, UIScene],
});
