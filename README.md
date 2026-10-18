# legendmemoria.org

The studio hub for Legends of the Game. GitHub Pages serves this repository from the `main` branch at https://legendmemoria.org/.

## Files

- `index.html`: the hub page.
- `plugins/index.html`: the list of Dalamud plugins. When a plugin gets a new release, update its version number on this page.
- `plugins/icons/`: plugin icons, 128 × 128 px. The page loads them from this site, not from GitHub.
- `plugins/copy.js`: the Copy button for repository URLs.
- `process/index.html`: the "How we work" page. It tells how a tool goes from an idea to a release, and which tools we use.
- `privacy.html`: the privacy policy.
- `404.html`: the page that GitHub Pages shows for an address that does not exist.
- `style.css`: all styles. Light and dark colours follow the system setting.
- `favicon.svg`: the site icon.
- `CNAME`: the custom domain. Do not remove this file.
- `.nojekyll`: stops the Jekyll build. GitHub Pages serves the files as they are.

## Rules

- Do not load files from other servers. The privacy policy states this.
- `privacy.html` covers the whole domain, the Adventurer's Ledger also. If a tool starts to collect, store or send new data, update `privacy.html` before the change goes live.
- Do not create a repository named `legendsofthegame.github.io`. Do not set a custom domain on the user site. If you do, GitHub redirects all project pages (the Adventurer's Ledger also) to this domain, and visitors lose their saved data.

## Preview on your computer

1. Open a terminal in this folder.
2. Run `python -m http.server 8080`.
3. Open http://localhost:8080/ in a browser.

## Advertisements (not in use)

The hub can show one advertisement unit below the content. To start advertisements, do these steps in this order:

1. Update the "Advertisements" and "Cookies" sections of `privacy.html`. Do this before the advertisements start.
2. Add `ads.txt` at the root of the repository.
3. In `index.html`, remove the comment marks around the `ad-slot` block.
4. Put the ad unit inside `ad-slot`. The `.ad-slot` class keeps the height before the ad loads, so that the page does not move.

Do not use Google Auto Ads. Do not use sticky or animated units.

CAUTION: Do not put advertisements on the Adventurer's Ledger. The Ledger states in writing that your data does not leave your browser. An ad script makes that statement false.
