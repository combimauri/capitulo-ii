import Phaser from 'phaser';
import '@fontsource/pixelify-sans/400.css';
import '@fontsource/vt323/400.css';
import { registerSW } from 'virtual:pwa-register';
import { BootScene } from './scenes/BootScene';
import { PreloadScene } from './scenes/PreloadScene';
import { MenuScene } from './scenes/MenuScene';
import { LocationScene } from './scenes/LocationScene';
import { UIScene } from './scenes/UIScene';
import { CascotesScene } from './scenes/minijuegos/CascotesScene';
import { FichaScene } from './scenes/minijuegos/FichaScene';
import { FacecrimeScene } from './scenes/minijuegos/FacecrimeScene';
import { RegistroScene } from './scenes/RegistroScene';
import { ParteScene } from './scenes/minijuegos/ParteScene';
import { FrenteScene } from './scenes/minijuegos/FrenteScene';
import { PancartaScene } from './scenes/minijuegos/PancartaScene';
import { ImpactosScene } from './scenes/minijuegos/ImpactosScene';
import { SammyScene } from './scenes/minijuegos/SammyScene';
import { DiarioScene } from './scenes/minijuegos/DiarioScene';
import { ComparadorScene } from './scenes/minijuegos/ComparadorScene';
import { EsconderScene } from './scenes/minijuegos/EsconderScene';
import { DocumentoScene } from './scenes/minijuegos/DocumentoScene';
import { LibroScene } from './scenes/minijuegos/LibroScene';
import { CopiarScene } from './scenes/minijuegos/CopiarScene';
import { PalancaScene } from './scenes/minijuegos/PalancaScene';
import { LlavesScene } from './scenes/minijuegos/LlavesScene';
import { CombinacionScene } from './scenes/minijuegos/CombinacionScene';
import { RectificacionScene } from './scenes/minijuegos/RectificacionScene';
import { ListaScene } from './scenes/minijuegos/ListaScene';
import { TunelesScene } from './scenes/minijuegos/TunelesScene';
import { CapituloScene } from './scenes/minijuegos/CapituloScene';
import { DialScene } from './scenes/minijuegos/DialScene';
import { Habitacion101Scene } from './scenes/minijuegos/Habitacion101Scene';
import { CFAutomaticoScene } from './scenes/minijuegos/CFAutomaticoScene';
import { DeclaracionScene } from './scenes/minijuegos/DeclaracionScene';
import { ResistenciaScene } from './scenes/minijuegos/ResistenciaScene';
import { EpilogoScene, CreditosScene } from './scenes/minijuegos/EpilogoScene';
import { RESOLUCION, narrativa, registro, mision, EV } from './core/juego';

registerSW({ immediate: true });

const juego = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'juego',
  width: RESOLUCION.ancho,
  height: RESOLUCION.alto,
  backgroundColor: '#0b0c0f',
  pixelArt: true,
  roundPixels: true,
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  input: { activePointers: 2 },
  dom: { createContainer: true },
  scene: [BootScene, PreloadScene, MenuScene, LocationScene, UIScene, CascotesScene, FichaScene, FacecrimeScene, ParteScene, FrenteScene, PancartaScene, ImpactosScene, SammyScene, DiarioScene, ComparadorScene, EsconderScene,
    DocumentoScene, LibroScene, CopiarScene, PalancaScene, LlavesScene, CombinacionScene, RectificacionScene, ListaScene,
    TunelesScene, CapituloScene, DialScene, Habitacion101Scene, DeclaracionScene, ResistenciaScene, EpilogoScene, CreditosScene, CFAutomaticoScene, RegistroScene],
});

// Atajos de depuración en la consola del navegador (solo en desarrollo):
//   saltar('departamento', 'depto.entrar')   → va a un escenario y lanza un knot de ink
if (import.meta.env.DEV) {
  Object.assign(window, {
    juego,
    narrativa,
    registro,
    mision,
    saltar(escena: string, knot?: string, vars: Record<string, unknown> = {}) {
      for (const [k, v] of Object.entries(vars)) narrativa.set(k, v);
      juego.scene.getScenes(true).forEach((s) => { if (!['UI', 'Location'].includes(s.scene.key)) s.scene.stop(); });
      if (!juego.scene.isActive('UI')) juego.scene.start('UI');
      if (juego.scene.isActive('Location')) juego.scene.getScene('Location').scene.restart({ escena, cargado: true });
      else juego.scene.start('Location', { escena, cargado: true });
      if (knot) setTimeout(() => juego.events.emit(EV.dialogoIniciar, knot), 600);
    },
  });
}
