# Glossary — Turkish to English

The project was built in Turkish and the code carried Turkish identifiers: function
names, JSON keys, console output. That is fine for a notebook and wrong for something
other people read. This file fixes the mapping so the rename is consistent rather than
improvised, and so anyone reading an older commit can follow.

Applied on branch `english-identifiers`. Behaviour must not change: the same archive
through the same logic has to produce the same numbers. That equality is the test.

## Domain terms

| Turkish | English | note |
|---|---|---|
| arsiv | archive | |
| anlik goruntu | snapshot | one collector run across three venues |
| damga | stamp | `2026-09-13T0515Z` |
| gun | day | |
| kosu | run | |
| merdiven | ladder | a set of contracts across strikes |
| basamak | rung | one contract in a ladder |
| esik | threshold | the strike or level |
| kova | bucket | range contract |
| fark | gap | prediction price minus option-implied |
| surtunme | friction | fees plus half-spread |
| band | band | threshold = 1.96·SE + friction |
| asan | exceeds | gap larger than the band |
| olculen | measured | |
| sessiz | silent | a row we cannot measure |
| yogunluk | density | |
| zincir | chain | option chain |
| kusatan | bracketing | the two strikes around a level |
| dijital | digital | model-free P(S_T > K) |
| sinir | bound | |
| pencere | window | sync window, seconds between reads |
| kararlilik | stability | does a rung behave the same across runs |
| olcum | measurement | |
| bulgu | finding | |
| oran | ratio | |
| ihlal | violation | |
| varlik | asset | |
| seri | series | |

## Files

| old | new |
|---|---|
| `scripts/arsiv.py` | `scripts/archive.py` |
| `scripts/kararlilik.py` | `scripts/stability.py` |

## JSON keys

`state/latest.json` and `findings/latest.json` are read by `web/index.html`, so they
are an interface, not private naming. They change together with the page.

| old | new |
|---|---|
| `surum` | `version` |
| `damga` | `stamp` |
| `gun` | `day` |
| `yollar` | `paths` |
| `tam_mi` | `complete` |
| `meta_yolu` | `meta_path` |
| `fiyat_penceresi_saniye` | `sync_window_seconds` |
| `arsiv` | `archive` |
| `gun_sayisi` | `day_count` |
| `anlik_goruntu_sayisi` | `snapshot_count` |
| `ilk_gun` / `son_gun` | `first_day` / `last_day` |
| `gunluk` | `per_day` |
| `olcumler` | `measurements` |
| `surtunme_bandi_kalshi` | `friction_band_kalshi` |
| `polymarket_terminal` | `polymarket_terminal` |
| `uzun_ufuk_touch` | `long_horizon_touch` |
| `asan` / `olculen` | `exceeding` / `measured` |
| `oran` | `ratio` |
| `yogunluk_ort` | `density_mean` |
| `farkli_basamak` | `distinct_rungs` |
| `toplam_gozlem` | `total_observations` |
| `basamak_basina_gozlem` | `observations_per_rung` |
| `her_zaman_asan` | `always_exceeds` |
| `bazen_asan` | `sometimes_exceeds` |
| `hic_asmayan` | `never_exceeds` |
| `aritmetik_ihlal` | `arithmetic_violations` |
| `ihlal_orani` | `violation_rate` |
| `oran_2_ustu` | `above_2x` |
| `elenen_touch_merdiveni` | `touch_ladders_excluded` |
| `bosluk_12h_*` | `gap_12h_*` |
| `uretildi` | `produced_by` |

## Version bump

`state/latest.json` goes from `surum: 1` to `version: 2`. During the changeover the
page accepts both, because the collector only writes the new shape on its next
scheduled run and the page must not break in between.

## What is not translated

`scripts/legacy/` keeps its Turkish. Those scripts do not run and are kept for the
reasoning, not the code. Renaming things inside them would suggest they are
maintained.
