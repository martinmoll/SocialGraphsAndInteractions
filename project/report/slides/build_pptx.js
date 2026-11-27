// Editable PowerPoint twin of report/slides/slides.tex (same text, numbers, figures and layout style).
// Run in a scratch folder holding this script, pptxgenjs (npm install pptxgenjs), figures/net_*.png and the crops
// made by pptx_crops.py:  python pptx_crops.py <report/slides/figures> . ; node build_pptx.js <out.pptx>
// Edit the text in slides.tex first; this file repeats it and must be kept in step by hand.
// Style (27 Nov): title band + subtitle; plain bold headings over figures; boxes with a purple header band and
// bullets with bold lead-ins; label tiles; tinted number tiles; Checked/Sources lines at the foot.
const pptxgen = require("pptxgenjs");
const path = require("path");
const OUT = process.argv[2];
const P = (f) => path.join(__dirname, f);

const PURPLE = "7D3C98", BAND = "F3EEF7", INK = "222222", MUTE = "666666", REP = "D62728", DEM = "1F77B4", WHITE = "FFFFFF";
const FONT = "Arial";
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.title = "Two maps of Congress";
pres.author = "Anas Mir, Martin Mollenhus, Diego A. Mijares";

const t = (text, o = {}) => ({ text, options: { fontFace: FONT, color: INK, ...o } });
const tb = (s, runs, o) => s.addText(runs, { margin: 0, isTextBox: true, fontFace: FONT, color: INK, ...o });

function frame(s, n, title, subtitle, notes) {
  s.background = { color: WHITE };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.53, fill: { color: PURPLE }, line: { color: PURPLE }, objectName: "Headline band" });
  tb(s, `${n}   ${title}`, { x: 0.3, y: 0, w: 9.4, h: 0.53, fontSize: 19, bold: true, color: WHITE, valign: "middle", objectName: "Title" });
  tb(s, subtitle, { x: 0.3, y: 0.64, w: 9.4, h: 0.26, fontSize: 11, valign: "middle", objectName: "Subtitle" });
  tb(s, "Two maps of Congress | Anas Mir, Martin Møllenhus, Diego A. Mijares | 02805, DTU", { x: 0.3, y: 5.4, w: 6, h: 0.18, fontSize: 7, color: MUTE });
  tb(s, "119th US House, Jan 2025–Nov 2026", { x: 6.7, y: 5.4, w: 3, h: 0.18, fontSize: 7, color: MUTE, align: "right" });
  s.addNotes(notes);
}
const heading = (s, x, y, w, text) => tb(s, text, { x, y, w, h: 0.24, fontSize: 11, bold: true, valign: "top" });
// Box with a purple header band. Returns the y where the body starts.
function bandbox(s, x, y, w, h, title) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.04, fill: { color: WHITE }, line: { color: PURPLE, width: 0.75 }, objectName: `Box: ${title}` });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.22, fill: { color: PURPLE }, line: { color: PURPLE } });
  tb(s, title, { x, y, w, h: 0.22, fontSize: 8.5, bold: true, color: WHITE, align: "center", valign: "middle" });
  return y + 0.3;
}
// Bullets with bold lead-ins: items = [[lead, rest-runs-or-string], ...]
function bullets(s, x, y, w, h, items, size = 8.5) {
  const runs = [];
  items.forEach(([lead, rest], i) => {
    const last = i === items.length - 1;
    runs.push(t(lead + " ", { bold: true, fontSize: size, bullet: { indent: 9 }, paraSpaceAfter: 2 }));
    const tail = typeof rest === "string" ? [t(rest, { fontSize: size })] : rest.map(r => ({ text: r.text, options: { fontFace: FONT, color: INK, fontSize: size, ...r.options } }));
    if (!last) tail[tail.length - 1].options.breakLine = true;
    runs.push(...tail);
  });
  tb(s, runs, { x, y, w, h, valign: "top" });
}
// Tinted number tile.
// Low number tile: number left, sentence beside it, both centred (slide 1, as \htile in slides.tex).
function htile(s, x, y, w, h, num, color, label) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: BAND }, line: { color: BAND } });
  tb(s, num, { x: x + 0.15, y, w: 1.15, h, fontSize: 20, bold: true, color, align: "right", valign: "middle" });
  tb(s, label, { x: x + 1.4, y, w: w - 1.5, h, fontSize: 8, valign: "middle" });
}
function tile(s, x, y, w, h, numRuns, label, size = 24) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: BAND }, line: { color: BAND } });
  const runs = (typeof numRuns === "string" ? [t(numRuns, {})] : numRuns).map(r => ({ text: r.text, options: { fontFace: FONT, color: INK, bold: true, fontSize: size, ...r.options } }));
  tb(s, runs, { x, y: y + 0.03, w, h: h * 0.55, align: "center", valign: "bottom" });
  tb(s, label, { x: x + 0.05, y: y + h * 0.58, w: w - 0.1, h: h * 0.4, fontSize: 8, align: "center", valign: "top" });
}
// Label tile: purple block + white box with detail.
function labeltile(s, x, y, w, h, label, main, sub) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.9, h, fill: { color: PURPLE }, line: { color: PURPLE } });
  tb(s, label, { x, y, w: 0.9, h, fontSize: 8.5, bold: true, color: WHITE, align: "center", valign: "middle" });
  s.addShape(pres.shapes.RECTANGLE, { x: x + 0.9, y, w: w - 0.9, h, fill: { color: WHITE }, line: { color: PURPLE, width: 0.75 } });
  tb(s, [t(main, { bold: true, fontSize: 8.5, breakLine: true }), t(sub, { fontSize: 8, color: MUTE })], { x: x + 0.98, y, w: w - 1.02, h, valign: "middle" });
}
const foot = (s, checked, sources) => tb(s, [
  t("Checked: ", { bold: true, color: MUTE, fontSize: 7 }), t(checked, { color: MUTE, fontSize: 7, breakLine: true }),
  t("Sources: ", { bold: true, color: MUTE, fontSize: 7 }), t(sources, { color: MUTE, fontSize: 7 }),
], { x: 0.3, y: 4.97, w: 9.4, h: 0.38, valign: "top" });

