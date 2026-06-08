"""
trendmap_final.py — Thematic Coding Structure Diagram (Figure A1)
Blockchain Technology in Capital Markets (Hajbowicz, 2026)

1. Reads source 2. code 3. category 4. cluster mapping from: Appendix_CodingTable.csv

Produces:
  Figure_CodingStructure.png  (Appendix 3 of thesis)

Coding method: Saldaña (2013) two-cycle thematic coding
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import csv
import os
from collections import defaultdict

#Paths
BASE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "PRACA LICENCJACKA")
CSV_PATH = os.path.join(BASE_DIR, "Appendix_CodingTable.csv")
OUT_PATH = os.path.join(BASE_DIR, "Figure_CodingStructure.png")

#Load coding table
cat_codes   = defaultdict(int)       # category -total code count
cat_sources = defaultdict(set)       # category - set of source names
cat_cluster = {}                     # category -cluster label
src_primary = defaultdict(lambda: defaultdict(int))  # source - {category: code_count}
methodological = set()               # sources flagged as methodology-only

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        src = row['Source'].strip()
        cat = row['Category'].strip()
        clu = row['Cluster'].strip()
        if cat == 'Other' or clu == 'Methodology':
            methodological.add(src)
            continue
        cat_codes[cat] += 1
        cat_sources[cat].add(src)
        cat_cluster[cat] = clu
        src_primary[src][cat] += 1

# Resolve each source's primary category (most codes)
source_to_cat = {}
for src, cats in src_primary.items():
    source_to_cat[src] = max(cats, key=cats.get)

total_codes   = sum(cat_codes.values())
total_sources = len(source_to_cat)
total_cats    = len(cat_codes)

print(f"Loaded: {total_sources} sources, {total_codes} codes, {total_cats} categories")

#Colours
NAVY      = '#030928'
MNAV      = '#1B3A6B'
GOLD      = '#B4865E'
LGOLD     = '#D4A882'
WHITE     = '#FFFFFF'
LGREY     = '#EFF2FC'
DARK      = '#242424'
GALAXY_BG = '#3A2800'
GALAXY_TXT= '#D4A040'

CAT_COLS = {
    'CLUSTER A Technology Enablers':      MNAV,
    'CLUSTER B Regulatory and Governance Forces': '#5C3A1E',
    'CLUSTER C Market and Adoption Dynamics':     '#1A4A35',
}
CLU_COLS = {
    'CLUSTER A Technology Enablers':      NAVY,
    'CLUSTER B Regulatory and Governance Forces': '#3D2210',
    'CLUSTER C Market and Adoption Dynamics':     '#0F3D28',
}
LINE_COLS = {
    'CLUSTER A Technology Enablers':      '#4A6FA0',
    'CLUSTER B Regulatory and Governance Forces': '#8A6040',
    'CLUSTER C Market and Adoption Dynamics':     '#3A7A55',
}

# Layout constants
# Y-positions are visual layout decisions, not derived from data
XS = 1.55;  SW = 2.8    # sources column
XC = 8.1;   CW = 4.6    # categories column
XK = 15.2;  KW = 4.6    # clusters column

CLUSTER_LAYOUT = [
    ('CLUSTER A Technology Enablers',                    7.5),
    ('CLUSTER B Regulatory and Governance Forces',       4.5),
    ('CLUSTER C Market and Adoption Dynamics',           1.5),
]

CATEGORY_LAYOUT = [
    ('Settlement Infrastructure & Efficiency',    8.55),
    ('Asset Tokenisation & DeFi',                 6.85),
    ('AI & Technology Convergence',               5.35),
    ('Regulatory Frameworks & Compliance',        3.90),
    ('Central Bank & Monetary Infrastructure',    2.55),
    ('Market Investment & Adoption Evidence',     1.20),
]

#Source display name overrides 
SRC_DISPLAY = {
    'BIS (2022) — Monetary Systems': 'BIS (2022)',
}
GALAXY_SOURCES = {'Galaxy Research (2025)'}

SOURCE_LAYOUT = [
    ('Mills et al. (2016)',          9.05),
    ('Benos et al. (2019)',          8.60),
    ('Priem (2020)',                 8.15),
    ('Nakamoto (2008)',              7.70),
    ('Tanveer et al. (2025)',        6.95),
    ('Proskurovska & Birch (2025)',  6.50),
    ('Shah et al. (2023)',           6.05),
    ('Adisa et al. (2024)',          5.60),
    ('Zou et al. (2025)',            5.15),
    ('AFME (2025)',                  4.70),
    ('Shukla et al. (2024)',         5.35),
    ('Divissenko (2023)',            3.90),
    ('European Commission (2020)',   3.50),
    ('Wronka (2024)',                3.10),
    ('ESMA (2026)',                  2.70),
    ('BIS (2022) — Monetary Systems', 2.55),
    ('Auer et al. (2020)',           2.10),
    ('Galaxy Research (2025)',       1.20),
]

METH_SOURCES = ['Shi & Herniman (2023)', 'Pólvora et al. (2020)',
                'Schoemaker (1995)', 'Nakamoto (2008)']

#Drawing helpers
def rbox(ax, x, y, w, h, fc, ec=None, lw=0.8, r=0.12):
    ec = ec or fc
    p = FancyBboxPatch((x-w/2, y-h/2), w, h,
                       boxstyle=f'round,pad=0.04,rounding_size={r}',
                       fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(p)

def txt(ax, x, y, s, fs=7, col=WHITE, bold=False,
        ha='center', va='center', italic=False):
    ax.text(x, y, s, fontsize=fs, color=col,
            fontweight='bold' if bold else 'normal',
            fontstyle='italic' if italic else 'normal',
            ha=ha, va=va, zorder=5, clip_on=False)

def line(ax, x1, y1, x2, y2, col='#4A5A6A', lw=0.9, alpha=0.55):
    ax.plot([x1, x2], [y1, y2], color=col, lw=lw, alpha=alpha,
            solid_capstyle='round', zorder=1)

#Build figure
fig, ax = plt.subplots(figsize=(18, 9.5))
fig.patch.set_facecolor(DARK)
ax.set_facecolor(DARK)
ax.set_xlim(0, 18); ax.set_ylim(0, 9.5)
ax.axis('off')

# Cluster boxes
clu_y = {}
for clu_name, y in CLUSTER_LAYOUT:
    rbox(ax, XK, y, KW, 1.65, fc=CLU_COLS[clu_name], ec=GOLD, lw=1.2)
    # Short display name for box
    display = clu_name.replace('CLUSTER A ', 'CLUSTER A\n')\
                      .replace('CLUSTER B ', 'CLUSTER B\n')\
                      .replace('CLUSTER C ', 'CLUSTER C\n')
    txt(ax, XK, y, display, fs=9.5, bold=True)
    rbox(ax, XK, y+0.82-0.08, KW, 0.16, fc=GOLD, ec=GOLD, lw=0)
    clu_y[clu_name] = y

# Category boxes
cat_y = {}
for cat_name, y in CATEGORY_LAYOUT:
    if cat_name not in cat_cluster:
        continue
    clu = cat_cluster[cat_name]
    fc  = CAT_COLS.get(clu, MNAV)
    n_codes = cat_codes[cat_name]
    n_srcs  = len(cat_sources[cat_name])
    meta    = f'{n_codes} codes · {n_srcs} src'

    rbox(ax, XC, y, CW, 0.98, fc=fc, ec='#FFFFFF22', lw=0.5)
    txt(ax, XC, y+0.17, cat_name, fs=8, bold=True)
    txt(ax, XC, y-0.24, meta, fs=6.5, col=LGOLD)
    cat_y[cat_name] = y

    #connect category → cluster
    lc = LINE_COLS.get(clu, '#556677')
    if clu in clu_y:
        line(ax, XC+CW/2, y, XK-KW/2, clu_y[clu], col=lc, lw=1.5, alpha=0.5)

#Source boxes
for src_csv, y in SOURCE_LAYOUT:
    display_name = SRC_DISPLAY.get(src_csv, src_csv)
    is_galaxy    = src_csv in GALAXY_SOURCES

    #Determine primary category from CSV data
    primary_cat = source_to_cat.get(src_csv)

    #Nakamoto: in Settlement (has a code there) but also in methodological strip
    if src_csv == 'Nakamoto (2008)':
        primary_cat = 'Settlement Infrastructure & Efficiency'

    fc  = GALAXY_BG       if is_galaxy else '#0D1635'
    ec  = GOLD            if is_galaxy else '#FFFFFF18'
    lw  = 1.2             if is_galaxy else 0.4
    col = GALAXY_TXT      if is_galaxy else '#C8D4F0'
    label = display_name + (' ⚠' if is_galaxy else '')

    rbox(ax, XS, y, SW, 0.32, fc=fc, ec=ec, lw=lw)
    txt(ax, XS, y, label, fs=6.8, col=col, bold=is_galaxy)

    # Connect source - category
    if primary_cat and primary_cat in cat_y:
        clu = cat_cluster.get(primary_cat, '')
        lc  = LINE_COLS.get(clu, '#556677')
        line(ax, XS+SW/2, y, XC-CW/2, cat_y[primary_cat], col=lc, lw=0.8, alpha=0.35)

#methodological sources strip
rbox(ax, XS, 9.18, SW, 0.40, fc='#181818', ec='#444444', lw=0.6)
txt(ax, XS, 9.28, 'Methodological sources (framework only):', fs=5.8, col='#666666')
txt(ax, XS, 9.10,
    'Shi & Herniman (2023)  ·  Pólvora et al. (2020)  ·  Schoemaker (1995)',
    fs=5.8, col='#555555')

#column headers
for x, label in [(XS, '21 SOURCES'), (XC, '6 CATEGORIES'), (XK, '3 TREND CLUSTERS')]:
    txt(ax, x, 9.32, label, fs=8, col=GOLD, bold=True)

#bottom coding trail bar
rbox(ax, 9, 0.38, 17.5, 0.42, fc=MNAV, ec=GOLD, lw=0.8)
txt(ax, 9, 0.38,
    f'Saldaña (2013) Two-Cycle Thematic Coding:   '
    f'21 sources  →  {total_codes} first-cycle codes  →  {total_cats} categories  →  3 trend clusters emerged',
    fs=8, col=WHITE)

#Galaxy warning
txt(ax, XS, 0.80,
    '⚠ Galaxy Research (2025): website-only — codes require independent verification',
    fs=6.2, col=GALAXY_TXT, italic=True)

#caption
txt(ax, 9, 0.10,
    'Figure A1. Thematic Coding Structure: From Sources to Trend Clusters '
    '(Following Saldaña, 2013). Own elaboration using Python (matplotlib, 2026).',
    fs=6.8, col='#888888', italic=True)

plt.tight_layout(pad=0.2)
plt.savefig(OUT_PATH, dpi=180, bbox_inches='tight', facecolor=DARK)
print(f"Saved: {OUT_PATH}")
