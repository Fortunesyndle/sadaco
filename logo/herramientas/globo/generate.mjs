import fs from 'node:fs';
import { createRequire } from 'node:module';
import { geoOrthographic, geoPath, geoGraticule, geoCentroid, geoArea } from 'd3-geo';
import * as topojson from 'topojson-client';

const require = createRequire(import.meta.url);
const Jimp = require('jimp');
const potrace = require('potrace');

const BLUE = '#004AAD', GREEN = '#7ED957', WHITE = '#FFFFFF', NAVY = '#0A2A5C', RED = '#CF142B';
const CX = 249, CY = 252, R = 156;
const ROTATE = [75, -15];
/* ---------- geography ---------- */

const land50 = JSON.parse(fs.readFileSync('node_modules/world-atlas/land-50m.json'));
const countries10 = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-10m.json'));
const land = topojson.feature(land50, land50.objects.land);
const countryFeatures = topojson.feature(countries10, countries10.objects.countries).features;
const venezuela10 = countryFeatures.find(f => f.id === '862');
const usa10 = countryFeatures.find(f => f.id === '840');
const isHawaii = poly => Math.max(...poly[0].map(p => p[1])) < 30 && Math.min(...poly[0].map(p => p[0])) < -140;
const usa = {
  ...usa10,
  geometry: { type: 'MultiPolygon', coordinates: usa10.geometry.coordinates.filter(poly => !isHawaii(poly)) },
};
const MAX_LAT = 13.5;
const venezuela = {
  ...venezuela10,
  geometry: {
    type: 'MultiPolygon',
    coordinates: venezuela10.geometry.coordinates.filter(poly => Math.min(...poly[0].map(p => p[1])) < MAX_LAT),
  },
};

function spherical(feature) {
  if (geoArea(feature) <= 2 * Math.PI) return feature;
  const g = feature.geometry;
  const rev = poly => poly.map(ring => ring.slice().reverse());
  const coordinates = g.type === 'Polygon' ? rev(g.coordinates) : g.coordinates.map(rev);
  return { ...feature, geometry: { ...g, coordinates } };
}

const disputed = JSON.parse(fs.readFileSync('data/ne_10m_admin_0_disputed_areas.geojson'));
const esequibo = spherical(disputed.features.find(f => /Claimed by Venezuela/.test(f.properties.NOTE_BRK || '')));

const projection = geoOrthographic().rotate(ROTATE).translate([CX, CY]).scale(R).clipAngle(90).precision(0.1);
const path = geoPath(projection);

const D = {
  sphere: path({ type: 'Sphere' }),
  land: path(land),
  graticule: path(geoGraticule().step([15, 15])()),
  ven: path(venezuela),
  eseq: path(esequibo),
  usa: path(usa),
  meridian: path({ type: 'LineString', coordinates: Array.from({ length: 181 }, (_, i) => [-66, i - 90]) }),
  parallel: path({ type: 'LineString', coordinates: Array.from({ length: 361 }, (_, i) => [i - 180, 7]) }),
};
const [vx, vy] = projection(geoCentroid(venezuela)).map(n => +n.toFixed(2));
const vb = path.bounds({ type: 'FeatureCollection', features: [venezuela, esequibo] });

/* ---------- laurel traced from the original logo ---------- */

async function traceLaurel() {
  const S = 4;
  const img = await Jimp.read('../../referencias/sadaco-international-logo.png');
  img.resize(img.bitmap.width * S, img.bitmap.height * S, Jimp.RESIZE_BILINEAR);
  const { width, height } = img.bitmap;
  img.scan(0, 0, width, height, function (x, y, idx) {
    const d = this.bitmap.data;
    const r = d[idx], g = d[idx + 1], b = d[idx + 2], a = d[idx + 3];
    const blue = a > 128 && b > 110 && r < 140 && g < 170 && b - r > 60;
    const outside = Math.hypot(x / S - CX, y / S - CY) > R + 4;
    const v = blue && outside ? 0 : 255;
    d[idx] = d[idx + 1] = d[idx + 2] = v; d[idx + 3] = 255;
  });
  const buf = await img.getBufferAsync(Jimp.MIME_PNG);
  const svg = await new Promise((res, rej) =>
    potrace.trace(buf, { threshold: 128, turdSize: 40, optTolerance: 0.3, color: BLUE }, (e, s) => e ? rej(e) : res(s)));
  return { d: svg.match(/ d="([^"]+)"/)[1], scale: 1 / S };
}

