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
news (Nvidia shares +31.5%, 404 flights axed in Belgium, 24 dead in the
factory fire, 258 Democrat House seats, 60 banks off SWIFT, Bitcoin's
$61,271 close), three lead stories — Jensen Huang back as Nvidia chief,
Belgium grounded by a national strike, and NATO's emergency meeting after
Russian missiles fell in Poland — each with its own illustration, a dotted
world map with numbered pins ("WHERE IT HAPPENED") matching the leads and
grid stories, a UTC timeline of the day, six more main stories (Ukraine's
claim that its sea drones sank the Russian corvette Merkury off Libya,
Bitcoin's rebound above $61,000, the EU's proposed 22nd sanctions package,
the US sanctions on Iran's shadow banking, the Dymer death toll rising to
11, the factory fire in Indonesia), twenty-six briefs from across seven
regions (including the NHS AI breast-screening trial, the Acropolis
Museum reopening, Finland summoning Russia's envoy, the UK hosting the
2035 Women's World Cup, and the UK recognising the Rohingya genocide),
and a DATE CHECK box listing the big non-23-November stories that were
deliberately left out. Story kickers are coloured by region so the
spread of the news is visible at a glance.

Every event in the main sections happened, or was first reported, on
23 November 2026. Stories from other days are not in the main sections:
the DATE CHECK box lists nine of them with their real dates — COP31
ending without a deal (22 Nov), BepiColombo reaching Mercury (21 Nov),
Bitcoin's $55,100 low (21 Nov), the Dymer strike (22 Nov), the Kryvyi
Rih missile (20 Nov), the Chapo Isidro arrest (20 Nov), the Wall Street
sell-off (20 Nov), the Shenzhen declaration (19 Nov), and the ICJ
Rohingya ruling (19 Nov) — so nothing is presented as the day's news
that was not. (v2 rebuild: v1's lead stories were dated wrong — COP31,
BepiColombo and the Bitcoin low all happened on other days.)

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
