"""Copy Apex and the Adventurer's Ledger into this site from their own repos.

Usage: python3 tools/sync_apps.py <Game-Challenge-Tracker checkout> <pandora-lunar checkout>

Apex: copies the whole apex/ folder, removes the Google Fonts and manifest links (this
site loads nothing from other hosts and has no manifest), and writes apex/version.json
when a file changed.

Lunar: copies index.html and every local file that it loads. The pandora-lunar workflows
refresh collection-lists.js and events-feed.js, so lunar/index.html loads those two from
the pandora-lunar Pages site instead. If index.html no longer has the two script tags,
the script stops and changes nothing in lunar/.
"""
import datetime
import pathlib
import re
import shutil
import subprocess
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent
LUNAR_PAGES = "https://legendsofthegame.github.io/pandora-lunar/"
LUNAR_FEEDS = ["collection-lists.js", "events-feed.js"]
APEX_DROP = ['<link rel="manifest" href="manifest.json">', "fonts.googleapis.com/css2"]


def commit_of(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()


def write_if_changed(path, data):
    """Write bytes to path. Returns True when the content changed."""
    if path.exists() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


def sync_apex(gct):
    src = gct / "apex"
    changed = False
    for f in sorted(p for p in src.rglob("*") if p.is_file()):
        rel = f.relative_to(src)
        data = f.read_bytes()
        if rel.as_posix() == "index.html":
            lines = data.decode("utf-8").splitlines(keepends=True)
            data = "".join(l for l in lines if not any(d in l for d in APEX_DROP)).encode("utf-8")
        changed |= write_if_changed(SITE / "apex" / rel, data)
    if changed:
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        version = '{"v":"%s","t":"%s"}' % (commit_of(gct)[:8], now)
        write_if_changed(SITE / "apex" / "version.json", version.encode("utf-8"))
    return changed


def sync_lunar(pl):
    html = (pl / "index.html").read_text(encoding="utf-8")
    for feed in LUNAR_FEEDS:
        tag = '<script src="%s"></script>' % feed
        if tag not in html:
            sys.exit("lunar: index.html has no tag %s; lunar/ was not changed" % tag)
        html = html.replace(tag, '<script src="%s%s"></script>' % (LUNAR_PAGES, feed))
    local = [u for u in re.findall(r'(?:src|href)="([^"]+)"', html)
             if not re.match(r"[a-z]+:|#|/|\./?$|\.\./", u)]
    changed = write_if_changed(SITE / "lunar" / "index.html", html.encode("utf-8"))
    for rel in sorted(set(local)):
        f = pl / rel
        if f.is_file():
            changed |= write_if_changed(SITE / "lunar" / rel, f.read_bytes())
    return changed


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    apex = sync_apex(pathlib.Path(sys.argv[1]))
    lunar = sync_lunar(pathlib.Path(sys.argv[2]))
    print("apex changed" if apex else "apex unchanged")
    print("lunar changed" if lunar else "lunar unchanged")
