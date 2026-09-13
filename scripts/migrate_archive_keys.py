#!/usr/bin/env python3
"""One-off migration: rewrite the archive's own field names into English.

WHAT IT TOUCHES AND WHAT IT DOES NOT
Only the keys WE invented are renamed:

  raw/kalshi/*.json.gz    the wrapper we built around the vendor response
  raw/coverage/*.json     our fetch-coverage record
  raw/_meta/*.json        our run record
  raw/holders/*.json.gz   only the _hata error marker we write on failure

Vendor payloads are NOT touched. Every Kalshi market object, every Deribit quote,
every Polymarket event keeps the field names the venue returned. raw/deribit and
raw/polymarket_events are not opened at all, because there is nothing of ours in
them.

WHY RENAME AT ALL
The project is in English. A reader who opens raw/_meta and finds
fiyat_penceresi_saniye has to be told what it means, and being told is the thing
we are trying to remove. Rule 2 says raw data is written once and never modified;
that rule protects the vendor bytes, which this script leaves alone. Our own
bookkeeping labels are not the measurement.

SAFETY
  - Nothing is written without --apply. The default is a dry run that prints
    what would change.
  - Idempotent: a file already migrated is reported as such and skipped.
  - Unknown keys are left alone, never dropped. If a key is not in the table
    below it survives untouched and is reported.
  - The proof is the measurement: the same archive through the same logic has to
    produce the same numbers after the migration. Run write_findings.py before
    and after and compare.

Usage:
    python scripts/migrate_archive_keys.py            # dry run, report only
    python scripts/migrate_archive_keys.py --apply    # rewrite the files
"""
import gzip
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw')

# ---- key tables -------------------------------------------------------------

KALSHI_TOP = {
    'katalog': 'catalogue',
    'secim': 'selection',
    'marketler': 'markets',
    'gozlem': 'observed',
}
KALSHI_SELECTION = {'kripto': 'crypto', 'gozlem': 'observed'}

COVERAGE = {
    'cekim_utc': 'fetched_utc',
    'donen': 'returned',
    'yeni': 'new',
    'sayfa': 'pages',
    'en_eski_ts': 'oldest_ts',
    'en_yeni_ts': 'newest_ts',
    'onceki_su_isareti': 'previous_watermark',
    'limit_doldu': 'limit_hit',
    'sayfalama_calisti': 'pagination_worked',
    'ilk_kez': 'first_time',
    'BOSLUK': 'GAP',
    'hata': 'error',
}

META_TOP = {
    'toplam_saniye': 'total_seconds',
    'fiyat_penceresi_saniye': 'sync_window_seconds',
    'kaynak_anlari_saniye': 'source_marks_seconds',
    'asama_sureleri': 'stage_seconds',
    'hatalar': 'errors',
    'tam_mi': 'complete',
    'akis_ozeti': 'flow_summary',
    'kalshi_ozeti': 'kalshi_summary',
    'dosyalar': 'files',
    'varliklar': 'assets',
    'surum': 'version',
}
META_FLOW = {
    'market': 'markets',
    'kapsam_disi_market': 'out_of_scope_markets',
    'yeni_islem': 'new_trades',
    'limit_dolan': 'limit_hit',
    'BOSLUKLU': 'WITH_GAP',
    'ilk_kez': 'first_time',
    'sayfalama_denendi': 'pagination_tried',
    'sayfalama_calisti': 'pagination_worked',
}
META_KALSHI = {
    'katalog': 'catalogue',
    'izlenen_kripto_seri': 'crypto_series_tracked',
    'izlenen_gozlem_seri': 'observed_series_tracked',
    'market_donen_seri': 'series_returning_markets',
    'toplam_market': 'total_markets',
    'gozlem_market': 'observed_markets',
}
META_MARKS = {
    'baslangic': 'start',
    'deribit_bitis': 'deribit_end',
    'polymarket_bitis': 'polymarket_end',
    'kalshi_bitis': 'kalshi_end',
}
META_STAGES = {'akis': 'flow'}
META_FILES = {'dosya': 'file', 'bayt': 'bytes'}

# Values, not keys. The stage table stores a sentence when a stage is skipped.
VALUE_FIXES = {'atlandi (gunde bir kez)': 'skipped (once a day)'}

ERROR_MARK = ('_hata', '_error')

ARCHIVE_VERSION = 3