// ------------------------------------------------------------------ 1
{
  const s = pres.addSlide();
  frame(s, 1, "They vote in two camps. Do they also name each other in two camps?",
    [t("No: drawn from the same 450 members, the House is "), t("less divided in whom it names than in whom it works with", { bold: true })],
    "Martin, about 60 s. See report/slides/STORY.md, slide 1.");
  const L = 0.3, LW = 2.75;
  let by = bandbox(s, L, 1.0, LW, 1.62, "The puzzle");
  bullets(s, L + 0.08, by, LW - 0.14, 1.3, [
    ["Two camps:", "members vote apart and talk apart."],
    ["So expect attacks:", "when one names a colleague of the other party on the floor."],
    ["Our question:", [{ text: "is the House as divided in " }, { text: "whom members name", options: { italic: true } }, { text: " as in " }, { text: "whom they work with", options: { italic: true } }, { text: "?" }]],
    ["Our approach:", "draw the same members twice, as two networks, and compare them."],
  ], 8);
  heading(s, L, 2.75, LW, "Same 450 members, three records");
  labeltile(s, L, 3.05, LW, 0.52, "Working map", "A cosponsors B's bill", "46,513 ties, govinfo bill data");
  labeltile(s, L, 3.66, LW, 0.52, "Floor map", "A names B in a floor speech", "17,824 speeches, Congressional Record");
  labeltile(s, L, 4.27, LW, 0.52, "At home", "A names B in a press release", "55,023 releases from house.gov");

  const X1 = 3.25, X2 = 6.55, W = 3.15;
  heading(s, X1, 1.0, W, "Floor: who names whom");
  heading(s, X2, 1.0, W, "Working: who cosponsors with whom");
  s.addImage({ path: P("net_floor.png"), x: X1, y: 1.27, w: W, h: W / 2.17, altText: "Floor map network, Bacon ringed" });
  s.addImage({ path: P("net_work.png"), x: X2, y: 1.27, w: W, h: W / 2.17, altText: "Working map network, Bacon ringed" });
  htile(s, X1, 2.76, W, 0.45, "38.7%", PURPLE, "of ties cross the aisle");
  htile(s, X2, 2.76, W, 0.45, "28.6%", INK, "cross at the same number of ties (mean of 200 draws)");
  tb(s, [t("● ", { color: REP }), t("Republican   "), t("● ", { color: DEM }), t("Democrat   "), t("— ", { color: PURPLE, bold: true }), t("cross-party tie   ○ "),
    t("Don Bacon", { bold: true }), t(" (R, NE)    Working map: one draw, 29.3% cross")], { x: X1, y: 3.25, w: 6.45, h: 0.18, fontSize: 7 });
  by = bandbox(s, X1, 3.47, W, 1.32, "Not chance, not thinning");
  bullets(s, X1 + 0.08, by, W - 0.14, 1.0, [
    ["None close:", "no random draw of working ties reaches the floor map."],
    ["Closest partners:", [{ text: "only " }, { text: "12.8%", options: { bold: true } }, { text: " of the strongest working ties cross." }]],
    ["Far from random:", [{ text: "rewired ties cross ≈" }, { text: "50%", options: { bold: true } }, { text: "." }]],
  ], 8);
  s.addImage({ path: P("fig1_C.png"), x: X2, y: 3.45, w: 2.1, h: 1.3, altText: "Cross-party share of ties in each map" });
  foot(s, "name matcher right in 98 of 100 hand-read mentions; the result holds with or without procedural yields (“I yield to…”).",
    "Congressional Record and BILLSTATUS bulk data (govinfo.gov), Jan 2025–Nov 2026; member lists from Voteview.");
}

