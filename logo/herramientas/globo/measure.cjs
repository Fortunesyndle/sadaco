const Jimp = require('jimp');

(async () => {
  const img = await Jimp.read('../../referencias/sadaco-international-logo.png');
  const W = img.bitmap.width, H = img.bitmap.height;
  const px = (x, y) => Jimp.intToRGBA(img.getPixelColor(x, y));
  const isWhite = p => p.a < 128 || (p.r > 235 && p.g > 235 && p.b > 235);
  const cls = p => isWhite(p) ? 'W' : (p.g > 150 && p.b < 150 ? 'G' : 'B');

  const x0 = Math.round(W / 2);
  let top = 0, bot = H - 1;
  while (isWhite(px(x0, top))) top++;
  while (isWhite(px(x0, bot))) bot--;
  const cy = (top + bot) / 2;
  let l = x0, r = x0;
  const yc = Math.round(cy);
  while (l > 0 && !(isWhite(px(l, yc)) && isWhite(px(l - 1, yc)) && isWhite(px(l - 2, yc)) && isWhite(px(l - 3, yc)))) l--;
  while (r < W - 1 && !(isWhite(px(r, yc)) && isWhite(px(r + 1, yc)) && isWhite(px(r + 2, yc)) && isWhite(px(r + 3, yc)))) r++;
  console.log({ W, H, top, bot, cy, left: l, right: r, cx: (l + r) / 2, R: (bot - top) / 2, Rx: (r - l) / 2 });

  const runs = (coords) => {
    let s = '', out = [];
    for (const [x, y] of coords) s += cls(px(x, y));
    let i = 0;
    while (i < s.length) { let j = i; while (j < s.length && s[j] === s[i]) j++; out.push(s[i] + (j - i)); i = j; }
    return out.join(' ');
  };
  const col = []; for (let y = top; y <= bot; y++) col.push([x0, y]);
  console.log('column x0:', runs(col));
  const row = []; for (let x = l; x <= r; x++) row.push([x, yc]);
  console.log('row cy:', runs(row));
})();
