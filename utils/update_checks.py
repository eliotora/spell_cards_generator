import requests
import os
import subprocess
import tempfile
import os


def check_for_updates(current_version):
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/eliotora/spell_cards_generator/main/version.json"
        )
        data = response.json()
        print(data)
        latest_version = data.get("version")
        download_url = data.get("url")

        if latest_version and latest_version != current_version:
            return latest_version, download_url
        else:
            return None, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None, None


def download_and_install(url):
    try:
        response = requests.get(url, stream=True)
        filename = url.split("/")[-1]
        tmp_path = os.path.join(tempfile.gettempdir(), filename)
        with open(tmp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        subprocess.Popen(["start", tmp_path])
        os._exit(0)
    except Exception as e:
        print(f"Error downloading update: {e}")
