"""Push catalog.json designs to Printful as store products.

Env:
  PRINTFUL_API_KEY   private token (developers.printful.com)
  PRINTFUL_STORE_ID  store to create products in (list with --stores)
  FILE_BASE_URL      public URL prefix where designs/out/<slug>.png is reachable

Usage:
  python3 store/printful_sync.py --stores      # list stores
  python3 store/printful_sync.py --costs       # live base costs vs catalog estimates
  python3 store/printful_sync.py --dry-run     # show what would be created
  python3 store/printful_sync.py               # create missing products
"""
import json
import os
import sys
from pathlib import Path

import requests

API = "https://api.printful.com"
ROOT = Path(__file__).resolve().parent
CATALOG = json.loads((ROOT / "catalog.json").read_text())


def call(method, path, **kw):
    headers = {"Authorization": f"Bearer {os.environ['PRINTFUL_API_KEY']}"}
    if os.environ.get("PRINTFUL_STORE_ID"):
        headers["X-PF-Store-Id"] = os.environ["PRINTFUL_STORE_ID"]
    r = requests.request(method, API + path, headers=headers, timeout=60, **kw)
    if r.status_code >= 400:
        sys.exit(f"{method} {path} -> {r.status_code}: {r.text[:500]}")
    return r.json()["result"]


def variants_for(spec):
    """Catalog variant ids matching the configured colours and sizes."""
    variants = call("GET", f"/products/{spec['printful_product_id']}")["variants"]
    return [v for v in variants if v["color"] in spec["colors"] and v["size"] in spec["sizes"]]


def price_for(spec, size):
    return spec["retail_2xl_plus"] if size in ("2XL", "3XL", "4XL", "5XL") else spec["retail"]


def show_costs():
    for key, spec in CATALOG["products"].items():
        for v in variants_for(spec):
            cost = float(v["price"])
            print(f"{key:7} {v['size']:4} cost ${cost:6.2f}  est ${spec['est_cost']:6.2f}  retail ${price_for(spec, v['size']):6.2f}")


def sync(dry_run):
    base = os.environ["FILE_BASE_URL"].rstrip("/")
    existing = {p["name"] for p in call("GET", "/store/products", params={"limit": 100})}
    variant_cache = {k: variants_for(s) for k, s in CATALOG["products"].items()}
    for slug, design in CATALOG["designs"].items():
        for key in design["products"]:
            spec = CATALOG["products"][key]
            name = f"{design['title']} ({spec['label']})"
            if name in existing:
                continue
            body = {
                "sync_product": {"name": name, "external_id": f"{slug}-{key}"},
                "sync_variants": [{
                    "variant_id": v["id"],
                    "external_id": f"{slug}-{key}-{v['id']}",
                    "retail_price": f"{price_for(spec, v['size']):.2f}",
                    "files": [{"type": "front", "url": f"{base}/{slug}.png"}],
                } for v in variant_cache[key]],
            }
            print(("WOULD CREATE " if dry_run else "create ") + name, f"[{len(body['sync_variants'])} variants]")
            if not dry_run:
                call("POST", "/store/products", json=body)


if __name__ == "__main__":
    if "--stores" in sys.argv:
        for s in call("GET", "/stores"):
            print(s["id"], s["type"], s["name"])
    elif "--costs" in sys.argv:
        show_costs()
    else:
        sync("--dry-run" in sys.argv)
