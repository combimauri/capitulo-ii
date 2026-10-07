/**
 * Pantalla completa (diseño técnico §8.1): entrar, salir y el botón con su icono.
 * El objetivo es el contenedor #juego (main.ts, scale.fullscreenTarget), que guarda el canvas y los
 * campos de texto HTML; si solo fuera el canvas, en Android los campos quedarían fuera y no saldría el teclado.
 */
import Phaser from 'phaser';
import { COLOR } from './estilo';

/** La app instalada ya va a pantalla completa; en iPhone el navegador no deja pedirla. */
export function hayPantallaCompleta(escena: Phaser.Scene) {
  const instalada = window.matchMedia?.('(display-mode: fullscreen), (display-mode: standalone)').matches;
  return !instalada && escena.scale.fullscreen.available;
}

/** Entra o sale. Debe llamarse al soltar un toque o un clic: es el gesto que los navegadores aceptan. */
export function alternarPantallaCompleta(escena: Phaser.Scene, entrar = !escena.scale.isFullscreen) {
  if (!hayPantallaCompleta(escena) || entrar === escena.scale.isFullscreen) return;
  try {
    if (!entrar) { escena.scale.stopFullscreen(); return; }
    escena.scale.startFullscreen();
    void (screen.orientation as ScreenOrientation & { lock?: (o: string) => Promise<void> }).lock?.('landscape').catch(() => {});
  } catch { /* el navegador no lo permite */ }
}

/**
 * Botón cuadrado con el icono de pantalla completa (esquinas hacia fuera) o de salir (hacia dentro).
 * Se redibuja solo al entrar o salir, también con el botón «atrás» del móvil.
 */
export function botonPantallaCompleta(escena: Phaser.Scene, x: number, y: number) {
  if (!hayPantallaCompleta(escena)) return null;
  const fondo = escena.add.rectangle(x, y, 44, 44, COLOR.gris1, 0.7).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
  const icono = escena.add.graphics();
  const dibujar = () => {
    const dentro = escena.scale.isFullscreen;
    const r = 12, l = 7;
    icono.clear().lineStyle(3, COLOR.papel3);
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      // entrar: el vértice en la esquina y los brazos hacia dentro; salir: el vértice hacia el centro y los brazos hacia fuera
      const vx = x + sx * (dentro ? r - l : r), vy = y + sy * (dentro ? r - l : r);
      const bx = dentro ? sx * l : -sx * l, by = dentro ? sy * l : -sy * l;
      icono.lineBetween(vx, vy, vx + bx, vy).lineBetween(vx, vy, vx, vy + by);
    }
  };
  fondo.on('pointerover', () => fondo.setFillStyle(COLOR.rojo3, 0.85));
  fondo.on('pointerout', () => fondo.setFillStyle(COLOR.gris1, 0.7));
  fondo.on('pointerup', () => alternarPantallaCompleta(escena));
  escena.scale.on(Phaser.Scale.Events.ENTER_FULLSCREEN, dibujar);
  escena.scale.on(Phaser.Scale.Events.LEAVE_FULLSCREEN, dibujar);
  escena.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
    escena.scale.off(Phaser.Scale.Events.ENTER_FULLSCREEN, dibujar);
    escena.scale.off(Phaser.Scale.Events.LEAVE_FULLSCREEN, dibujar);
  });
  dibujar();
  return { fondo, icono };
}