// ------------------------------------------------------------------ 2
{
  const s = pres.addSlide();
  frame(s, 2, "You would expect attacks. Most of the time, it's a thank-you",
    [t("Naming across the aisle is "), t("committee work made public", { bold: true }), t(": mostly credit, rarely argument")],
    "Diego, about 60 s. See report/slides/STORY.md, slide 2.");
  const X = [0.3, 3.45, 6.6], W = 3.1, BY = 2.85, BH = 1.95;
  heading(s, X[0], 1.0, W, "What does a cross-party mention say?");
  heading(s, X[1], 1.0, W, "How much is just procedure?");
  heading(s, X[2], 1.0, W, "Which groups does each map form?");
  s.addImage({ path: P("fig2.png"), x: X[0], y: 1.3, w: 2.85, h: 1.44, altText: "Codes of 100 hand-labelled floor mentions" });
  s.addImage({ path: P("fig1_D.png"), x: X[1], y: 1.3, w: 2.3, h: 1.44, altText: "Party modularity against the nulls" });

  let by = bandbox(s, X[0], BY, W, BH, "Mostly credit, rarely attack");
  tb(s, "69%", { x: X[0], y: by - 0.04, w: W / 2, h: 0.38, fontSize: 24, bold: true, color: PURPLE, align: "center", valign: "bottom" });
  tb(s, "7%", { x: X[0] + W / 2, y: by - 0.04, w: W / 2, h: 0.38, fontSize: 24, bold: true, align: "center", valign: "bottom" });
  tb(s, "thanks & credit", { x: X[0], y: by + 0.34, w: W / 2, h: 0.14, fontSize: 8, align: "center" });
  tb(s, "disagreement", { x: X[0] + W / 2, y: by + 0.34, w: W / 2, h: 0.14, fontSize: 8, align: "center" });
  bullets(s, X[0] + 0.08, by + 0.55, W - 0.14, 1.05, [
    ["Method:", "100 random floor mentions, each coded by hand."],
    ["Example:", [{ text: "“I also thank my friend and subcommittee ranking member, Mr. Ro Khanna, for his collaboration this year.” ", options: { italic: true } },
      { text: "Bacon (", options: { color: MUTE } }, { text: "R", options: { color: REP } }, { text: ") on Khanna (", options: { color: MUTE } }, { text: "D", options: { color: DEM } }, { text: "), 21 Jul 2026.", options: { color: MUTE } }]],
    ["Procedure:", "handing over debate time never crosses the aisle."],
  ], 7.5);

  by = bandbox(s, X[1], BY, W, BH, "About two thirds is how debates run");
  tb(s, "≈ 2/3", { x: X[1], y: by - 0.04, w: W, h: 0.38, fontSize: 24, bold: true, align: "center", valign: "bottom" });
  tb(s, "of the floor map's division comes from debate procedure", { x: X[1], y: by + 0.34, w: W, h: 0.14, fontSize: 8, align: "center" });
  bullets(s, X[1] + 0.08, by + 0.55, W - 0.14, 1.05, [
    ["Shuffle within debates:", "each debate brings both parties' managers; shuffling who is named inside each debate drops party modularity from 0.112 to 0.074."],
    ["The last third is real:", "members name their own side more than in any of 200 shuffles."],
    ["Not states:", "state delegations explain almost none."],
  ], 7.5);

  by = bandbox(s, X[2], 1.3, W, BY + BH - 1.3, "Organised by committee, not party");
  bullets(s, X[2] + 0.08, by, W - 0.14, 0.5, [
    ["Working map:", [{ text: "Louvain finds " }, { text: "2", options: { bold: true } }, { text: " communities, the two parties." }]],
    ["Floor map:", [{ text: "8", options: { bold: true } }, { text: " communities, each bipartisan." }]],
  ], 8);
  tile(s, X[2] + 0.1, by + 0.55, W / 2 - 0.15, 0.7, "0.83", "overlap with party, working (NMI)");
  tile(s, X[2] + W / 2 + 0.05, by + 0.55, W / 2 - 0.15, 0.7, [{ text: "0.03", options: { color: PURPLE } }], "overlap with party, floor (NMI)");
  bullets(s, X[2] + 0.08, by + 1.35, W - 0.14, 0.6, [
    ["Committees:", "seven floor communities gather around one committee (Appropriations, Ways and Means, …); the eighth is the party leaders."],
  ], 8);
  tile(s, X[2] + 0.1, by + 2.05, W / 2 - 0.15, 0.7, [{ text: "44%", options: { color: PURPLE } }], "of floor ties join committee colleagues");
  tile(s, X[2] + W / 2 + 0.05, by + 2.05, W / 2 - 0.15, 0.7, "17%", "if ties were placed at random");
  foot(s, "two human coders agree 82% (κ = 0.64), a blind AI coder 88%; a text classifier did not beat the baseline, so only hand codes are reported.",
    "Congressional Record (govinfo.gov); 100 hand-labelled mentions; committee assignments, Nov 2026.");
}

