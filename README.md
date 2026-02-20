# Switch Homebrew Updater

A small desktop app for downloading the latest GitHub release assets for configured repositories and organizing the results into a Switch-friendly folder structure.

## What it does

- Reads a list of repositories from `config.txt`.
- Lets you choose which configured entries to download from a simple Tkinter UI.
- Downloads assets from each repo's **latest release** (optionally filtered by filename pattern).
- Processes downloaded files into an `Output/` directory:
  - Moves `.nro` files into `Output/switch/`
  - Moves `.ovl` files into `Output/switch/.overlays/`
  - Extracts `.zip` and `.7z` archives and merges recognized folders like `atmosphere`, `switch`, and `bootloader`
  - Copies any files from `Persistent/` into `Output/`

## Requirements

- Python 3.9+
- Packages:
  - `requests`
  - `tqdm`
  - `python-dotenv`
  - `py7zr`

Install dependencies:

```bash
pip install requests tqdm python-dotenv py7zr
```

## Configuration

### `config.txt`

Each non-empty, non-comment line should be one of:

- `owner/repo`
- `owner/repo:pattern`

Where `pattern` is a shell-style wildcard used to match release asset filenames.

Example:

```txt
# Download all latest-release assets
CTCaer/hekate

# Download only matching assets
Atmosphere-NX/Atmosphere:*.zip
LilyLavender/ovlmenu:*.ovl
```

### `.env`

The app reads `GITHUB_TOKEN` from `.env` to increase GitHub API limits.

Example:

```env
GITHUB_TOKEN=ghp_your_token_here
```

If `.env` does not exist, it is created automatically with:

```env
GITHUB_TOKEN=None
```

You can also set or update the token from the app menu:

- `Configure` → `Add a GitHub Token`

## Basic usage

1. Add repositories to `config.txt` (or use `Configure` → `Add a Repository`).
2. Start the app:

```bash
python Update.py
```

3. In the app window:
   - Keep checked entries you want to download.
   - Click **Download Selected**.

4. (Optional) Process archives and organize files:
   - `File` → `Process Downloads`

5. (Optional) Clear downloaded raw files:
   - `File` → `Clear Downloads`

## Folder layout

Common folders used by the app:

- `Downloads/` — raw downloaded files
- `Processing/` — temporary extraction area during processing
- `Output/` — final merged output
- `Persistent/` — optional local files always copied into `Output/`

## Notes

- Downloads use each repository's **latest release** endpoint.
- If a pattern is omitted for an entry, all assets in the latest release are downloaded.
- The app is GUI-based and uses Tkinter.
