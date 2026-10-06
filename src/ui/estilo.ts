/** Colores y tipografías de la interfaz (biblia visual §8). */
export const COLOR = {
  negro: 0x0b0c0f,
  gris1: 0x16181c,
  gris2: 0x22252a,
  gris3: 0x2f3338,
  papel3: 0xd8d2bd,
  papel4: 0xeeead9,
  rojo3: 0xa4262a,
  rojo4: 0xc8382f,
  tele0: 0x071712,
  tele1: 0x0f2a22,
  tele4: 0x48906c,
  tele5: 0x7fc496,
  ocre4: 0xf4dc94,
};

export const hex = (c: number) => '#' + c.toString(16).padStart(6, '0');

export const FUENTE = {
  texto: '"Pixelify Sans", monospace',
  maquina: '"VT323", monospace',
  /** El epílogo del Final D: un libro académico, fuera de la paleta y la letra del Partido. */
  libro: 'Georgia, "Iowan Old Style", "Times New Roman", serif',
};
