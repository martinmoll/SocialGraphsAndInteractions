#!/usr/bin/env node
/**
 * ArcDeck PPTX Generator — v6 (multi-template + charts + adaptive layout)
 *
 * Usage: node generate_pptx.js [template]
 *   Templates: ocean (default), minimal, dark, warm
 *
 * Hard rules:
 *  1. MAX 1 figure or table per slide — extras get their own slide
 *  2. Figures fill the largest available space, aspect ratio preserved
 *  3. No overlapping elements — every shape has its own clear zone
 *  4. Template-driven styling with 4 built-in themes
 *  5. VE diagrams get adaptive height — more room when fewer bullets
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const WS = process.env.ARCDECK_WORKSPACE || __dirname;
const FIG = path.join(WS, "figures");

// ══════════════════════════════════════════════
//  TEMPLATES — 4 distinct presentation styles
// ══════════════════════════════════════════════

const TEMPLATES = {
  ocean: {
    name: "Ocean Gradient",
    FH: "Georgia", FB: "Calibri",
    C: {
      navy: "0D1B2A", deep: "1B2A4A", pri: "065A82", teal: "1C7293",
      mid: "21295C", acc: "0891B2", accLt: "67E8F9", wh: "FFFFFF",
      bg: "F0F4F8", card: "FFFFFF", tx: "1E293B", txM: "475569", txL: "94A3B8",
      red: "DC2626", grn: "059669", div: "CBD5E1",
    },
    veCols: ["065A82", "1C7293", "21295C", "059669"],
    chartCols: ["065A82", "1C7293", "0891B2", "21295C", "059669", "DC2626"],
  },
  minimal: {
    name: "Clean Minimal",
    FH: "Calibri Light", FB: "Calibri",
    C: {
      navy: "2B2D42", deep: "3D3F5C", pri: "E63946", teal: "457B9D",
      mid: "1D3557", acc: "E63946", accLt: "F4A261", wh: "FFFFFF",
      bg: "FFFFFF", card: "FFFFFF", tx: "2B2D42", txM: "555770", txL: "8D99AE",
      red: "E63946", grn: "2A9D8F", div: "D6D8E7",
    },
    veCols: ["E63946", "457B9D", "2A9D8F", "1D3557"],
    chartCols: ["E63946", "457B9D", "2A9D8F", "1D3557", "F4A261", "264653"],
  },
  dark: {
    name: "Dark Mode",
    FH: "Trebuchet MS", FB: "Calibri",
    C: {
      navy: "16161A", deep: "1A1A2E", pri: "7F5AF0", teal: "2CB67D",
      mid: "3A3A5C", acc: "7F5AF0", accLt: "B8A9FF", wh: "FFFFFE",
      bg: "242629", card: "2C2C34", tx: "FFFFFE", txM: "94A1B2", txL: "72757E",
      red: "EF4444", grn: "2CB67D", div: "3A3A5C",
    },
    veCols: ["7F5AF0", "2CB67D", "FF6B6B", "E8A838"],
    chartCols: ["7F5AF0", "2CB67D", "FF6B6B", "E8A838", "72B7F2", "F472B6"],
  },
  warm: {
    name: "Warm Academic",
    FH: "Georgia", FB: "Calibri",
    C: {
      navy: "3C2415", deep: "4A3228", pri: "C45B3E", teal: "5B8A72",
      mid: "2C5F2D", acc: "C45B3E", accLt: "E8B4A0", wh: "FFFFFF",
      bg: "FAF6F0", card: "FFFFFF", tx: "3C2415", txM: "6B5B4E", txL: "A09080",
      red: "C45B3E", grn: "5B8A72", div: "D4C8B8",
    },
    veCols: ["C45B3E", "5B8A72", "D4A84B", "6B5B4E"],
    chartCols: ["C45B3E", "5B8A72", "D4A84B", "6B5B4E", "8B4513", "2E8B57"],
  },
};

const TMPL = process.argv[2] || process.env.ARCDECK_TEMPLATE || "ocean";
const T = TEMPLATES[TMPL] || TEMPLATES.ocean;
const C = T.C;
const FH = T.FH, FB = T.FB;
const VC = T.veCols;
const CC = T.chartCols;

console.log(`Template: ${T.name} (${TMPL})`);

const SW = 13.33, SH = 7.5, ML = 0.6, CW = SW - 1.2;

// ── Helpers ──

function parseLaTeX(t) {
  const out = []; let r = t;
  while (r.length) {
    const b = r.match(/\\textbf\{([^}]+)\}/), c = r.match(/\\textcolor\{(\w+)\}\{([^}]+)\}/);
    let fi = r.length, mt = null, m = null;
    if (b && b.index < fi) { fi = b.index; mt = "b"; m = b; }
    if (c && c.index < fi) { fi = c.index; mt = "c"; m = c; }
    if (!m) { if (r) out.push({ t: r }); break; }
    if (fi > 0) out.push({ t: r.substring(0, fi) });
    if (mt === "b") out.push({ t: m[1], bold: true });
    else out.push({ t: m[2], bold: true, col: m[1] === "red" ? C.red : C.acc });
    r = r.substring(fi + m[0].length);
  }
  return out.filter(s => s.t);
}

function shd() { return { type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.12 }; }
function fp(n) { return path.join(FIG, n); }
function fe(n) { return fs.existsSync(fp(n)); }
// Resolve slide title: JSON may use "title" or "subsection" depending on agent output
function slideTitle(sd) { return sd.title || sd.subsection || ""; }

function fitImg(name, mw, mh) {
  try {
    const buf = fs.readFileSync(fp(name));
    let pw = 0, ph = 0;
    if (buf[0] === 0x89 && buf[1] === 0x50) { pw = buf.readUInt32BE(16); ph = buf.readUInt32BE(20); }
    else if (buf[0] === 0xFF && buf[1] === 0xD8) {
      let o = 2;
      while (o < buf.length - 4) {
        if (buf[o] !== 0xFF) break;
        const mk = buf[o + 1];
        if (mk === 0xC0 || mk === 0xC2) { ph = buf.readUInt16BE(o + 5); pw = buf.readUInt16BE(o + 7); break; }
        o += 2 + buf.readUInt16BE(o + 2);
      }
    }
    if (pw > 0 && ph > 0) {
      const ar = pw / ph;
      let w = mw, h = mw / ar;
      if (h > mh) { h = mh; w = mh * ar; }
      return { w, h };
    }
  } catch (_) {}
  return { w: mw, h: mh };
}

function extractValue(item) {
  if (typeof item.value === "number") return item.value;
  const m = String(item.label).match(/[\d.]+/);
  return m ? parseFloat(m[0]) : 1;
}

// Scale font size proportionally to available height (base height = 2.0")
// Absolute cap prevents oversized fonts when VE area is very tall
function sf(base, h) { return Math.min(Math.round(base * Math.min(h / 2.0, 1.5)), base + 6); }

// Clamp x position and width to slide bounds
function clampX(x, w) {
  const cx = Math.max(x, 0.1);
  const cw = Math.min(w, SW - 0.1 - cx);
  return { x: cx, w: Math.max(cw, 0.3) };
}

// Safe item slice — cap VE item count to avoid unreadable tiny elements
function capItems(items, max) { return items.slice(0, max); }

// ── Load + split multi-visual slides ──
const plan = JSON.parse(fs.readFileSync(path.join(WS, "slide_plan_refined.json"), "utf8"));
const meta = plan.metadata;
const allSlides = [];

for (const sd of plan.slides) {
  const vis = [...(sd.images || []), ...(sd.tables || [])].filter(fe);
  if (vis.length <= 1) {
    allSlides.push({ ...sd, _img: vis[0] || null });
  } else {
    allSlides.push({ ...sd, _img: vis[0] });
    for (let i = 1; i < vis.length; i++) {
      allSlides.push({
        section: sd.section, title: slideTitle(sd), subsection: sd.subsection,
        template_id: "_FIGPAGE", bullets: [], paragraph: "",
        images: [], tables: [], reference: "", visual_element: null,
        _img: vis[i],
      });
    }
  }
}

// ── Pres ──
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const authorStr = meta.author || meta.authors || "";
pres.author = authorStr;
pres.title = meta.title;

// ── Bullet rows ──
function bRows(bullets, sz, subSz, col, subCol) {
  const rows = [];
  if (!bullets || !bullets.length) return rows;
  for (const raw of bullets) {
    const b = typeof raw === "string" ? { text: raw } : raw;
    const segs = parseLaTeX(b.text || "");
    for (let i = 0; i < segs.length; i++) {
      const s = segs[i];
      rows.push({ text: s.t, options: {
        fontFace: FB, fontSize: sz, color: s.col || col, bold: s.bold || false,
        ...(i === 0 ? { bullet: true } : {}),
        ...(i === segs.length - 1 ? { breakLine: true } : {}),
      }});
    }
    for (const sub of (b.sub || [])) {
      rows.push({ text: sub, options: {
        fontFace: FB, fontSize: subSz, color: subCol,
        bullet: true, indentLevel: 1, breakLine: true,
      }});
    }
  }
  if (rows.length) delete rows[rows.length - 1].options.breakLine;
  return rows;
}

function putBullets(s, bullets, x, y, w, h) {
  const r = bRows(bullets, 15, 13, C.tx, C.txM);
  if (r.length) s.addText(r, { x, y, w, h, valign: "top", paraSpaceAfter: 6, margin: [0, 0, 0, 0.15] });
}

// Paragraph mode — flowing text instead of bullets
function putParagraph(s, text, x, y, w, h) {
  if (!text) return;
  const segs = parseLaTeX(text);
  const runs = segs.map(seg => ({
    text: seg.t,
    options: { fontFace: FB, fontSize: 14, color: seg.col || C.tx, bold: seg.bold || false }
  }));
  s.addText(runs, { x, y, w, h, valign: "top", lineSpacingMultiple: 1.3, margin: [0, 0, 0, 0] });
}

function putTitle(s, title) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: SW, h: 0.05, fill: { color: C.pri } });
  s.addText(title, {
    x: ML, y: 0.25, w: CW, h: 0.5,
    fontFace: FH, fontSize: 26, color: C.tx, bold: true, align: "left", valign: "top", margin: 0
  });
  return 0.85;
}

// Count effective lines in bullet list
function countLines(bullets) {
  return (bullets || []).reduce((c, b) => {
    const item = typeof b === "string" ? { text: b } : b;
    return c + 1 + ((item.sub || []).length);
  }, 0);
}

// ══════════════════════════════════════════════
//  SLIDE TYPES
// ══════════════════════════════════════════════

function mkTitle() {
  const s = pres.addSlide(); s.background = { color: C.navy };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: SW, h: 0.05, fill: { color: C.acc } });
  s.addText(meta.title, { x: 1, y: 1.4, w: 11.3, h: 2, fontFace: FH, fontSize: 36, color: C.wh, bold: true, align: "left", valign: "top", margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 1, y: 3.6, w: 2.5, h: 0.03, fill: { color: C.acc } });
  s.addText(authorStr, { x: 1, y: 4.0, w: 11.3, h: 0.6, fontFace: FB, fontSize: 16, color: C.accLt, align: "left", margin: 0 });
  s.addText(meta.organization, { x: 1, y: 4.7, w: 8, h: 0.5, fontFace: FB, fontSize: 14, color: C.txL, align: "left", margin: 0 });
  const pd = meta["publish_date"] || meta["publish date"] || "";
  if (pd) {
    s.addShape(pres.shapes.RECTANGLE, { x: 1, y: 5.6, w: 1.8, h: 0.42, fill: { color: C.acc } });
    s.addText(pd, { x: 1, y: 5.6, w: 1.8, h: 0.42, fontFace: FB, fontSize: 14, color: C.wh, bold: true, align: "center", valign: "middle", margin: 0 });
  }
}

function mkDivider(name) {
  const s = pres.addSlide(); s.background = { color: C.deep };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.06, h: SH, fill: { color: C.acc } });
  s.addText(name, { x: 1.1, y: 2.5, w: 10, h: 2, fontFace: FH, fontSize: 44, color: C.wh, bold: true, align: "left", valign: "middle", margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.1, y: 4.55, w: 3, h: 0.04, fill: { color: C.acc } });
}

function mkFigPage(sd) {
  const s = pres.addSlide(); s.background = { color: C.bg };
  putTitle(s, slideTitle(sd));
  const maxH = SH - 0.95 - 0.3;
  const d = fitImg(sd._img, CW, maxH);
  s.addImage({ path: fp(sd._img), x: ML + (CW - d.w) / 2, y: 0.95 + (maxH - d.h) / 2, w: d.w, h: d.h });
}

function mkImgSlide(sd) {
  const s = pres.addSlide(); s.background = { color: C.bg };
  const y0 = putTitle(s, slideTitle(sd));
  if (!sd._img) { putBullets(s, sd.bullets, ML, y0 + 0.1, CW, 6.0); return; }

  const probe = fitImg(sd._img, 100, 100);
  const ar = probe.w / probe.h;
  const nLines = countLines(sd.bullets);

  const bodyH = SH - y0 - 0.4;   // total usable height below title

  if (ar > 1.5) {
    // Wide image: bullets on top, image below
    const bulletH = Math.min(Math.max(nLines * 0.35, 1.0), Math.min(bodyH * 0.45, 2.8));
    putBullets(s, sd.bullets, ML, y0 + 0.1, CW, bulletH);
    const imgY = y0 + 0.1 + bulletH + 0.2;
    const imgAvailH = Math.max(SH - imgY - 0.3, 1.0);
    const d = fitImg(sd._img, CW, imgAvailH);
    s.addImage({ path: fp(sd._img), x: ML + (CW - d.w) / 2, y: imgY, w: d.w, h: d.h });
  } else {
    // Tall/square image: bullets left, image right
    const imgMaxW = 5.0, imgMaxH = Math.min(bodyH, 5.5);
    const d = fitImg(sd._img, imgMaxW, imgMaxH);
    const imgX = SW - 0.6 - d.w;
    const imgY = y0 + 0.1 + Math.max((bodyH - d.h) / 2, 0);
    s.addImage({ path: fp(sd._img), x: imgX, y: imgY, w: d.w, h: d.h });
    const bulletW = Math.max(imgX - ML - 0.3, 2.0);
    putBullets(s, sd.bullets, ML, y0 + 0.1, bulletW, bodyH);
  }
}

function mkTextSlide(sd) {
  const s = pres.addSlide(); s.background = { color: C.bg };
  const y0 = putTitle(s, slideTitle(sd));
  const ve = sd.visual_element;
  const veType = ve && (ve.type || ve.layout);
  const hasVE = ve && veType && ve.items && ve.items.length && VE[veType];

  if (hasVE) {
    // Dynamic split: bullets get proportional space, VE fills remaining (capped at 4.5")
    const nLines = countLines(sd.bullets);
    const bulletH = Math.max(Math.min(nLines * 0.38, 2.8), 0.5);
    putBullets(s, sd.bullets, ML, y0 + 0.1, CW, bulletH);
    const veY = y0 + 0.1 + bulletH + 0.2;
    const veH = Math.max(Math.min(SH - veY - 0.3, 4.5), 1.5);
    VE[veType](s, ve.items, veY, veH);
  } else if (sd.paragraph && sd.paragraph.length > 0) {
    putParagraph(s, sd.paragraph, ML, y0 + 0.1, CW, 6.0);
  } else {
    putBullets(s, sd.bullets, ML, y0 + 0.1, CW, 6.0);
  }
}

function mkConclusion(sd) {
  const s = pres.addSlide(); s.background = { color: C.navy };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: SW, h: 0.05, fill: { color: C.acc } });
  s.addText(slideTitle(sd), { x: ML, y: 0.25, w: CW, h: 0.5, fontFace: FH, fontSize: 28, color: C.wh, bold: true, align: "left", margin: 0 });

  const r = bRows(sd.bullets, 15, 13, C.wh, C.txL);
  for (const row of r) { if (row.options.bold && row.options.color === C.wh) row.options.color = C.accLt; }

  const ve = sd.visual_element;
  const cveType = ve && (ve.type || ve.layout);
  const hasVE = ve && ve.items && ve.items.length && cveType && VE[cveType];

  if (hasVE) {
    const nLines = countLines(sd.bullets);
    const bulletH = Math.max(Math.min(nLines * 0.38, 2.8), 0.5);
    if (r.length) s.addText(r, { x: ML, y: 1.0, w: CW, h: bulletH, valign: "top", paraSpaceAfter: 6, margin: [0, 0, 0, 0.15] });
    const veY = 1.0 + bulletH + 0.2;
    const veH = Math.max(Math.min(SH - veY - 0.3, 4.5), 1.5);
    VE[cveType](s, ve.items, veY, veH);
  } else {
    if (r.length) s.addText(r, { x: ML, y: 1.0, w: CW, h: 5.5, valign: "top", paraSpaceAfter: 6, margin: [0, 0, 0, 0.15] });
  }
}

function mkThankYou() {
  const s = pres.addSlide(); s.background = { color: C.navy };
  s.addText("Thank You", { x: 0, y: 2, w: SW, h: 1.5, fontFace: FH, fontSize: 48, color: C.wh, bold: true, align: "center", valign: "middle", margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: SW / 2 - 1.5, y: 3.7, w: 3, h: 0.03, fill: { color: C.acc } });
  s.addText(authorStr.split(",")[0] + " et al.", { x: 0, y: 4.1, w: SW, h: 0.5, fontFace: FB, fontSize: 16, color: C.accLt, align: "center", margin: 0 });
  s.addText(meta.organization, { x: 0, y: 4.7, w: SW, h: 0.5, fontFace: FB, fontSize: 13, color: C.txL, align: "center", margin: 0 });
}

// ══════════════════════════════════════════════
//  VISUAL ELEMENTS — all take (s, items, y, h)
//  y = top of VE area, h = available height
// ══════════════════════════════════════════════

function veProcessFlow(s, its, y, h) {
  const items = capItems(its, 6);
  const n = items.length, gap = 0.4;
  const bw = (CW - (n - 1) * gap) / n;
  const bh = Math.min(h - 0.1, 2.8);  // cap box height for proportions
  const by = y + (h - bh) / 2;        // center vertically
  const labelH = Math.min(bh * 0.28, 0.5);
  const fsLabel = sf(13, h), fsSub = sf(10, h);
  for (let i = 0; i < n; i++) {
    const x = ML + i * (bw + gap), col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: by, w: bw, h: bh, fill: { color: C.card }, rectRadius: 0.06, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: by, w: bw, h: 0.05, fill: { color: col } });
    s.addText(items[i].label || "", { x: x + 0.12, y: by + 0.12, w: bw - 0.24, h: labelH, fontFace: FB, fontSize: fsLabel, color: col, bold: true, align: "center", valign: "middle", margin: 0 });
    if (items[i].sublabel) s.addText(items[i].sublabel, { x: x + 0.12, y: by + 0.12 + labelH + 0.08, w: bw - 0.24, h: bh - labelH - 0.35, fontFace: FB, fontSize: fsSub, color: C.txM, align: "center", valign: "top", margin: 0 });
    if (i < n - 1) s.addText("\u27A1", { x: x + bw + 0.04, y: by + bh / 2 - 0.18, w: gap - 0.08, h: 0.36, fontFace: FB, fontSize: 20, color: C.acc, align: "center", valign: "middle", margin: 0 });
  }
}

function veCalloutCards(s, its, y, h) {
  const items = capItems(its, 6);
  const n = items.length, gap = 0.25;
  const cw = (CW - (n - 1) * gap) / n;
  const ch = Math.min(h - 0.1, 2.5);    // cap card height
  const cy = y + (h - ch) / 2;           // center vertically
  const fsLabel = sf(12, h), fsSub = sf(10, h);
  for (let i = 0; i < n; i++) {
    const x = ML + i * (cw + gap), col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.card }, rectRadius: 0.05, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: 0.06, h: ch, fill: { color: col } });
    s.addText(items[i].label || "", { x: x + 0.18, y: cy + 0.12, w: cw - 0.3, h: 0.35, fontFace: FB, fontSize: fsLabel, color: col, bold: true, align: "left", valign: "middle", margin: 0 });
    if (items[i].sublabel) s.addText(items[i].sublabel, { x: x + 0.18, y: cy + 0.5, w: cw - 0.3, h: ch - 0.6, fontFace: FB, fontSize: fsSub, color: C.txM, align: "left", valign: "top", margin: 0 });
  }
}

function veComparison(s, its, y, h) {
  const items = capItems(its, 5);
  const n = items.length, gap = 0.2;
  const cw = (CW - (n - 1) * gap) / n;
  const ch = Math.min(h, 3.0);            // cap panel height
  const cy = y + (h - ch) / 2;            // center vertically
  const headH = Math.min(ch * 0.18, 0.45);
  const fsSub = sf(10, h);
  for (let i = 0; i < n; i++) {
    const x = ML + i * (cw + gap);
    const tone = items[i].tone || "neutral";
    let hc = C.teal; if (tone === "positive") hc = C.grn; else if (tone === "negative") hc = C.txL;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.card }, rectRadius: 0.05, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: headH, fill: { color: hc } });
    s.addText(items[i].label || "", { x: x + 0.08, y: cy, w: cw - 0.16, h: headH, fontFace: FB, fontSize: sf(12, h), color: C.wh, bold: true, align: "center", valign: "middle", margin: 0 });
    const lines = (items[i].sublabel || "").split("\n");
    const ct = lines.map((l, j) => ({ text: l, options: { fontFace: FB, fontSize: fsSub, color: C.txM, breakLine: j < lines.length - 1 } }));
    s.addText(ct, { x: x + 0.1, y: cy + headH + 0.1, w: cw - 0.2, h: ch - headH - 0.2, valign: "top", margin: 0 });
  }
}

function veCycle(s, its, y, h) {
  const items = capItems(its, 8);
  const n = items.length, cx = SW / 2;
  const useH = Math.min(h, 3.5);          // cap usable height
  const cy = y + h / 2;
  const r = Math.min(useH / 2 - 0.2, 2.2);
  const nw = Math.min(r * 1.1, 2.2), nh = Math.min(r * 0.5, 0.85);
  s.addText("\u21BB", { x: cx - 0.25, y: cy - 0.2, w: 0.5, h: 0.4, fontFace: FB, fontSize: 22, color: C.div, align: "center", valign: "middle", margin: 0 });
  for (let i = 0; i < n; i++) {
    const ang = -Math.PI / 2 + (2 * Math.PI * i / n);
    const rawX = cx + r * Math.cos(ang) - nw / 2, rawY = cy + r * Math.sin(ang) - nh / 2;
    const nx = Math.max(rawX, 0.1), ny = Math.max(rawY, y);
    const col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: nx, y: ny, w: Math.min(nw, SW - 0.1 - nx), h: nh, fill: { color: col }, rectRadius: 0.05, shadow: shd() });
    const t = [{ text: items[i].label || "", options: { fontSize: sf(10, h), bold: true, color: C.wh, breakLine: !!items[i].sublabel } }];
    if (items[i].sublabel) t.push({ text: items[i].sublabel, options: { fontSize: sf(8, h), color: C.accLt } });
    s.addText(t, { x: nx + 0.06, y: ny + 0.03, w: Math.min(nw, SW - 0.1 - nx) - 0.12, h: nh - 0.06, fontFace: FB, align: "center", valign: "middle", margin: 0 });
  }
}

function veSplitPanel(s, items, y, h) {
  const gap = 0.3, pw = (CW - gap) / 2;
  const ph = Math.min(h, 3.0);            // cap panel height
  const py = y + (h - ph) / 2;            // center vertically
  const cols = [VC[0], VC[1]];
  for (let i = 0; i < Math.min(items.length, 2); i++) {
    const x = ML + i * (pw + gap), col = cols[i];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: py, w: pw, h: ph, fill: { color: col }, rectRadius: 0.05, shadow: shd() });
    s.addText(items[i].label || "", { x: x + 0.2, y: py + 0.12, w: pw - 0.4, h: 0.4, fontFace: FB, fontSize: sf(13, h), color: C.wh, bold: true, align: "left", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.2, y: py + 0.56, w: 1.0, h: 0.02, fill: { color: C.accLt, transparency: 50 } });
    const lines = (items[i].sublabel || "").split("\n");
    const ct = lines.map((l, j) => ({ text: l, options: { fontFace: FB, fontSize: sf(10, h), color: C.wh, breakLine: j < lines.length - 1 } }));
    s.addText(ct, { x: x + 0.2, y: py + 0.64, w: pw - 0.4, h: ph - 0.76, valign: "top", margin: 0 });
  }
}

function veStats(s, its, y, h) {
  const items = capItems(its, 5);
  const n = items.length, gap = 0.25;
  const cw = (CW - (n - 1) * gap) / n;
  const ch = Math.min(h - 0.1, 2.8);     // cap box height
  const cy = y + (h - ch) / 2;            // center vertically
  const numH = ch * 0.55;
  for (let i = 0; i < n; i++) {
    const x = ML + i * (cw + gap), col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.card }, rectRadius: 0.05, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: 0.05, fill: { color: col } });
    s.addText(items[i].label || "0", { x: x + 0.1, y: cy + 0.08, w: cw - 0.2, h: numH, fontFace: FH, fontSize: sf(34, h), color: col, bold: true, align: "center", valign: "middle", margin: 0 });
    s.addText(items[i].sublabel || "", { x: x + 0.1, y: cy + 0.08 + numH, w: cw - 0.2, h: ch - numH - 0.16, fontFace: FB, fontSize: sf(10, h), color: C.txM, align: "center", valign: "top", margin: 0 });
  }
}

function veStackedList(s, its, y, h) {
  const items = capItems(its, 8);
  const n = items.length;
  const gap = 0.12;
  const rh = Math.min((h - (n - 1) * gap) / n, 0.85);
  const totalH = n * rh + (n - 1) * gap;
  const startY = y + (h - totalH) / 2;    // center vertically
  for (let i = 0; i < n; i++) {
    const ry = startY + i * (rh + gap), col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: ML, y: ry, w: CW, h: rh, fill: { color: C.card }, rectRadius: 0.04, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x: ML, y: ry, w: 0.06, h: rh, fill: { color: col } });
    s.addText(items[i].label || "", { x: ML + 0.22, y: ry, w: 3.5, h: rh, fontFace: FB, fontSize: sf(12, h), color: col, bold: true, align: "left", valign: "middle", margin: 0 });
    if (items[i].sublabel) s.addText(items[i].sublabel, { x: ML + 3.8, y: ry, w: CW - 4.2, h: rh, fontFace: FB, fontSize: sf(10, h), color: C.txM, align: "left", valign: "middle", margin: 0 });
  }
}

function veBanner(s, items, y, h) {
  if (!items.length) return;
  const bh = Math.min(h, 2.0);
  const by = y + (h - bh) / 2;            // center vertically
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: ML, y: by, w: CW, h: bh, fill: { color: C.navy }, rectRadius: 0.05, shadow: shd() });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: by, w: 0.06, h: bh, fill: { color: C.acc } });
  const t = [{ text: items[0].label || "", options: { fontSize: sf(15, h), bold: true, color: C.wh, breakLine: !!items[0].sublabel } }];
  if (items[0].sublabel) t.push({ text: items[0].sublabel, options: { fontSize: sf(11, h), italic: true, color: C.accLt } });
  s.addText(t, { x: ML + 0.28, y: by + 0.1, w: CW - 0.56, h: bh - 0.2, fontFace: FB, align: "left", valign: "middle", margin: 0 });
}

// ── Timeline — horizontal line with milestone nodes ──
function veTimeline(s, its, y, h) {
  const items = capItems(its, 8);
  const n = items.length;
  const lineY = y + h * 0.45;
  s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.3, y: lineY, w: CW - 0.6, h: 0.03, fill: { color: C.div } });
  const step = n > 1 ? (CW - 0.6) / (n - 1) : CW;
  // Scale text width to step so adjacent items never overlap
  const tw = n > 1 ? Math.min(step - 0.15, 2.5) : 3.0;
  for (let i = 0; i < n; i++) {
    const cx = ML + 0.3 + i * step;
    const col = VC[i % VC.length];
    s.addShape(pres.shapes.RECTANGLE, { x: cx - 0.06, y: lineY - 0.045, w: 0.12, h: 0.12, fill: { color: col } });
    // Clamp text box to slide bounds
    const tx = Math.max(cx - tw / 2, ML);
    const txw = Math.min(tw, SW - 0.3 - tx);
    s.addText(items[i].label || "", { x: tx, y, w: txw, h: lineY - y - 0.08, fontFace: FB, fontSize: sf(10, h), color: col, bold: true, align: "center", valign: "bottom", margin: 0 });
    if (items[i].sublabel) s.addText(items[i].sublabel, { x: tx, y: lineY + 0.12, w: txw, h: y + h - lineY - 0.15, fontFace: FB, fontSize: sf(8, h), color: C.txM, align: "center", valign: "top", margin: 0 });
  }
}

// ── Hierarchy — root box on top, children below ──
function veHierarchy(s, its, y, h) {
  const items = capItems(its, 7);
  if (!items.length) return;
  const rootW = Math.min(4.0, CW * 0.35), rootH = Math.min(h * 0.2, 0.8);
  const rootX = SW / 2 - rootW / 2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rootX, y, w: rootW, h: rootH, fill: { color: VC[0] }, rectRadius: 0.05, shadow: shd() });
  s.addText(items[0].label || "", { x: rootX + 0.1, y, w: rootW - 0.2, h: rootH, fontFace: FB, fontSize: sf(12, h), color: C.wh, bold: true, align: "center", valign: "middle", margin: 0 });
  if (items[0].sublabel) s.addText(items[0].sublabel, { x: rootX + 0.1, y: y + rootH * 0.55, w: rootW - 0.2, h: rootH * 0.4, fontFace: FB, fontSize: sf(8, h), color: C.accLt, align: "center", valign: "middle", margin: 0 });

  const children = items.slice(1);
  if (!children.length) return;
  const n = children.length, gap = 0.25;
  const cw = Math.min((CW - (n - 1) * gap) / n, 3.5);
  const connH = Math.min(h * 0.1, 0.5);
  const childY = y + rootH + connH;
  const ch = Math.max(y + h - childY, 0.8);

  const totalW = n * cw + (n - 1) * gap;
  const startX = ML + (CW - totalW) / 2;

  for (let i = 0; i < n; i++) {
    const cx = startX + i * (cw + gap), col = VC[(i + 1) % VC.length];
    const childMidX = cx + cw / 2;
    s.addShape(pres.shapes.LINE, { x: SW / 2, y: y + rootH, w: childMidX - SW / 2, h: connH, line: { color: C.div, width: 1.2 } });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y: childY, w: cw, h: ch, fill: { color: C.card }, rectRadius: 0.05, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x: cx, y: childY, w: cw, h: 0.04, fill: { color: col } });
    s.addText(children[i].label || "", { x: cx + 0.1, y: childY + 0.08, w: cw - 0.2, h: Math.min(ch * 0.35, 0.5), fontFace: FB, fontSize: sf(11, h), color: col, bold: true, align: "center", valign: "middle", margin: 0 });
    if (children[i].sublabel) s.addText(children[i].sublabel, { x: cx + 0.1, y: childY + 0.08 + Math.min(ch * 0.35, 0.5) + 0.05, w: cw - 0.2, h: ch - Math.min(ch * 0.35, 0.5) - 0.2, fontFace: FB, fontSize: sf(9, h), color: C.txM, align: "center", valign: "top", margin: 0 });
  }
}

// ── Matrix — 2 or 3 column grid ──
function veMatrix(s, its, y, h) {
  const items = capItems(its, 9);
  const cols = items.length <= 4 ? 2 : 3;
  const rows = Math.ceil(items.length / cols);
  const gapX = 0.25, gapY = 0.15;
  const cw = (CW - (cols - 1) * gapX) / cols;
  const ch = Math.min((h - (rows - 1) * gapY) / rows, 1.3);
  const totalH = rows * ch + (rows - 1) * gapY;
  const startY = y + (h - totalH) / 2;    // center vertically
  for (let i = 0; i < items.length; i++) {
    const r = Math.floor(i / cols), c = i % cols;
    const x = ML + c * (cw + gapX), ry = startY + r * (ch + gapY);
    const col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: ry, w: cw, h: ch, fill: { color: C.card }, rectRadius: 0.05, shadow: shd() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: ry, w: 0.06, h: ch, fill: { color: col } });
    s.addText(items[i].label || "", { x: x + 0.18, y: ry + 0.08, w: cw - 0.36, h: Math.min(ch * 0.35, 0.45), fontFace: FB, fontSize: sf(11, h), color: col, bold: true, align: "left", valign: "middle", margin: 0 });
    if (items[i].sublabel) s.addText(items[i].sublabel, { x: x + 0.18, y: ry + 0.08 + Math.min(ch * 0.35, 0.45) + 0.04, w: cw - 0.36, h: ch - Math.min(ch * 0.35, 0.45) - 0.2, fontFace: FB, fontSize: sf(9, h), color: C.txM, align: "left", valign: "top", margin: 0 });
  }
}

// ── Funnel — progressively narrower bars ──
function veFunnel(s, its, y, h) {
  const items = capItems(its, 7);
  const n = items.length, gap = 0.1;
  const useH = Math.min(h, 3.5);
  const bh = Math.min((useH - (n - 1) * gap) / n, 0.8);
  const totalH = n * bh + (n - 1) * gap;
  const startY = y + (h - totalH) / 2;    // center vertically
  for (let i = 0; i < n; i++) {
    const shrink = CW * 0.08 * i;
    const bw = CW - shrink;
    const x = ML + shrink / 2;
    const by = startY + i * (bh + gap);
    const col = VC[i % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: by, w: bw, h: bh, fill: { color: col }, rectRadius: 0.05 });
    const label = items[i].label || "";
    const sub = items[i].sublabel ? " \u2014 " + items[i].sublabel : "";
    s.addText(label + sub, { x: x + 0.15, y: by, w: bw - 0.3, h: bh, fontFace: FB, fontSize: sf(11, h), color: C.wh, bold: true, align: "center", valign: "middle", margin: 0 });
  }
}

// ── Pyramid — bottom widest, top narrowest ──
function vePyramid(s, its, y, h) {
  const items = capItems(its, 7);
  const n = items.length, gap = 0.08;
  const useH = Math.min(h, 3.5);
  const bh = Math.min((useH - (n - 1) * gap) / n, 0.8);
  const totalH = n * bh + (n - 1) * gap;
  const startY = y + (h - totalH) / 2;    // center vertically
  for (let i = 0; i < n; i++) {
    const shrink = CW * 0.1 * i;
    const bw = CW - shrink;
    const x = ML + shrink / 2;
    const by = startY + i * (bh + gap);
    const level = n - 1 - i;
    const col = VC[level % VC.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: by, w: bw, h: bh, fill: { color: col }, rectRadius: 0.04 });
    s.addText(items[level] ? items[level].label || "" : "", { x: x + 0.12, y: by, w: bw - 0.24, h: bh, fontFace: FB, fontSize: sf(11, h), color: C.wh, bold: true, align: "center", valign: "middle", margin: 0 });
  }
}

// ── Before/After — two panels with arrow ──
function veBeforeAfter(s, its, y, h) {
  const items = capItems(its, 2);
  const pw = (CW - 0.9) / 2;
  const ph = Math.min(h, 2.8);            // cap panel height
  const py = y + (h - ph) / 2;            // center vertically
  const lx = ML, rx = ML + pw + 0.9;
  const lCol = (items[0] && items[0].tone === "positive") ? C.grn : C.txL;
  const rCol = (items[1] && items[1].tone === "positive") ? C.grn : (items[1] && items[1].tone === "negative") ? C.txL : C.grn;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: lx, y: py, w: pw, h: ph, fill: { color: lCol }, rectRadius: 0.06, shadow: shd() });
  if (items[0]) {
    s.addText(items[0].label || "Before", { x: lx + 0.18, y: py + 0.12, w: pw - 0.36, h: 0.4, fontFace: FB, fontSize: sf(13, h), color: C.wh, bold: true, align: "left", valign: "middle", margin: 0 });
    if (items[0].sublabel) s.addText(items[0].sublabel, { x: lx + 0.18, y: py + 0.58, w: pw - 0.36, h: ph - 0.7, fontFace: FB, fontSize: sf(10, h), color: C.wh, align: "left", valign: "top", margin: 0 });
  }
  s.addText("\u27A1", { x: ML + pw + 0.15, y: py + ph / 2 - 0.22, w: 0.6, h: 0.44, fontFace: FB, fontSize: 26, color: C.acc, align: "center", valign: "middle", margin: 0 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y: py, w: pw, h: ph, fill: { color: rCol }, rectRadius: 0.06, shadow: shd() });
  if (items[1]) {
    s.addText(items[1].label || "After", { x: rx + 0.18, y: py + 0.12, w: pw - 0.36, h: 0.4, fontFace: FB, fontSize: sf(13, h), color: C.wh, bold: true, align: "left", valign: "middle", margin: 0 });
    if (items[1].sublabel) s.addText(items[1].sublabel, { x: rx + 0.18, y: py + 0.58, w: pw - 0.36, h: ph - 0.7, fontFace: FB, fontSize: sf(10, h), color: C.wh, align: "left", valign: "top", margin: 0 });
  }
}

// ══════════════════════════════════════════════
//  VISUAL ELEMENTS — chart-based (PptxGenJS addChart)
// ══════════════════════════════════════════════

function veBarChart(s, items, y, h) {
  const labels = items.map(it => it.sublabel || it.label || "");
  const values = items.map(extractValue);
  s.addChart("bar", [{ name: "Data", labels, values }], {
    x: ML + 0.5, y, w: CW - 1.0, h,
    barDir: "col", barGrouping: "clustered", barGapWidthPct: 80,
    chartColors: CC.slice(0, items.length),
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 9, dataLabelColor: C.txM,
    catAxisLabelFontSize: 9, catAxisLabelColor: C.txM, catAxisLineColor: C.div,
    valAxisHidden: true, valGridLine: { color: C.div, style: "dash", size: 0.3 },
    chartArea: { fill: { color: C.bg }, border: { color: C.div, pt: 0.5 }, roundedCorners: true },
    plotArea: { fill: { color: C.bg } },
    showLegend: false,
  });
}

function vePieChart(s, items, y, h) {
  const labels = items.map(it => it.sublabel || it.label || "");
  const values = items.map(extractValue);
  const cw = Math.min(CW - 2.0, h * 1.5);
  s.addChart("pie", [{ name: "Data", labels, values }], {
    x: ML + (CW - cw) / 2, y, w: cw, h,
    chartColors: CC.slice(0, items.length),
    showPercent: true, showLabel: true,
    dataLabelPosition: "outEnd", dataLabelFontSize: 9, dataLabelColor: C.txM,
    chartArea: { fill: { color: C.bg }, border: { color: C.div, pt: 0.5 }, roundedCorners: true },
    dataNoEffects: true,
    showLegend: false,
  });
}

function veDoughnutChart(s, items, y, h) {
  const labels = items.map(it => it.sublabel || it.label || "");
  const values = items.map(extractValue);
  const cw = Math.min(CW - 2.0, h * 1.5);
  s.addChart("doughnut", [{ name: "Data", labels, values }], {
    x: ML + (CW - cw) / 2, y, w: cw, h,
    chartColors: CC.slice(0, items.length),
    holeSize: 55, showPercent: true,
    dataLabelPosition: "outEnd", dataLabelFontSize: 9, dataLabelColor: C.txM,
    chartArea: { fill: { color: C.bg }, border: { color: C.div, pt: 0.5 }, roundedCorners: true },
    dataNoEffects: true,
    showLegend: true, legendPos: "r", legendFontSize: 9, legendColor: C.txM,
  });
}

function veRadarChart(s, items, y, h) {
  const labels = items.map(it => it.sublabel || it.label || "");
  const values = items.map(extractValue);
  const cw = Math.min(CW - 2.0, h * 1.5);
  s.addChart("radar", [{ name: "Data", labels, values }], {
    x: ML + (CW - cw) / 2, y, w: cw, h,
    chartColors: [CC[0]],
    radarStyle: "marker",
    catAxisLabelFontSize: 8, catAxisLabelColor: C.txM,
    chartArea: { fill: { color: C.bg }, border: { color: C.div, pt: 0.5 }, roundedCorners: true },
    plotArea: { fill: { color: C.bg } },
    showLegend: false,
  });
}

function veLineChart(s, items, y, h) {
  const labels = items.map(it => it.sublabel || it.label || "");
  const values = items.map(extractValue);
  s.addChart("line", [{ name: "Trend", labels, values }], {
    x: ML + 0.5, y, w: CW - 1.0, h,
    chartColors: [CC[0]],
    lineSize: 2.5, lineSmooth: true, lineDataSymbol: "circle", lineDataSymbolSize: 8,
    showValue: true, dataLabelPosition: "t", dataLabelFontSize: 9, dataLabelColor: C.txM,
    catAxisLabelFontSize: 9, catAxisLabelColor: C.txM, catAxisLineColor: C.div,
    valAxisHidden: true, valGridLine: { color: C.div, style: "dash", size: 0.3 },
    chartArea: { fill: { color: C.bg }, border: { color: C.div, pt: 0.5 }, roundedCorners: true },
    plotArea: { fill: { color: C.bg } },
    showLegend: false,
  });
}

// ══════════════════════════════════════════════
//  VE MAP — 19 types (14 shape + 5 chart)
// ══════════════════════════════════════════════

const VE = {
  // 8 original shape-based
  process_flow: veProcessFlow, callout_cards: veCalloutCards, comparison: veComparison,
  cycle: veCycle, split_panel: veSplitPanel, stats_callout: veStats,
  stacked_list: veStackedList, banner_quote: veBanner,
  // 6 new shape-based
  timeline: veTimeline, hierarchy: veHierarchy, matrix: veMatrix,
  funnel: veFunnel, pyramid: vePyramid, before_after: veBeforeAfter,
  // 5 chart-based
  bar_chart: veBarChart, pie_chart: vePieChart, doughnut_chart: veDoughnutChart,
  radar_chart: veRadarChart, line_chart: veLineChart,
  // Aliases for backward compatibility
  equation_highlight: veBanner, icon_row: veCalloutCards, progress_bar: veProcessFlow,
  radial: veCycle,
};

// ══════════════════════════════════════════════
//  ASSEMBLE
// ══════════════════════════════════════════════

// workspace patch: ARCDECK_NO_BOOKENDS=true drops the title and Thank-You slides (course rule: three pages)
const BOOKENDS = (process.env.ARCDECK_NO_BOOKENDS || "false") !== "true";
if (BOOKENDS) mkTitle();

// Section dividers: opt-in via env (default: off to keep slide count tight)
const DIVIDERS = (process.env.ARCDECK_DIVIDERS || "false") === "true";
function fmtSec(s) { return s.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()); }

let curSec = "";
for (const sd of allSlides) {
  // Skip JSON title slide — mkTitle() already renders from metadata
  if (sd.template_id === "T7_Title") continue;

  if (DIVIDERS && sd.section !== curSec && sd.section !== "title") {
    mkDivider(fmtSec(sd.section));
  }
  curSec = sd.section;

  // Route by template_id (primary) then section name (fallback)
  if (sd.template_id === "T8_Conclusion" || /conclus/i.test(sd.section)) {
    mkConclusion(sd);
  } else if (sd.template_id === "_FIGPAGE") {
    mkFigPage(sd);
  } else if (sd.template_id === "T1_TextOnly") {
    mkTextSlide(sd);
  } else {
    mkImgSlide(sd);
  }
}
if (BOOKENDS) mkThankYou();

const out = path.join(WS, "output.pptx");
pres.writeFile({ fileName: out }).then(() => {
  const sz = fs.statSync(out);
  console.log(`\n\u2705 ${out}`);
  console.log(`   Slides: ${pres.slides.length}  |  Size: ${Math.round(sz.size / 1024)}K`);
  console.log(`   Template: ${T.name}`);
}).catch(e => { console.error(e); process.exit(1); });
