# $25,000 by December 31, 2026 — plan

Store: Jamaican-diaspora print-on-demand apparel ("Yaad" brand working name), sold on Etsy + direct
group orders, fulfilled by Printful. Ad budget: $500 total.

## The math

| Channel | Orders | Avg order | Revenue |
|---|---|---|---|
| Group / matching-family orders (personalised, invoiced directly) | ~35 | ~$285 | ~$10,000 |
| Etsy organic search (Jamaican gift, patois, Christmas) | ~200 | ~$38 | ~$7,500 |
| Creator / affiliate partners (15–20% commission, no upfront cost) | ~130 | ~$38 | ~$5,000 |
| Paid ads ($500, only behind proven designs) | ~50 | ~$40 | ~$2,000 |
| **Total** | **~415** | | **~$24,500** |

$25k is not reachable from $500 of ads alone (that would take 50x return on ad spend). It is reachable only if
group orders and creators deliver, because they bring big orders or free reach.
Honest odds: base case $5–12k; $25k needs at least one breakout (a viral video or a large
church or alumni order).

## Calendar (US Christmas delivery cutoff ≈ Dec 12–14 for Printful standard shipping)

| Week | Focus | Revenue goal (cumulative) |
|---|---|---|
| Oct 30 – Nov 5 | Etsy shop live with 14 designs × tee/hoodie; group-order page; draft outreach | $0 |
| Nov 6 – 12 | Outreach to ~150 diaspora alumni chapters, churches, associations; 10 creators seeded with free shirts; $100 ad test | $1,500 |
| Nov 13 – 19 | Double down on top 3 designs; matching family Christmas shirts push | $4,000 |
| Nov 20 – 26 | Pre-Black Friday; $250 ads on winners only | $8,000 |
| Nov 27 – Dec 1 | Black Friday–Cyber Monday sale (20% off, tee+hoodie bundle) | $13,000 |
| Dec 2 – 12 | "Last day to get it by Christmas" countdown; group-order deadline Dec 5 | $22,000 |
| Dec 13 – 31 | Gift cards, Grand Market / New Year drop, Jamaica-bound orders | $25,000 |

## Daily loop (scheduled task)
1. `python3 store/report.py` → revenue vs $/day needed.
2. Kill any ad set with return on ad spend under 1.5x after $25 spent; move budget to the best performer.
3. Etsy: retitle and retag listings that have views but no favourites; add variants of designs that sell.
4. Answer customer email; check Printful for failed or late orders.

## Blocked on owner
- Printful account + API token; Etsy shop connected to Printful in the Printful dashboard.
- Stripe connector authorised (for invoicing group orders).
- Meta/Pinterest ad account with spending cap.
- Approval before any outreach email is sent from your Gmail.