// ------------------------------------------------------------------ 3
{
  const s = pres.addSlide();
  frame(s, 3, "At home, members in close races name the other party most",
    [t("How divided Congress looks "), t("depends on the record you read", { bold: true }), t("; a name, unlike the word “bipartisan”, can be checked")],
    "Anas, about 60 s. See report/slides/STORY.md, slide 3.");
  const X = [0.3, 5.1], W = 4.6, BY = 3.2, BH = 1.6;
  heading(s, X[0], 1.0, W, "Press releases naming the other party, by how safe the seat is");
  heading(s, X[1], 1.0, W, "The home map: exposed members are the hubs");
  s.addImage({ path: P("lean.png"), x: X[0], y: 1.28, w: 3.3, h: 1.83, altText: "Share of releases naming the other party, by district lean" });
  const IW = 1.83 * 1.361, IH = 1.83, IX = X[1], IY = 1.28;
  s.addImage({ path: P("home.png"), x: IX, y: IY, w: IW, h: IH, altText: "Who names whom in press releases" });
  // Bacon's dot is at (0.4554, 0.4625 from the top) of home.png, as in slides.tex.
  const bx = IX + 0.4554 * IW, by0 = IY + 0.4625 * IH;
  s.addShape(pres.shapes.OVAL, { x: bx - 0.09, y: by0 - 0.09, w: 0.18, h: 0.18, line: { color: "000000", width: 2 }, objectName: "Bacon ring" });
  const CX = 7.75, CY = 1.3, CW = 1.9, CH = 1.0;
  s.addShape(pres.shapes.LINE, { x: bx + 0.08, y: CY + 0.5, w: CX - bx - 0.08, h: by0 - CY - 0.5 - 0.04, flipH: true, line: { color: "000000", width: 1 }, objectName: "Bacon pointer" });
  const cy = bandbox(s, CX, CY, CW, CH, "Don Bacon (R, NE)");
  tb(s, [t("1 in 3", { bold: true, fontSize: 18, color: PURPLE, breakLine: true }), t("releases names a Democrat", { fontSize: 8, breakLine: true }), t("53 of 163; district leans D+3", { fontSize: 7, color: MUTE })],
    { x: CX, y: cy - 0.06, w: CW, h: CH - 0.28, align: "center", valign: "middle", objectName: "Bacon callout text" });

  let by = bandbox(s, X[0], BY, W, BH, "Exposed seats name the other party more");
  const pair = (x, a, b, c, lab) => {
    tb(s, [t(a, { color: c, bold: true, fontSize: 20 }), t(" vs ", { fontSize: 10, bold: true }), t(b, { bold: true, fontSize: 20 })], { x, y: by - 0.04, w: W / 2, h: 0.36, align: "center", valign: "bottom" });
    tb(s, lab, { x, y: by + 0.32, w: W / 2, h: 0.14, fontSize: 8, align: "center" });
  };
  pair(X[0], "13.3%", "9.2%", REP, "Republicans, exposed vs safe");
  pair(X[0] + W / 2, "11.6%", "9.0%", DEM, "Democrats, exposed vs safe");
  bullets(s, X[0] + 0.08, by + 0.52, W - 0.14, 0.75, [
    ["Exposed:", "district leans to own party by ≤5 points; p = 0.004 in each party, survives every check fixed in advance."],
    ["Closest seats:", [{ text: "about " }, { text: "1 release in 5", options: { bold: true } }, { text: " names the other party (Republicans)." }]],
  ], 8);

  by = bandbox(s, X[1], BY, W, BH, "Exposed members are the bridges");
  const tw = (W - 0.4) / 3;
  tile(s, X[1] + 0.1, by + 0.02, tw, 1.15, [{ text: "22%" }, { text: " → ", options: { fontSize: 11 } }, { text: "1/3", options: { color: PURPLE } }], "of members, of cross-party ties", 20);
  tile(s, X[1] + 0.2 + tw, by + 0.02, tw, 1.15, [{ text: "46 of 60", options: { color: PURPLE } }], "names read: a partner or praise (1 criticised)", 20);
  tile(s, X[1] + 0.3 + 2 * tw, by + 0.02, tw, 1.15, [{ text: "64%" }, { text: " vs ", options: { fontSize: 10 } }, { text: "9%" }], "“bipartisan” releases vs others name a partner", 20);
  foot(s, "exposed members are also their party's moderates; comparing members of similar ideology leaves little of the gap, so seat and moderation cannot be separated here. One Congress, one chamber.",
    "55,023 press releases from house.gov (3 Jan 2025–20 Nov 2026); Cook PVI 2025; names read by three blind AI readers, disagreements by one author.");
}

pres.writeFile({ fileName: OUT }).then(() => console.log("written", OUT));
