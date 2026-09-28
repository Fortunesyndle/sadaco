import fs from 'node:fs';
import { geoMercator, geoPath, geoGraticule, geoArea } from 'd3-geo';
import * as topojson from 'topojson-client';

const W = 640, H = 480, PAD = 24;
const OJEDA = [-71.31, 10.2];

const countries10 = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-10m.json'));
const land50 = JSON.parse(fs.readFileSync('node_modules/world-atlas/land-50m.json'));
const venezuela10 = topojson.feature(countries10, countries10.objects.countries).features.find(f => f.id === '862');
const venezuela = {
  ...venezuela10,
  geometry: {
    type: 'MultiPolygon',
    coordinates: venezuela10.geometry.coordinates.filter(poly => Math.min(...poly[0].map(p => p[1])) < 13.5),
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

const projection = geoMercator().fitExtent([[PAD, PAD], [W - PAD, H - PAD]], {
  type: 'FeatureCollection', features: [venezuela, esequibo],
}).clipExtent([[0, 0], [W, H]]);
const path = geoPath(projection).digits(1);

const [ox, oy] = projection(OJEDA).map(n => +n.toFixed(1));

const out = {
  width: W,
  height: H,
  land: path(topojson.feature(land50, land50.objects.land)),
  graticule: path(geoGraticule().extent([[-76, -1], [-56, 16]]).step([2, 2])()),
  venezuela: path(venezuela),
  esequibo: path(esequibo),
  ojeda: { x: ox, y: oy },
};

fs.writeFileSync('../../../web/src/data/mapa-venezuela.json', JSON.stringify(out));
console.log('ojeda', ox, oy, Object.fromEntries(Object.entries(out).map(([k, v]) => [k, typeof v === 'string' ? v.length : v])));
