# Anas_Claude: pilots behind the ratings and proposals

Written 12 November 2026 by Anas with Claude (AI-assisted). The overview these scripts support is
`../research_questions_rating_and_proposals.md`. Nothing here changes anyone else's files.

**Status: exploratory.** One run each, definitions chosen on the day. `pilot_counts.py`,
`pilot_together.py`, `pilot_symbolic.py` and `pilot_names.py` were run a second time from this layout and
printed the same numbers. That confirms the scripts are deterministic, not that the findings are robust.

## Scripts

Run from the `project/` folder. Each takes the data folder as its argument and reads only `data/processed/`.

```bash
python Anas_Claude/pilot/pilot_counts.py data/processed
```

| Script | Question it tests | Section in the overview |
|---|---|---|
| `pilot/pilot_counts.py` | Do Republicans sign more Democratic bills over time, or fewer Republican ones? | 4.1 |
| `pilot/pilot_together.py` | Does a member's change in Trump mentions or cross-party share follow their seat, their ideology, or the people they work with? | 4.2, 4.3 |
| `pilot/pilot_symbolic.py` | How much of cross-party cosponsorship sits on symbolic bills? | 4.4 |
| `pilot/pilot_bills.py` | Do bill titles, scored with floor vocabulary, show what Republicans cross the aisle for? | 5 |
| `pilot/pilot_names.py` | Who names whom in floor speeches, and do named pairs share cosponsorship ties? Prints 25 matches to read | 6 |
| `pilot/press_pull.py` | Do Republicans' press releases name colleagues, and of which party? | 6 |

`press_pull.py` takes two arguments, the data folder and an output file, and makes about 320 web requests to
eight members' house.gov sites with pauses:

```bash
python Anas_Claude/pilot/press_pull.py data/processed Anas_Claude/pilot/press_sample_new.json
```

`pilot/press_sample_2026-11-12.json` is what it collected on 12 November 2026: 280 releases from seven
Republicans, with the names matched in each and the first 200 characters of the text. The sites change, so a
rerun will not return the same releases.

## Known limits

- Name matching uses surnames that are unique in the House. Members who share a surname are skipped.
- The press release matcher has not been read for false hits.
- `pilot_together.py` uses the unfiltered Republican cosponsorship network, not Martin's backbone blocs.
- Environment: Anaconda `base`, the same as `../readme.md`, section 4.
