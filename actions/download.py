import requests
import os
import fnmatch
from tqdm import tqdm

from actions.config import DOWNLOADS_DIR_NAME

def download_github_release(repo, pattern, output_dir=DOWNLOADS_DIR_NAME, token=None):
    """
    Downloads all release assets matching a pattern from a GitHub repository.

    :param repo: GitHub repository in the format "owner/repo".
    :param pattern: Wildcard pattern to match the desired files, or None to download all files.
    :param output_dir: Directory to save the downloaded files.
    :param token: GitHub Personal Access Token (optional for higher rate limits).
    """
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Authorization": f"token {token}"} if token else {}

    api_timeout_seconds = 15
    asset_timeout_seconds = 60

    response = requests.get(api_url, headers=headers, timeout=api_timeout_seconds)
    if response.status_code != 200:
        print(f"Failed to fetch releases for {repo}: {response.status_code} {response.text}")
        return

    release_data = response.json()
    assets = release_data.get("assets", [])

    if not assets:
        print(f"No assets found for {repo}.")
        return

    os.makedirs(output_dir, exist_ok=True)

    downloaded_any = False
    for asset in tqdm(assets, desc=f"Downloading assets from {repo}"):
        asset_name = asset["name"]
        if not pattern or fnmatch.fnmatch(asset_name, pattern):
            download_url = asset["browser_download_url"]
            print(f"Downloading {asset_name} from {repo}...")

            file_path = os.path.join(output_dir, asset_name)

            temp_file_path = f"{file_path}.part"

            try:
                # Download the file
                with requests.get(
                    download_url,
                    headers=headers,
                    stream=True,
                    timeout=asset_timeout_seconds,
                ) as file_response:
                    file_response.raise_for_status()
                    total_size = int(file_response.headers.get("content-length", 0))
                    with open(temp_file_path, "wb") as file:
                        with tqdm(total=total_size, unit="B", unit_scale=True, desc=asset_name) as pbar:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                if not chunk:
                                    continue
                                file.write(chunk)
                                pbar.update(len(chunk))

                os.replace(temp_file_path, file_path)
                print(f"Downloaded: {file_path}")
                downloaded_any = True
            except requests.RequestException as error:
                print(f"Failed to download asset '{asset_name}' from {repo}: {error}")
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            except OSError as error:
                print(f"Failed to save asset '{asset_name}' from {repo}: {error}")
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

    if not downloaded_any:
        print(f"No files found matching pattern: {pattern} for {repo}.")

def start_download(selected_files, github_token=None):
    for file in selected_files:
        repo = file["repo"]
        pattern = file.get("pattern", None)
        download_github_release(repo, pattern, token=github_token)
