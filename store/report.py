"""Daily/weekly sales report from Printful orders, tracked against the $25k target.

Env: PRINTFUL_API_KEY, PRINTFUL_STORE_ID, AD_SPEND_TO_DATE (optional, USD)
Usage: python3 store/report.py [--days 7]
Appends a row to store/reports/daily.csv and prints a summary.
"""
import csv
import datetime as dt
import os
import sys
from pathlib import Path

from printful_sync import call

TARGET = 25_000
START, END = dt.date(2026, 11, 1), dt.date(2026, 12, 31)
ROOT = Path(__file__).resolve().parent


def orders_since(since):
    out, offset = [], 0
    while True:
        page = call("GET", "/orders", params={"limit": 100, "offset": offset})
        if not page:
            return out
        for o in page:
            created = dt.datetime.fromtimestamp(o["created"]).date()
            if created < since:
                return out
            out.append(o)
        offset += 100


def main():
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 1
    today = dt.date.today()
    season = [o for o in orders_since(START) if o["status"] not in ("canceled", "failed")]
    window = [o for o in season if dt.datetime.fromtimestamp(o["created"]).date() > today - dt.timedelta(days=days)]

    def revenue(orders):
        return sum(float(o["retail_costs"]["total"] or 0) for o in orders)

    def cost(orders):
        return sum(float(o["costs"]["total"] or 0) for o in orders)

    rev, rev_win = revenue(season), revenue(window)
    spend = float(os.environ.get("AD_SPEND_TO_DATE", 0))
    elapsed = max((today - START).days + 1, 1)
    needed_per_day = (TARGET - rev) / max((END - today).days, 1)
    print(f"Last {days}d: {len(window)} orders, ${rev_win:,.2f} revenue")
    print(f"Season:  {len(season)} orders, ${rev:,.2f} revenue ({rev / TARGET:.0%} of ${TARGET:,})")
    print(f"Gross margin after Printful: ${rev - cost(season):,.2f}")
    print(f"Run rate ${rev / elapsed:,.0f}/day vs ${needed_per_day:,.0f}/day needed")
    if spend:
        print(f"Ad spend ${spend:,.2f} -> blended ROAS {rev / spend:.1f}x")
    (ROOT / "reports").mkdir(exist_ok=True)
    path = ROOT / "reports" / "daily.csv"
    new = not path.exists()
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "orders_window", "revenue_window", "orders_season", "revenue_season", "ad_spend"])
        w.writerow([today, len(window), f"{rev_win:.2f}", len(season), f"{rev:.2f}", f"{spend:.2f}"])


if __name__ == "__main__":
    main()
