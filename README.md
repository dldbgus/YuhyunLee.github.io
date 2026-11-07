# Yuhyun Lee — Minimal Academic Research Website

A simple, editable academic profile inspired by classic faculty / researcher sites.

## How it works

- **GitHub Pages** publishes the static website.
- **Pages CMS** at https://app.pagescms.org edits content from `data/*.json` and uploaded research images.
- **GitHub Actions** (`.github/workflows/publish.yml`) runs `python scripts/build.py` on every push.
- HTML is generated automatically; CSS maintains one clean, consistent design.

## To update the existing repository

Copy all files from the **UPDATE_ONLY** ZIP into the root of your *existing, locally cloned* GitHub repo, replacing same-name files. Commit once, then Push origin in GitHub Desktop. Do not copy the enclosing folder or the `.git` directory. You do not need to make a new repository.

## Edit content

Pages CMS: https://app.pagescms.org → select repository → About & contact / Recent news / Research projects / Publications. New photos can be uploaded for your profile and each project; until an image is added, only text appears.

## Build locally (optional)

```bash
python3 scripts/build.py
```

Your source fields are escaped on output, optional image filenames are validated, and external link schemes are restricted to https/mailto.
