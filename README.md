# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/7tomars/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/7tomars/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**The World in One Image** — a one-page newspaper front page that sums up the
world's news of **Sunday 22 November 2026** in a single 1024×1024 PNG.

`main.py` is a pure Python 3 program (standard library only, no network, no
external assets). It draws the page pixel by pixel into an RGB framebuffer
with a built-in 5×7 bitmap font and writes it out with a hand-rolled PNG
encoder (zlib + struct). The render is fully deterministic: every run
produces byte-identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png`. Without `MAKEFUN_OUTPUT_DIR` the program writes
`/output/entry.png` (creating `/output` if needed), falling back to
`./entry.png`.

## The eight stories

1. **COP31 collapses in Antalya** — the final climate deal names no fossil
   fuels and the EU rejects it. *(Rapporteur; The Curtain)*
2. **Indonesia factory fire: 3 dead, 36 missing** — rescuers search the ruins
   of a candy factory in Banten, Java. *(Reuters; AFP)*
3. **Nigeria funeral boat toll rises to 24** — the emergency agency confirms
   the toll after the Bayelsa capsize. *(Reuters; QNC News)*
4. **Bahrain: Iranian attack hits civilian site** — an industrial facility is
   struck and two people are injured, says Manama. *(Reuters; AFP)*
5. **S. Korea education minister quits** — resigns over the AI-cheating chaos
   around the entrance exam. *(Korea JoongAng Daily; Seoul Economic Daily;
   Aju Press)*
6. **Russian cargo ship still burning off Finland** — the Sparta II is ablaze
   after a drone strike and its crew is evacuated. *(Reuters; TBS News)*
7. **Verstappen wins Las Vegas thriller** — beats Norris by 0.6s in a race of
   35 lead changes. *(Reuters; AP)*
8. **Italy airport strikes hit Milan and Venice** — controllers and airport
   staff walk out on Sunday. *(PaxSentinel; VolClaim)*

---

<sub>Entered on [make.fun](https://make.fun/?ref=xs6hh474&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
