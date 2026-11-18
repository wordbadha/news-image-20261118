// "THE WORLD TODAY" — Wednesday, 18 November 2026.
//
// The front page for this entry is already finished: it sits next to this
// file as entry.png. Nothing is drawn while the program runs. All this
// program does is hand that exact file to the grader, dropping it into the
// output folder under the name entry.png.
//
// How the grader runs it:
//   MAKEFUN_OUTPUT_DIR=/output node main.ts
// Leave MAKEFUN_OUTPUT_DIR unset and /output is used instead.
//
// Node 22, standard library only — there is nothing to install.

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// Work out where this program lives, so the picture is found no matter
// which directory the program is launched from.
const here = dirname(fileURLToPath(import.meta.url));
const picture = join(here, 'entry.png');

// The destination comes from the environment, with /output as the fallback.
const destinationDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
const destination = join(destinationDir, 'entry.png');

// Make sure the destination folder is there, then hand the picture over
// byte for byte — the judge sees exactly the bytes in entry.png.
mkdirSync(destinationDir, { recursive: true });
copyFileSync(picture, destination);

console.log(`Wrote ${destination}`);
