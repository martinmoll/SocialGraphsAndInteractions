// Baseline check for the 115th Congress (2017-18, Trump's first term, also a Democratic midterm wave).
// govinfo is not reachable from every machine's proxy, so this was run in a browser console
// on a govinfo.gov page (open https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr first). 11 Nov 2026.
// Deterministic sample: every 6th House bill (1,233 bills, 19,356 non-withdrawn cosponsorships).
// For the paper, replace this with the full download via scripts/02_fetch_bills.py pointed at congress 115.
const L = await fetch('/bulkdata/json/BILLSTATUS/115/hr', {headers: {Accept: 'application/json'}}).then(r => r.json());
let files = L.files.filter(f => f.fileExtension === 'xml').map(f => f.link.replace('https://www.govinfo.gov', ''));
files = files.sort().filter((_, i) => i % 6 === 0);
const rows = [];
async function one(u) {
  const d = new DOMParser().parseFromString(await fetch(u).then(r => r.text()), 'text/xml');
  const sp = d.querySelector('sponsors > item party')?.textContent;
  for (const it of d.querySelectorAll('cosponsors > item')) {
    if (it.querySelector('sponsorshipWithdrawnDate')) continue;
    rows.push([sp, it.querySelector('party')?.textContent, it.querySelector('sponsorshipDate')?.textContent]);
  }
}
for (let i = 0; i < files.length; i += 20) await Promise.all(files.slice(i, i + 20).map(one));
const agg = {};
for (const [s, p, dt] of rows) {
  if (!dt) continue;
  const k = dt.slice(0, 4) + 'Q' + (Math.floor((+dt.slice(5, 7) - 1) / 3) + 1);
  agg[k] = agg[k] || {Rn: 0, Rx: 0, Dn: 0, Dx: 0};
  if (p === 'R') { agg[k].Rn++; if (s === 'D') agg[k].Rx++; }
  if (p === 'D') { agg[k].Dn++; if (s === 'R') agg[k].Dx++; }
}
Object.fromEntries(Object.keys(agg).sort().map(k => [k, [agg[k].Rn, (agg[k].Rx / agg[k].Rn).toFixed(3), agg[k].Dn, (agg[k].Dx / agg[k].Dn).toFixed(3)]]));
// Result 11 Nov 2026 (R n, R cross share, D n, D cross share):
// 2017Q1 1468 0.080 1991 0.261 | 2017Q2 1397 0.167 2456 0.317 | 2017Q3 725 0.124 1415 0.304 | 2017Q4 1158 0.109 1794 0.328
// 2018Q1  997 0.126 1620 0.328 | 2018Q2  691 0.175 1300 0.263 | 2018Q3 563 0.171 1249 0.199 | 2018Q4  115 0.374  412 0.223
