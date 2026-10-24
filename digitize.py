#!/usr/bin/env python3
"""Digitize the 瓷音未来 Link-50 frequency response from the published chart.

Source chart: the PNG in source/ (B&K 5128 measurement, JM1-DF compensated,
published by 哔哩哔哩 UP主 "A子如是说").

Axis calibration, verified against every gridline in the image:
  x: log scale, 20 Hz .. 20 kHz, 1340 px per 3 decades
  y: linear, +25 dB .. -25 dB

Usage:
    python digitize.py 24oct > data/Link-50_BK5128_1-24oct.csv
    python digitize.py raw   > data/Link-50_BK5128_raw.csv

The script writes CSV to stdout and never opens a file for writing; redirect
where you want it. The only file it reads is the fixed chart under source/.
"""
import os
import sys

import numpy as np
from PIL import Image

X0, X1 = 114.0, 1454.0     # 20 Hz .. 20 kHz on the log axis
Y0, Y1 = 146.0, 718.0      # +25 dB .. -25 dB on the linear axis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def chart_path():
    """Resolve source/chart.png, refusing anything that escapes the repo."""
    joined = os.path.normpath(os.path.join(BASE_DIR, 'source', 'chart.png'))
    if os.path.commonpath([joined, BASE_DIR]) != BASE_DIR:
        raise ValueError(f'refusing path outside the repository: {joined!r}')
    return joined


def db_of(y):
    return 25.0 - (y - Y0) * 50.0 / (Y1 - Y0)


def load_trace():
    a = np.asarray(Image.open(chart_path()).convert('RGB')).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    sat = a.max(axis=2) - a.min(axis=2)
    # crimson solid curve; the red legend swatch, the pink JM-1 target and
    # the pale green diffuse-field curve each fail one of these tests
    mask = (r >= 150) & (g <= 95) & (b >= 45) & (b <= 170) & (sat >= 90)
    mask[:147, :] = False
    mask[717:, :] = False
    mask[:, :115] = False
    mask[:, 1453:] = False

    def runs_of(col):
        ys = np.nonzero(mask[:, col])[0]
        if len(ys) == 0:
            return []
        out, s, p = [], ys[0], ys[0]
        for y in ys[1:]:
            if y - p <= 2:
                p = y
            else:
                out.append((s, p))
                s = p = y
        out.append((s, p))
        return [(s + e) / 2.0 for s, e in out]

    # continuity tracking: pick the run nearest the previous column so the
    # legend swatch and stray marks are rejected
    xs, ys = [], []
    prev = 380.0
    for x in range(115, 1453):
        cands = runs_of(x)
        if not cands:
            continue
        best = min(cands, key=lambda v: abs(v - prev))
        if abs(best - prev) > 20.0:
            continue
        xs.append(x)
        ys.append(best)
        prev = best
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)

    def medfilt(v, k=3):
        h = k // 2
        return np.array([np.median(v[max(0, i - h):i + h + 1])
                         for i in range(len(v))])

    smoothed = np.convolve(np.pad(medfilt(ys, 3), 2, mode='edge'),
                           np.ones(5) / 5, mode='valid')
    xfull = np.arange(xs.min(), xs.max() + 1)
    return xfull, np.interp(xfull, xs, smoothed)


def emit(freqs, levels):
    out = sys.stdout
    out.write('frequency,spl\n')
    for a, b in zip(freqs, levels):
        out.write(f'{a:.2f},{b:.2f}\n')


def main(mode):
    px, py = load_trace()
    f_raw = 20.0 * 10 ** ((px - X0) / ((X1 - X0) / 3.0))
    db_raw = db_of(py)
    keep = (f_raw >= 20.0) & (f_raw <= 20000.0)
    f_raw, db_raw = f_raw[keep], db_raw[keep]

    if mode == 'raw':
        emit(f_raw, db_raw)
        return

    octaves = np.arange(np.log2(20.0), np.log2(20000.0) + 1e-9, 1.0 / 24.0)
    f_24 = 2.0 ** octaves
    emit(f_24, np.interp(f_24, f_raw, db_raw))


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ('24oct', 'raw'):
        sys.exit('usage: python digitize.py {24oct|raw} > out.csv')
    main(sys.argv[1])
