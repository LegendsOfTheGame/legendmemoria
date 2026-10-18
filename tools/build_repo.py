"""Combine each plugin's own repo.json into one repo.json for the whole studio.

Players add https://legendmemoria.org/repo.json to Dalamud once and see every
plugin. sources.json lists the per-plugin manifests. If any source fails, the
script stops before it writes, so a GitHub outage never empties the list.
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("InternalName", "Name", "AssemblyVersion", "DownloadLinkInstall")


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def main():
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    plugins = {}
    for url in sources:
        try:
            entries = fetch(url)
        except Exception as exc:
            sys.exit(f"Could not read {url}: {exc}")
        for entry in entries:
            missing = [k for k in REQUIRED if not entry.get(k)]
            if missing:
                sys.exit(f"{url}: entry lacks {', '.join(missing)}")
            # Last source wins on a duplicate InternalName; there should be none.
            plugins[entry["InternalName"]] = entry

    combined = sorted(plugins.values(), key=lambda e: e["Name"].lower())
    out = json.dumps(combined, indent=2, ensure_ascii=False) + "\n"
    target = ROOT / "repo.json"
    if target.exists() and target.read_text(encoding="utf-8") == out:
        print("repo.json unchanged")
        return
    target.write_text(out, encoding="utf-8", newline="\n")
    print(f"repo.json written: {len(combined)} plugins")


if __name__ == "__main__":
    main()
