"""
Perception Survey Visualisations for my thesis -
Blockchain Technology in Capital Markets (Hajbowicz, 2026)

Generates Figures 5–8 (Appendix 2) from raw survey CSV.
Data: perception survey-c8786e5b.csv (n=38, May 2026)

Figures:
  Figure 5  — Q4:  Current state of blockchain in capital markets
  Figure 6  — Q11: Perceived change in blockchain credibility over 3–5 years
  Figure 7  — Q10: Perceptions of MiCA sufficiency and global coordination
  Figure 8  — Q12: Most likely future scenario for blockchain by 2030
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import csv
import os
from collections import Counter

#Paths
CSV_PATH = os.path.join(os.path.dirname(__file__), "perception survey-c8786e5b.csv")
OUT_DIR  = os.path.join(os.path.expanduser("~"),
                        "Desktop", "PRACA LICENCJACKA")
os.makedirs(OUT_DIR, exist_ok=True)

#data
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))[1:]   #skip header row

N = len(rows)   #38

#style
FONT  = "DejaVu Sans"
BLUE  = "#1B3A6B"
LGREY = "#EFF2FC"

plt.rcParams.update({
    "font.family":       FONT,
    "font.size":         10,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  False,
    "axes.grid":         True,
    "axes.grid.axis":    "x",
    "grid.color":        "#DDDDDD",
    "grid.linewidth":    0.6,
    "figure.dpi":        150,
    "savefig.bbox":      "tight",
    "savefig.pad_inches": 0.15,
})


def save_barh(fname, title, labels, counts, colour=BLUE):
    """Horizontal bar chart — labels on Y, % values on bars."""
    total = sum(counts)
    pcts  = [c / total * 100 for c in counts]

    fig_h = max(2.8, 0.55 * len(labels) + 1.2)
    fig, ax = plt.subplots(figsize=(7, fig_h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.barh(labels, pcts, color=colour, height=0.55, zorder=3)

    # value labels inside / outside bars
    for bar, pct, cnt in zip(bars, pcts, counts):
        x = bar.get_width()
        label_txt = f"{pct:.0f}%  (n={cnt})"
        ax.text(
            x + 0.6, bar.get_y() + bar.get_height() / 2,
            label_txt, va="center", ha="left",
            fontsize=9, color="#333333"
        )

    ax.set_xlabel("% of respondents", fontsize=9, color="#555555")
    ax.set_xlim(0, max(pcts) * 1.35)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=8, colors="#777777")
    ax.invert_yaxis()

    ax.set_title(title, fontsize=11, fontweight="bold",
                 color="#1A1A1A", pad=10, loc="left")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, fname)
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


#Figure 5 — Q4: Current state of blockchain
q4_raw = Counter(r[4] for r in rows)
q4_order = [
    "Gradually being adopted in specific use cases",
    "I don't know enough to say",
    "Past the hype, but struggling to scale",
    "Already mainstream in the industry",
    "Still mostly hype, limited real use",
]
q4_labels = [
    "Gradually being adopted\nin specific use cases",
    "I don't know enough to say",
    "Past the hype,\nbut struggling to scale",
    "Already mainstream\nin the industry",
    "Still mostly hype,\nlimited real use",
]
q4_counts = [q4_raw[k] for k in q4_order]

save_barh(
    "Survey_Q4_CurrentState.png",
    "Figure 5. Current State of Blockchain in Capital Markets (Q4, n=38)",
    q4_labels, q4_counts,
)

#Figure 6 — Q11: Credibility change 
q11_raw = Counter(r[11] for r in rows)
q11_order = [
    "Improved significantly",
    "Improved slightly",
    "Stayed the same",
    "I don't know",
    "Declined",
]
q11_labels = [
    "Improved significantly",
    "Improved slightly",
    "Stayed the same",
    "I don't know",
    "Declined",
]
q11_counts = [q11_raw[k] for k in q11_order]

save_barh(
    "Survey_Q11_Credibility.png",
    "Figure 6. Perceived Change in Blockchain Credibility over 3–5 Years (Q11, n=38)",
    q11_labels, q11_counts,
)

#Figure 7 — Q10: MiCA / global coordination
q10_raw = Counter(r[10] for r in rows)
q10_order = [
    "I'm not familiar with MiCA",
    "Global coordination is necessary",
    "Regulation is holding blockchain back",
    "MiCA is enough for now",
]
q10_labels = [
    "I'm not familiar with MiCA",
    "Global coordination is necessary",
    "Regulation is holding\nblockchain back",
    "MiCA is enough for now",
]
q10_counts = [q10_raw[k] for k in q10_order]

save_barh(
    "Survey_Q10_MiCA.png",
    "Figure 7. Perceptions of MiCA Sufficiency and Global Coordination (Q10, n=38)",
    q10_labels, q10_counts,
)

#Figure 8 — Q12: Most likely scenario by 2030
q12_raw = Counter(r[12] for r in rows)
q12_order = [
    "Blockchain stays niche, used only in specific cases",
    "Blockchain thrives in the EU but remains fragmented globally",
    "I have no idea",
    "Blockchain becomes a global standard in capital markets",
    "Blockchain adoption stalls or reverses",
]
q12_labels = [
    "Blockchain stays niche,\nused only in specific cases",
    "Blockchain thrives in the EU\nbut remains fragmented globally",
    "I have no idea",
    "Blockchain becomes a global\nstandard in capital markets",
    "Blockchain adoption\nstalls or reverses",
]
q12_counts = [q12_raw[k] for k in q12_order]

save_barh(
    "Survey_Q12_Scenarios.png",
    "Figure 8. Most Likely Future Scenario for Blockchain by 2030 (Q12, n=38)",
    q12_labels, q12_counts,
)

print(f"\nAll 4 survey charts saved to {OUT_DIR}")
