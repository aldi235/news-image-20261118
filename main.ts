// News-image entry: the image beside this file is the entry itself.
// Copy it to the grader's output directory so the judge sees exactly those bytes.
import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outFile = join(outDir, 'entry.png');
const srcFile = new URL('./entry.png', import.meta.url);

// The gate only accepts a whole image of at most 1 MiB: fail loudly, never
// ship a file the gate would reject.
const size = statSync(srcFile).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate limit`);
}
mkdirSync(dirname(outFile), { recursive: true });
copyFileSync(srcFile, outFile);
