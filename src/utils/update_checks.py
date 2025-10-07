import requests
import os
import subprocess
import tempfile
import os


def check_for_updates(current_version):
    try:
        response = requests.get(
            "https://api.github.com/repos/eliotora/spell_cards_generator/releases/latest"
        )
        data = response.json()
        latest_version = data.get("tag_name")
        download_url = data.get("assets")[0].get("browser_download_url")

        if latest_version and latest_version != current_version:
            return latest_version, download_url
        else:
            return None, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None, None


def download_and_install(url):
    try:
        # Récupère le nom de fichier à partir de l'URL
        filename = url.split("/")[-1]
        # Crée un chemin temporaire pour stocker l'installeur
        tmp_path = os.path.join(tempfile.gettempdir(), filename)

        print(f"Téléchargement dans : {tmp_path}")

        # Télécharge le fichier
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lève une exception si le téléchargement échoue

        # Écrit le fichier dans un fichier temporaire
        with open(tmp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Vérifie que le fichier a bien été écrit
        if not os.path.exists(tmp_path):
            raise FileNotFoundError(f"Le fichier {tmp_path} n'existe pas après téléchargement.")

        # Exécute le fichier téléchargé
        subprocess.Popen([tmp_path], shell=True)  # shell=True important sur Windows
        os._exit(0)
    except Exception as e:
        print(f"Error downloading update: {e}")
