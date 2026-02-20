import os

DOWNLOADS_DIR_NAME = "Downloads"


def get_project_root():
    """Return the absolute path to the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_config_path(config_file="config.txt"):
    """Return an absolute path to the configuration file."""
    if os.path.isabs(config_file):
        return config_file
    return os.path.join(get_project_root(), config_file)

def load_config(config_file="config.txt"):
    """
    Load repositories and patterns from a configuration file.

    :param config_file: Path to the configuration file.
    :return: List of repositories and patterns.
    """
    files_to_download = []
    config_path = get_config_path(config_file)
    
    if not os.path.exists(config_path):
        print(f"Config file '{config_path}' not found. Exiting.")
        return files_to_download

    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(":", 1)
            repo = parts[0].strip()
            pattern = parts[1].strip() if len(parts) > 1 else None
            files_to_download.append({"repo": repo, "pattern": pattern})

    return files_to_download

def get_env_path():
    """
    Get the path to the .env file in the project root directory.

    :return: Path to the .env file.
    """
    env_path = os.path.join(get_project_root(), ".env")
    if not os.path.exists(env_path):
        with open(env_path, "w") as env_file:
            env_file.write("GITHUB_TOKEN=None\n")
    return env_path
