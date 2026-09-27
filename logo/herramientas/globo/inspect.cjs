const fs = require('fs');

const disputed = JSON.parse(fs.readFileSync('data/ne_10m_admin_0_disputed_areas.geojson'));
for (const f of disputed.features) {
  const p = f.properties;
  const txt = JSON.stringify(p);
  if (/VEN|GUY|Venez|Guyan|Essequ/i.test(txt)) {
    console.log(p.NAME || p.NAME_LONG, '|', p.ADMIN, '|', p.NOTE_BRK || p.NOTE_ADM0 || '', '|', f.geometry.type);
  }
}

const rivers = JSON.parse(fs.readFileSync('data/ne_10m_rivers_lake_centerlines.geojson'));
const ess = rivers.features.filter(f => f.properties.name === 'Essequibo');
for (const f of ess) {
  const lines = f.geometry.type === 'LineString' ? [f.geometry.coordinates] : f.geometry.coordinates;
  lines.forEach((l, i) => console.log('Essequibo line', i, 'pts', l.length, 'start', l[0], 'end', l[l.length - 1]));
}
