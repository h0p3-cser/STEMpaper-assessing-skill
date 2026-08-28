#!/usr/bin/env node
// radar-chart.js — Generate an SVG radar chart for paper-rubric-review.
//
// Supports any number of axes (3 to ~12). Pass a JSON object where keys are
// category labels and values are 0-100 scores.
//
// Usage:
//   node radar-chart.js '{"问题价值":85,"方法严谨":80,"证据强度":75,"论文表达":60,"学术价值":80}' > radar.svg
//   echo '{"research":78,"paper":45,"potential":60}' | node radar-chart.js --stdin > radar.svg
//
// Optional second arg: --max <N> (default 100) — sets the outer ring value.
// Optional third arg: --rings <N> (default 4) — number of concentric guide rings.
//
// Output: SVG document on stdout. No external dependencies.

'use strict';

function readInput() {
  const args = process.argv.slice(2);
  if (args.includes('--stdin')) {
    return require('fs').readFileSync(0, 'utf8');
  }
  if (args.length === 0) {
    process.stderr.write('Usage: node radar-chart.js \'{"label1":N,"label2":N,...}\'\n');
    process.exit(1);
  }
  return args[0];
}

function parseFlags(argv) {
  const flags = { max: 100, rings: 4, title: null };
  for (let i = 1; i < argv.length; i++) {
    if (argv[i] === '--max') flags.max = parseFloat(argv[++i]);
    else if (argv[i] === '--rings') flags.rings = parseInt(argv[++i], 10);
    else if (argv[i] === '--title') flags.title = argv[++i];
  }
  return flags;
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

function build(data, flags) {
  // Accept any {label: value} object; sort keys for stable layout
  const entries = Object.keys(data)
    .map(k => ({ label: k, value: clamp(Number(data[k]) || 0, 0, flags.max) }))
    .sort((a, b) => a.label.localeCompare(b.label));

  if (entries.length < 3) {
    process.stderr.write(`Error: need at least 3 axes, got ${entries.length}\n`);
    process.exit(1);
  }
  if (entries.length > 16) {
    process.stderr.write(`Error: too many axes (${entries.length} > 16); readability suffers\n`);
    process.exit(1);
  }

  const n = entries.length;
  // Adapt canvas size to number of axes (more axes = bigger chart)
  const W = Math.max(380, 100 + n * 90);
  const H = W + (flags.title ? 30 : 0);
  const cx = W / 2;
  const cy = H / 2 + (flags.title ? 15 : 0);
  const R = Math.min(W, H - (flags.title ? 60 : 40)) / 2 - 60;

  // Angles: top (12 o'clock), then clockwise
  const angles = [];
  for (let i = 0; i < n; i++) {
    angles.push((90 - i * (360 / n)) * Math.PI / 180);
  }

  // Background grid (concentric polygons at evenly spaced levels)
  const levels = [];
  for (let i = 1; i <= flags.rings; i++) levels.push(i / flags.rings);
  const gridPolys = levels.map(level => {
    const pts = angles.map(a => {
      const x = cx + R * level * Math.cos(a);
      const y = cy - R * level * Math.sin(a);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
    return `  <polygon points="${pts}" fill="none" stroke="#d4d4d8" stroke-width="1"/>`;
  });

  // Axis lines
  const axisLines = angles.map(a => {
    const x = cx + R * Math.cos(a);
    const y = cy - R * Math.sin(a);
    return `  <line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="#d4d4d8" stroke-width="1"/>`;
  });

  // Data polygon
  const dataPts = angles.map((a, i) => {
    const v = entries[i].value;
    const x = cx + R * (v / flags.max) * Math.cos(a);
    const y = cy - R * (v / flags.max) * Math.sin(a);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  // Data point markers
  const dataDots = angles.map((a, i) => {
    const v = entries[i].value;
    const x = cx + R * (v / flags.max) * Math.cos(a);
    const y = cy - R * (v / flags.max) * Math.sin(a);
    return `  <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3.5" fill="#2563eb" stroke="white" stroke-width="1.5"/>`;
  });

  // Axis labels (category name + value)
  const labelEls = angles.map((a, i) => {
    const lr = R + 25;
    const lx = cx + lr * Math.cos(a);
    const ly = cy - lr * Math.sin(a);
    const cosA = Math.cos(a);
    const anchor = Math.abs(cosA) < 0.1 ? 'middle' : (cosA > 0 ? 'start' : 'end');
    const v = entries[i].value;
    return `  <text x="${lx.toFixed(1)}" y="${(ly - 4).toFixed(1)}" text-anchor="${anchor}" font-size="13" font-weight="600" fill="#1f2937">${entries[i].label}</text>
  <text x="${lx.toFixed(1)}" y="${(ly + 12).toFixed(1)}" text-anchor="${anchor}" font-size="12" font-weight="700" fill="#2563eb">${v.toFixed(1)} / ${flags.max}</text>`;
  });

  // Level labels (along the top axis)
  const levelLabels = levels.map(level => {
    const y = cy - R * level;
    return `  <text x="${(cx + 4).toFixed(1)}" y="${(y + 3).toFixed(1)}" font-size="9" fill="#a1a1aa">${Math.round(level * flags.max)}</text>`;
  });

  const titleEl = flags.title
    ? `  <text x="${cx}" y="20" text-anchor="middle" font-size="14" font-weight="700" fill="#111827">${flags.title}</text>\n`
    : '';

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <rect width="${W}" height="${H}" fill="#fafafa"/>
${titleEl}${gridPolys.join('\n')}
${axisLines.join('\n')}
  <polygon points="${dataPts}" fill="rgba(37, 99, 235, 0.18)" stroke="#2563eb" stroke-width="2" stroke-linejoin="round"/>
${dataDots.join('\n')}
${labelEls.join('\n')}
${levelLabels.join('\n')}
</svg>
`;
}

const raw = readInput();
let data;
try {
  data = JSON.parse(raw);
} catch (e) {
  process.stderr.write(`Invalid JSON: ${e.message}\n`);
  process.exit(1);
}
const flags = parseFlags(process.argv.slice(2));
process.stdout.write(build(data, flags));
