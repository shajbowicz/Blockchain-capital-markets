"""
code for thesis charts — Blockchain Technology in Capital Markets
Author: Szymon Hajbowicz
the code generates 4 PNG figures for the bachelor's thesis.

Sources:
  Figure 1: CoinGecko (2026a, 2026b) — Global crypto market cap
  Figure 2: AFME (2026) — DLT fixed income issuance 2021–2025
  Figure 3: Galaxy Research (2025) — Crypto VC funding 2021–2025
  Figure 4: ESMA (2026) — MiCA CASP authorisations growth
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
import os

#Output dir
OUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "PRACA LICENCJACKA")
os.makedirs(OUT_DIR, exist_ok=True)

#style
FONT = "DejaVu Sans"
plt.rcParams.update({
    "font.family": FONT,
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

NAVY   = "#1B3A6B"
TEAL   = "#2E8B8B"
AMBER  = "#E07B39"
GREY   = "#8C8C8C"
LGREY  = "#E8E8E8"
RED    = "#C0392B"


#FIGURE 1 - Global Crypto Market Capitalisation with Hype Cycle Phases
def fig1_market_cap():
    # Approximate yearly / key data points (USD billions)
    # Source: CoinGecko historical data, CoinGecko Q1 2026 Report
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
             2022, 2023, 2024, 2025.75, 2026.25]
    mcap  = [   2,   6,   7,   17,  600,  130,  200,  760, 2900,
               821, 1100, 3700,  4400,  2379]
    # 2022 = trough $821bn (Nov); 2025.75 = peak ~$4.4T (Oct 2025);
    # 2026.25 = end Q1 2026 $2.4T

    fig, ax = plt.subplots(figsize=(8.5, 4.8))

    # add coloured background bands for each hype cycle phase
    phases = [
        (2013, 2016, "#EAF4FB", "Innovation\nTrigger"),
        (2016, 2018, "#FEF9E7", "Peak of Inflated\nExpectations"),
        (2018, 2023, "#FDF2F8", "Trough of\nDisillusionment"),
        (2023, 2026.5, "#EAFAF1", "Slope of\nEnlightenment"),
    ]
    for x0, x1, color, label in phases:
        ax.axvspan(x0, x1, color=color, alpha=0.85, zorder=0)
        ax.text((x0 + x1) / 2, 4650, label,
                ha="center", va="top", fontsize=7.5, color="#555",
                style="italic", multialignment="center")

    # Main line
    ax.plot(years, mcap, color=NAVY, linewidth=2.2, zorder=3, marker="o",
            markersize=4.5, markerfacecolor="white", markeredgewidth=1.5,
            markeredgecolor=NAVY)

    # Key annotations
    ax.annotate("Trough: $821bn\n(Nov 2022)",
                xy=(2022, 821), xytext=(2020.5, 1600),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
                fontsize=8, color=RED, ha="center")

    ax.annotate("Peak: ~$4.4T\n(Oct 2025)",
                xy=(2025.75, 4400), xytext=(2023.0, 4200),
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.2),
                fontsize=8, color=AMBER, ha="center")

    ax.annotate("Q1 2026 end:\n$2.38T (+190%\nfrom trough)",
                xy=(2026.25, 2400), xytext=(2025.0, 700),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2),
                fontsize=8, color=TEAL, ha="center")

    ax.set_xlim(2013, 2026.9)
    ax.set_ylim(0, 5300)
    ax.set_xlabel("Year", labelpad=6)
    ax.set_ylabel("Market Capitalisation (USD billions)", labelpad=6)
    ax.set_title(
        "Figure 1. Global Cryptocurrency Market Capitalisation and\n"
        "Hype Cycle Phase Mapping, 2013–Q1 2026", pad=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${int(x):,}bn"))
    ax.set_xticks(range(2013, 2027))
    ax.tick_params(axis="x", rotation=45)
    ax.text(0.99, 0.02, "Source: CoinGecko (2026a, 2026b)",
            transform=ax.transAxes, fontsize=7, color=GREY, ha="right")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "Figure1_MarketCap_HypeCycle.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


#FIGURE 2 — AFME DLT Fixed Income Issuance 2021–2025
def fig2_afme():
    years  = ["2021", "2022", "2023", "2024", "2025"]
    values = [270, 882, 860, 3251, 4811]  #millions of EUR

    fig, ax = plt.subplots(figsize=(7, 4.5))

    bars = ax.bar(years, values, color=[LGREY, LGREY, LGREY, TEAL, NAVY],
                  width=0.55, edgecolor="white", linewidth=0.5, zorder=3)

    #add value labels on top of each bar
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 55,
                f"€{val:,}m",
                ha="center", va="bottom", fontsize=8.5, color=NAVY, fontweight="bold")

    #addarrow showing total growth from 2021 to 2025
    ax.annotate("", xy=(4, 4811), xytext=(0, 270),
                arrowprops=dict(arrowstyle="-|>",
                                color=AMBER, lw=1.5,
                                connectionstyle="arc3,rad=-0.25"))
    ax.text(2.5, 3800, "+1,682%\n(2021→2025)", ha="center",
            fontsize=8.5, color=AMBER, fontweight="bold")

    ax.set_ylim(0, 5800)
    ax.set_xlabel("Year", labelpad=6)
    ax.set_ylabel("Issuance Volume (EUR millions)", labelpad=6)
    ax.set_title(
        "Figure 2. DLT-Enabled Fixed Income Issuance in Global\n"
        "Capital Markets, 2021–2025 (EUR millions)", pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"€{int(x):,}m"))
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=0)
    ax.text(0.99, 0.02, "Source: AFME (2025)",
            transform=ax.transAxes, fontsize=7, color=GREY, ha="right")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "Figure2_AFME_DLT_Issuance.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


#FIGURE 3 — Crypto VC Funding 2021–2025
def fig3_vc():
    years  = ["2021", "2022", "2023", "2024", "2025"]
    values = [33.0, 16.5, 9.0, 11.5, 20.0]  #billions of USD

    fig, ax = plt.subplots(figsize=(7, 4.5))

    colors = [LGREY, LGREY, RED, LGREY, NAVY]
    bars = ax.bar(years, values, color=colors,
                  width=0.55, edgecolor="white", linewidth=0.5, zorder=3)

    #add a trend line over the bars
    x_pos = range(len(years))
    ax.plot(list(x_pos), values, color=TEAL, linewidth=1.8,
            marker="o", markersize=5, markerfacecolor="white",
            markeredgewidth=1.5, markeredgecolor=TEAL, zorder=4)

    #add value labels on top of each bar
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"${ val:.0f}bn",
                ha="center", va="bottom", fontsize=8.5,
                color=NAVY, fontweight="bold")

    #annotate the trough and recovery points
    ax.annotate("Trough ~$9bn\n(2023)",
                xy=(2, 9.0), xytext=(0.7, 14),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
                fontsize=8, color=RED, ha="center")
    ax.annotate("Recovery: $20bn\n(+122% vs 2023)",
                xy=(4, 20.0), xytext=(3.1, 25),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2),
                fontsize=8, color=TEAL, ha="center")

    ax.set_ylim(0, 40)
    ax.set_xlabel("Year", labelpad=6)
    ax.set_ylabel("VC Investment (USD billions)", labelpad=6)
    ax.set_title(
        "Figure 4. Global Crypto-Sector Venture Capital Funding,\n"
        "2021–2025 (USD billions)", pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${x:.0f}bn"))
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=0)
    ax.text(0.99, 0.02, "Source: Galaxy Research (2025)",
            transform=ax.transAxes, fontsize=7, color=GREY, ha="right")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "Figure4_Galaxy_VC_Funding.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


#FIGURE 4 — ESMA MiCA CASP Authorisations Growth
def fig4_casp():
    #monthly CASP counts from ESMA public register, Dec 2024 to May 2026
    labels = ["Dec\n2024", "Feb\n2025", "Apr\n2025", "Jun\n2025",
              "Aug\n2025", "Oct\n2025", "Dec\n2025", "Feb\n2026",
              "Apr\n2026", "May\n2026"]
    counts = [1, 6, 17, 35, 58, 80, 102, 140, 178, 204]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8, 4.5))

    #fill area under the line
    ax.fill_between(x, counts, alpha=0.12, color=NAVY, zorder=1)
    ax.plot(x, counts, color=NAVY, linewidth=2.2, zorder=3,
            marker="o", markersize=5.5, markerfacecolor="white",
            markeredgewidth=1.8, markeredgecolor=NAVY)

    #mark start and end points
    ax.annotate("MiCA fully\napplicable\n(1 CASP)",
                xy=(0, 1), xytext=(0.8, 50),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2),
                fontsize=8, color=GREY, ha="center")
    ax.annotate("204 CASPs\n(May 2026)",
                xy=(9, 204), xytext=(7.8, 170),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2),
                fontsize=8.5, color=TEAL, ha="center", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylim(0, 240)
    ax.set_xlabel("Date", labelpad=6)
    ax.set_ylabel("Number of Authorised CASPs", labelpad=6)
    ax.set_title(
        "Figure 3. Growth of ESMA-Authorised MiCA Crypto-Asset\n"
        "Service Providers (CASPs), December 2024 – May 2026", pad=10)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=0)
    ax.text(0.99, 0.02, "Source: ESMA (2026); CASPS.csv (last updated 22 May 2026)",
            transform=ax.transAxes, fontsize=7, color=GREY, ha="right")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "Figure3_ESMA_CASP_Growth.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


# -------------------------
if __name__ == "__main__":
    fig1_market_cap()
    fig2_afme()
    fig3_vc()
    fig4_casp()
    print("\nAll 4 figures saved to:", OUT_DIR)
