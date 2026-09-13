# Glossary — Turkish to English

The project was built in Turkish and the code carried Turkish identifiers: function
names, JSON keys, console output. That is fine for a notebook and wrong for something
other people read. This file fixes the mapping so the rename is consistent rather than
improvised, and so anyone reading an older commit can follow.

Applied on branch `english-identifiers`. Behaviour must not change: the same archive
through the same logic has to produce the same numbers. That equality is the test, and
`.github/workflows/migrate_keys.yml` runs it mechanically.

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
| sessiz | skipped | a row we cannot measure |
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
| bosluk | gap | expiry gap, or a hole in trade coverage |
| kapsam | coverage | |
| su isareti | watermark | |
| akis | flow | trade flow |

## Files

| old | new |
|---|---|
| `scripts/arsiv.py` | `scripts/archive.py` |
| `scripts/kararlilik.py` | `scripts/stability.py` |

## `state/latest.json` — the pointer

Read by `web/index.html`, so it is an interface, not private naming. Version 1 to
version 2.

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

## `findings/latest.json` — measurement output

| old | new |
|---|---|
| `uretildi` | `produced_by` |
| `olcumler` | `measurements` |
| `surtunme_bandi_kalshi` | `friction_band_kalshi` |
| `uzun_ufuk_touch` | `long_horizon_touch` |
| `asan` / `olculen` | `exceeding` / `measured` |
| `oran` | `percent` |
| `yogunluk_ort` | `mean_density` |
| `kararlilik` | `stability` |
| `farkli_basamak` | `distinct_rungs` |
| `toplam_gozlem` | `total_observations` |
| `basamak_basina_gozlem` | `observations_per_rung` |
| `her_zaman_asan` | `always_exceeds` |
| `bazen_asan` | `sometimes_exceeds` |
| `hic_asmayan` | `never_exceeds` |
| `aritmetik_ihlal` | `arithmetic_violations` |
| `ihlal_orani` | `violation_percent` |
| `oran_2_ustu` | `ratio_over_two` |
| `elenen_touch_merdiveni` | `touch_ladders_excluded` |
| `bosluk_12h_*` | `gap_12h_*` |

## The archive — our own fields, version 2 to version 3

The archive is translated too. Only the fields WE write are renamed; vendor payloads
keep the names the venue returned, because those are the vendor's data and not ours to
relabel. `raw/deribit/` and `raw/polymarket_events/` therefore contain nothing to
rename at all.

`raw/kalshi/` — the wrapper around the response:

| old | new |
|---|---|
| `katalog` | `catalogue` |
| `secim` | `selection` |
| `secim.kripto` | `selection.crypto` |
| `secim.gozlem` | `selection.observed` |
| `marketler` | `markets` |
| `gozlem` | `observed` |
| `_hata` | `_error` |

`raw/coverage/` — the fetch-coverage record:

| old | new |
|---|---|
| `cekim_utc` | `fetched_utc` |
| `donen` | `returned` |
| `yeni` | `new` |
| `sayfa` | `pages` |
| `en_eski_ts` / `en_yeni_ts` | `oldest_ts` / `newest_ts` |
| `onceki_su_isareti` | `previous_watermark` |
| `limit_doldu` | `limit_hit` |
| `sayfalama_calisti` | `pagination_worked` |
| `ilk_kez` | `first_time` |
| `BOSLUK` | `GAP` |
| `hata` | `error` |

`raw/_meta/` — the run record:

| old | new |
|---|---|
| `toplam_saniye` | `total_seconds` |
| `fiyat_penceresi_saniye` | `sync_window_seconds` |
| `kaynak_anlari_saniye` | `source_marks_seconds` |
| `asama_sureleri` | `stage_seconds` |
| `hatalar` | `errors` |
| `tam_mi` | `complete` |
| `akis_ozeti` | `flow_summary` |
| `kalshi_ozeti` | `kalshi_summary` |
| `dosyalar` / `dosya` / `bayt` | `files` / `file` / `bytes` |
| `varliklar` | `assets` |
| `surum` | `version` |
| `market` | `markets` |
| `kapsam_disi_market` | `out_of_scope_markets` |
| `yeni_islem` | `new_trades` |
| `limit_dolan` | `limit_hit` |
| `BOSLUKLU` | `WITH_GAP` |
| `sayfalama_denendi` | `pagination_tried` |
| `izlenen_kripto_seri` | `crypto_series_tracked` |
| `izlenen_gozlem_seri` | `observed_series_tracked` |
| `market_donen_seri` | `series_returning_markets` |
| `toplam_market` | `total_markets` |
| `gozlem_market` | `observed_markets` |
| `baslangic` / `*_bitis` | `start` / `*_end` |
| `akis` (stage name) | `flow` |

### How the archive gets migrated

Rule 2 says raw data is written once and never modified. That rule protects the vendor
bytes, which the migration does not touch. Our own labels are bookkeeping, not
measurement, and relabelling them changes no number.

1. `collector/collect.py` writes version 3 from now on.
2. `scripts/migrate_archive_keys.py` rewrites the older files. It writes nothing
   without `--apply`, it is idempotent, and an unrecognised key is left alone rather
   than dropped.
3. `.github/workflows/migrate_keys.yml` runs it with the proof attached: measure,
   migrate, measure again, and fail if the two outputs differ.
4. `scripts/archive.py` and `web/index.html` each upgrade an old snapshot at read
   time, in exactly one place. Those two blocks are the only code in the project that
   knows the old names, and they can be deleted once every copy of the archive —
   including the private mirror — has been migrated.

## What is not translated

`scripts/legacy/` keeps its Turkish. Those scripts do not run and are kept for the
reasoning, not the code. Renaming things inside them would suggest they are
maintained.
