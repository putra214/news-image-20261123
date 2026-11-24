[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/putra214/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/putra214/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Day — Monday 23 November 2026

One image that sums up the world's news of Monday 23 November 2026, for
make.fun's "Sum up 23 November's world news in one image" bounty.

## The image

A one-page newspaper front page, drawn entirely in code
(`generate_poster.py`, Python + Pillow): a masthead dated
**MONDAY, 23 NOVEMBER 2026**, a strip of six big numbers from the day's
news (15+ killed in the Kyiv strikes, 24+ dead in the factory fire, 30%
Nvidia surge, Bitcoin's $55,100 low, 8 years to Mercury orbit, 258
Democrat House seats), a lead story on COP31 ending in Antalya with no
deal — illustrated by a dotted world map with numbered pins
("WHERE IT HAPPENED") matching the lead and grid stories — six more main
stories (the sea-drone sinking of the Russian corvette Merkury off Libya,
the strikes on the Kyiv region, Jensen Huang's return as Nvidia chief,
Bitcoin's slide in the AI sell-off, the candy-factory fire in Indonesia,
BepiColombo reaching Mercury), twenty-two briefs from across six regions
(including the Belgian national strike, the US sanctions on Iran's shadow
banking, the NHS AI breast-screening trial, and the Democrats' 258 House
seats), and a DATE CHECK box listing the big non-23-November stories that
were deliberately left out. Story kickers are coloured by region so the
spread of the news is visible at a glance.

Every event in the main sections happened, or was first reported, on
23 November 2026. Stories from other days are not in the main sections:
the DATE CHECK box lists four of them with their real dates — the Chapo
Isidro arrest in Mexico (21 Nov), the Wall Street sell-off (20 Nov), the
Shenzhen declaration (19 Nov), the ICJ Rohingya ruling (19 Nov) — so
nothing is presented as the day's news that was not.

## How it is built

- `generate_poster.py` draws `entry.png` (1024x1024, PNG) with flat
  vector-style art and real text, so every letter stays sharp.
- `main.py` (Python 3.13, standard library only) copies `entry.png` to the
  output directory. It runs with no network and writes the same bytes on
  every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB
```