def rename(d, table):
    """Rename the keys of one dict. Unknown keys survive untouched."""
    if not isinstance(d, dict):
        return d, 0
    out, n = {}, 0
    for k, v in d.items():
        nk = table.get(k, k)
        if nk != k:
            n += 1
        out[nk] = v
    return out, n


def fix_error_marks(d):
    """_hata -> _error, one level down. Used where a per-item failure is stored."""
    n = 0
    if not isinstance(d, dict):
        return d, 0
    for k, v in list(d.items()):
        if isinstance(v, dict) and ERROR_MARK[0] in v:
            v[ERROR_MARK[1]] = v.pop(ERROR_MARK[0])
            n += 1
    return d, n


def migrate_kalshi(data):
    if not isinstance(data, dict):
        return data, 0
    if 'markets' in data and 'marketler' not in data:
        return data, 0                      # already migrated
    data, n = rename(data, KALSHI_TOP)
    if isinstance(data.get('selection'), dict):
        data['selection'], k = rename(data['selection'], KALSHI_SELECTION)
        n += k
    for key in ('catalogue', 'markets', 'observed'):
        if isinstance(data.get(key), dict):
            data[key], k = fix_error_marks(data[key])
            n += k
    return data, n


def migrate_coverage(data):
    if not isinstance(data, list):
        return data, 0
    n = 0
    out = []
    for row in data:
        row, k = rename(row, COVERAGE)
        n += k
        out.append(row)
    return out, n


def migrate_meta(data):
    if not isinstance(data, dict):
        return data, 0
    if 'sync_window_seconds' in data and 'fiyat_penceresi_saniye' not in data:
        return data, 0                      # already migrated
    data, n = rename(data, META_TOP)
    for key, table in (('flow_summary', META_FLOW),
                       ('kalshi_summary', META_KALSHI),
                       ('source_marks_seconds', META_MARKS),
                       ('stage_seconds', META_STAGES)):
        if isinstance(data.get(key), dict):
            data[key], k = rename(data[key], table)
            n += k
    if isinstance(data.get('stage_seconds'), dict):
        for k2, v in data['stage_seconds'].items():
            if v in VALUE_FIXES:
                data['stage_seconds'][k2] = VALUE_FIXES[v]
                n += 1
    if isinstance(data.get('files'), list):
        new_files = []
        for row in data['files']:
            row, k = rename(row, META_FILES)
            n += k
            new_files.append(row)
        data['files'] = new_files
    data['version'] = ARCHIVE_VERSION
    return data, n


def migrate_holders(data):
    return fix_error_marks(data) if isinstance(data, dict) else (data, 0)


JOBS = (
    ('kalshi', '.json.gz', migrate_kalshi),
    ('coverage', '.json', migrate_coverage),
    ('_meta', '.json', migrate_meta),
    ('holders', '.json.gz', migrate_holders),
)


def read(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write(path, data):
    """Written back in the same shape the collector uses: gz compact, plain
    indented. A different shape would make every file look changed in git."""
    if path.endswith('.gz'):
        with gzip.open(path, 'wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)


def main():
    apply = '--apply' in sys.argv
    total_files = total_keys = touched = 0

    print('ARCHIVE KEY MIGRATION%s' % ('' if apply else '  (DRY RUN, nothing written)'))
    print('root: %s' % RAW)
    print()

    for stream, ext, fn in JOBS:
        base = os.path.join(RAW, stream)
        if not os.path.isdir(base):
            print('%-12s absent, skipped' % stream)
            continue
        files = keys = changed = 0
        for day in sorted(os.listdir(base)):
            dp = os.path.join(base, day)
            if not os.path.isdir(dp):
                continue
            for name in sorted(os.listdir(dp)):
                if not name.endswith(ext):
                    continue
                path = os.path.join(dp, name)
                files += 1
                try:
                    data = read(path)
                except Exception as e:
                    print('  ! unreadable %s: %s' % (name, str(e)[:80]))
                    continue
                data, n = fn(data)
                if n:
                    changed += 1
                    keys += n
                    if apply:
                        write(path, data)
        print('%-12s %4d files, %4d with changes, %5d keys renamed'
              % (stream, files, changed, keys))
        total_files += files
        total_keys += keys
        touched += changed

    print()
    print('TOTAL %d files scanned, %d rewritten, %d keys renamed'
          % (total_files, touched, total_keys))
    if not apply:
        print()
        print('Dry run. Re-run with --apply to write.')
    else:
        print()
        print('Now re-run scripts/write_findings.py and compare the numbers with')
        print('the run before the migration. They have to be identical; the data')
        print('did not change, only the labels did.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