/* ---------- composition ---------- */

function svgDoc(inner, defs = '') {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
<defs><clipPath id="sph"><path d="${D.sphere}"/></clipPath>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.4"/></filter>${defs}</defs>
${inner}
</svg>`;
}

function base({ landFill = GREEN, landOpacity = 1, under = '', over = '', gridOpacity = 1 } = {}, laurel) {
  return `<g transform="scale(${laurel.scale})"><path d="${laurel.d}" fill="${BLUE}"/></g>
<path d="${D.sphere}" fill="${BLUE}"/>
<g clip-path="url(#sph)">
  <path d="${D.land}" fill="${landFill}" fill-opacity="${landOpacity}"/>
  ${under}
  <path d="${D.graticule}" fill="none" stroke="${WHITE}" stroke-width="1.35" stroke-opacity="${gridOpacity}"/>
  ${over}
</g>`;
}

const venShape = (fill, extra = '') => `<g fill="${fill}" stroke="${fill}" stroke-width=".35" stroke-linejoin="round" ${extra}>
  <path d="${D.ven}"/><path d="${D.eseq}"/></g>`;
const venOutline = (color, w) => `<g fill="none" stroke="${color}" stroke-width="${w}" stroke-linejoin="round">
  <path d="${D.ven}"/><path d="${D.eseq}"/></g>`;
const usaShape = fill => `<path d="${D.usa}" fill="${fill}" stroke="${fill}" stroke-width=".35" stroke-linejoin="round"/>`;

const EDGE = '#7F95AE';
function relief(shape, { k = 1, depth = 2.5, dx = 5, dy = 7.5 } = {}) {
  const at = (x, y) => `translate(${(x / k).toFixed(3)},${(y / k).toFixed(3)})`;
  const edge = Array.from({ length: 8 }, (_, i) => {
    const f = (i + 1) / 8;
    return `<g transform="${at(depth * f * .6, depth * f)}">${shape(EDGE)}</g>`;
  }).reverse().join('');
  return `<g transform="${at(dx, dy)}" opacity=".6" filter="url(#castShadow)">${shape(NAVY)}</g>
    <g transform="${at(depth * .9, depth * 1.4)}" opacity=".7" filter="url(#soft)">${shape(NAVY)}</g>
    ${edge}<g filter="url(#bevel)">${shape(WHITE)}</g>`;
}

const RELIEF_DEFS = `
  <filter id="castShadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="bevel" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceAlpha" stdDeviation=".8" result="bump"/>
    <feDiffuseLighting in="bump" surfaceScale="2.6" diffuseConstant="1" lighting-color="#FFFFFF" result="light">
      <feDistantLight azimuth="235" elevation="58"/></feDiffuseLighting>
    <feComponentTransfer in="light" result="shade">
      <feFuncR type="linear" slope=".82" intercept=".3"/><feFuncG type="linear" slope=".78" intercept=".34"/>
      <feFuncB type="linear" slope=".7" intercept=".42"/></feComponentTransfer>
    <feComposite in="shade" in2="SourceAlpha" operator="in"/></filter>`;

function pop(s, content, { dx = 2.5, dy = 3.5, shadow = .4 } = {}) {
  const t = `translate(${vx},${vy}) scale(${s}) translate(${-vx},${-vy})`;
  return `<g transform="translate(${dx},${dy}) ${t}" opacity="${shadow}" filter="url(#soft)">${venShape(NAVY)}</g>
    <g transform="${t}">${content}</g>`;
}

const PIN = (x, y, s = 1, fill = WHITE, stroke = BLUE, dot = BLUE) => `<g transform="translate(${x},${y}) scale(${s})">
  <ellipse cx="0" cy="1" rx="7" ry="2.5" fill="${NAVY}" opacity=".35"/>
  <path d="M0,0 C-3,-7 -13,-14 -13,-25 A13,13 0 1 1 13,-25 C13,-14 3,-7 0,0Z" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
  <circle cx="0" cy="-25" r="5.5" fill="${dot}"/></g>`;

const TACK_BODY = `<rect x="-8.5" y="-19.5" width="17" height="4.5" rx="2.2"/>
    <path d="M-4.2,-19.5 C-3,-23 -3,-27 -3.6,-30.5 H3.6 C3,-27 3,-23 4.2,-19.5 Z"/>
    <rect x="-10" y="-38.5" width="20" height="8.5" rx="3.2"/>`;
const THUMBTACK = (x, y, s = 1, tilt = 28) => `<g transform="translate(${x},${y}) scale(${s})">
  <ellipse cx="0" cy="0.6" rx="4.5" ry="1.6" fill="${NAVY}" opacity=".45" filter="url(#pinShadow)"/>
  <g transform="rotate(${tilt})">
    <polygon points="-1,-15 1,-15 0.35,-1.2 0,0 -0.35,-1.2" fill="url(#needle)"/>
    <g fill="${WHITE}" stroke="${WHITE}" stroke-width="2.6" stroke-linejoin="round">${TACK_BODY}</g>
    <g fill="url(#tackBody)">${TACK_BODY}</g>
    <rect x="-7.5" y="-37.3" width="3.2" height="6" rx="1.4" fill="#FFFFFF" opacity=".45"/>
    <rect x="-6.3" y="-18.6" width="2.4" height="2.8" rx="1" fill="#FFFFFF" opacity=".35"/>
  </g>
</g>`;

const PUSHPIN = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})">
  <ellipse cx="0" cy="0.8" rx="5" ry="1.8" fill="${NAVY}" opacity=".4" filter="url(#pinShadow)"/>
  <polygon points="-1.9,-33 1.9,-33 0.8,-3.5 0,0 -0.8,-3.5" fill="url(#needle)"/>
  <circle cx="0" cy="-41" r="11" fill="url(#pinBall)"/>
  <ellipse cx="-3.6" cy="-45.2" rx="3.6" ry="2.4" fill="#FFFFFF" opacity=".55" transform="rotate(-25 -3.6 -45.2)"/>
</g>`;

const PUSHPIN_DEFS = `
  <radialGradient id="pinBall" cx=".38" cy=".32" r=".78">
    <stop offset="0" stop-color="#FF7B80"/><stop offset=".5" stop-color="#EF3F47"/><stop offset="1" stop-color="#C9262E"/></radialGradient>
  <linearGradient id="needle" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8E959C"/><stop offset=".45" stop-color="#DADDE0"/><stop offset="1" stop-color="#9AA1A8"/></linearGradient>
  <filter id="pinShadow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.8"/></filter>
  <linearGradient id="tackBody" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F0525B"/><stop offset=".45" stop-color="#D81E2C"/><stop offset="1" stop-color="#9E1320"/></linearGradient>`;

const VARIANTS = [
  ['00-base', 'Base: América al centro', 'El globo original girado, sin marcar Venezuela.', () => ({})],
  ['01-blanco', 'Venezuela en blanco', 'El contraste más limpio: Venezuela en blanco sobre el verde del continente.',
    () => ({ over: venShape(WHITE) })],
  ['02-azul-profundo', 'Azul profundo', 'Venezuela en azul oscuro con contorno blanco. Sobrio y corporativo.',
    () => ({ over: venOutline(WHITE, 4) + venShape(NAVY) })],
  ['03-tricolor', 'Tricolor', 'Venezuela con los tres colores de la bandera. El más explícito.',
    () => ({ over: pop(1.35, venOutline(NAVY, 8 / 1.35) + venOutline(WHITE, 5 / 1.35) + venShape('url(#flag)')) }),
    `<linearGradient id="flag" gradientUnits="userSpaceOnUse" x1="0" y1="${vb[0][1]}" x2="0" y2="${vb[1][1]}">
      <stop offset="0" stop-color="#FFCC00"/><stop offset=".3333" stop-color="#FFCC00"/>
      <stop offset=".3333" stop-color="#00247D"/><stop offset=".6666" stop-color="#00247D"/>
      <stop offset=".6666" stop-color="#CF142B"/><stop offset="1" stop-color="#CF142B"/></linearGradient>`],
  ['04-pin', 'Pin de ubicación', 'Un marcador de mapa clavado en Venezuela: "aquí estamos".',
    () => ({ over: pop(1.3, venOutline(WHITE, 3.5 / 1.3) + venShape(RED)) + PIN(vx, vy, 1.6, RED, WHITE, WHITE) })],
  ['05-ondas', 'Ondas de señal', 'Venezuela en blanco emitiendo ondas: la sede que irradia hacia la región.',
    () => ({
      over: [[24, 3, 1], [38, 2.5, .6], [52, 2, .3]].map(([r, w, o]) =>
        `<circle cx="${vx}" cy="${vy}" r="${r}" fill="none" stroke="${WHITE}" stroke-width="${w}" stroke-opacity="${o}"/>`).join('') + venShape(WHITE),
    })],
  ['06-lupa', 'Lupa', 'Una lupa sobre el mapa amplía Venezuela y la hace legible incluso en tamaños pequeños.',
    () => {
      const K = 2.6, LR = 46;
      const z = `translate(${vx},${vy}) scale(${K}) translate(${-vx},${-vy})`;
      const hx1 = vx + LR * Math.SQRT1_2, hy1 = vy + LR * Math.SQRT1_2;
      const hx2 = hx1 + 26, hy2 = hy1 + 26;
      return {
        over: `<g stroke-linecap="round"><line x1="${hx1}" y1="${hy1}" x2="${hx2}" y2="${hy2}" stroke="${NAVY}" stroke-width="12"/>
            <line x1="${hx1}" y1="${hy1}" x2="${hx2}" y2="${hy2}" stroke="${WHITE}" stroke-width="7"/></g>
          <g clip-path="url(#lens)"><rect x="0" y="0" width="500" height="500" fill="${BLUE}"/>
            <g transform="${z}"><path d="${D.land}" fill="${GREEN}"/>
              <path d="${D.graticule}" fill="none" stroke="${WHITE}" stroke-width="${1.35 / K * 1.4}"/>
              ${venOutline(BLUE, 1.2 / K * 2)}${venShape(WHITE)}</g></g>
          <circle cx="${vx}" cy="${vy}" r="${LR + 2.2}" fill="none" stroke="${NAVY}" stroke-width="1.6"/>
          <circle cx="${vx}" cy="${vy}" r="${LR}" fill="none" stroke="${WHITE}" stroke-width="4.5"/>`,
      };
    },
    `<clipPath id="lens"><circle cx="${vx}" cy="${vy}" r="46"/></clipPath>`],
  ['07-resplandor', 'Resplandor', 'Venezuela verde con un halo de luz blanca alrededor.',
    () => ({ over: `<g filter="url(#glow)">${venOutline(WHITE, 14)}${venShape(WHITE)}</g>` + venOutline(WHITE, 3) + venShape(GREEN) }),
    `<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="6"/></filter>`],
  ['08-relieve', 'Relieve', 'Venezuela y Estados Unidos en blanco, levantados del mapa con canto y sombra, como piezas en relieve.',
    () => {
      const K = 1.65;
      const t = `translate(${vx},${vy}) scale(${K}) translate(${-vx},${-vy})`;
      return { over: relief(usaShape, { depth: 2.1, dx: 4.5, dy: 6.5 }) + `<g transform="${t}">${relief(venShape, { k: K })}</g>` };
    },
    RELIEF_DEFS],
  ['09-coordenadas', 'Coordenadas', 'El meridiano y el paralelo que cruzan Venezuela se resaltan y marcan su posición.',
    () => ({
      gridOpacity: .55,
      over: `<g fill="none" stroke="${WHITE}" stroke-width="3.2"><path d="${D.meridian}"/><path d="${D.parallel}"/></g>` +
        venShape(WHITE) +
        `<circle cx="${vx}" cy="${vy}" r="11" fill="none" stroke="${NAVY}" stroke-width="2.5"/><circle cx="${vx}" cy="${vy}" r="4.5" fill="${NAVY}"/>`,
    })],
  ['10-chincheta', 'Chincheta', 'Una chincheta roja clavada en Venezuela, como en un mapa de pared: "aquí estamos".',
    () => ({ over: pop(1.3, venOutline(BLUE, 3.5 / 1.3) + venShape(WHITE)) + THUMBTACK(vx, vy, 1.75) }),
    PUSHPIN_DEFS],
];

const laurel = await traceLaurel();
fs.mkdirSync('svg', { recursive: true });
const meta = [];
for (const [file, title, desc, build, defs = ''] of VARIANTS) {
  fs.writeFileSync(`svg/${file}.svg`, svgDoc(base(build(), laurel), defs));
  meta.push({ file, title, desc });
}
fs.writeFileSync('variants.js', `window.VARIANTS = ${JSON.stringify(meta, null, 2)};\nwindow.CENTROID = [${vx}, ${vy}];\n`);
console.log('centroid', vx, vy, 'bounds', vb.map(p => p.map(n => n.toFixed(1))));
console.log('wrote', meta.length, 'variants');
