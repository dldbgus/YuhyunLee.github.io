# Yuhyun Lee | Editable Research Portfolio

A professional, responsive academic/industry research portfolio with **GitHub Pages + Pages CMS** editing.

## Quick start

See **`START_HERE_한국어.md`** for Korean setup and editing instructions.

Architecture:

- `.pages.yml`: Pages CMS editor schema (text, multiple images, documents)
- `data/*.json`: all user-editable content
- `scripts/build.py`: standard-library-only static-site generator
- `source/template.html`: original home design template
- `assets/illustrations/*.svg`: conceptual figure fallbacks
- `assets/uploads`: CMS-managed images and CV replacements
- `.github/workflows/publish.yml`: GitHub Actions to rebuild and deploy
- `_site/`: generated publication output (do not manually edit)
- `index.html`, `projects/.../index.html`: pre-generated local preview

To build locally: `python3 scripts/build.py`. No pip packages, Node installs, or cloud database required.

For GitHub Pages, set **Source → GitHub Actions**. The workflow publishes `_site`, regenerating the HTML and project detail pages whenever content files are committed from Pages CMS.

To edit through the browser: https://app.pagescms.org — authorize your repository and select `main`.

Public-facing content is in English; editing instructions are in Korean. No analytics, tracking scripts, third-party fonts, cookies, or external CSS frameworks are required.

**Careful:** This portfolio contains an October 2026 CV and some conceptual schematic placeholders. Review scientific claims and publication status before public release.
