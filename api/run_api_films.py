##################################################################################
# ✅ Script Python complet pour automatiser tout ce processus du Docker
##################################################################################
import subprocess
import socket

# Noms personnalisables
IMAGE_NAME = "img__api_films"
CONTAINER_NAME = "api_films_container"
PORT_HOST = 8000
PORT_CONTAINER = 80

# Vérifie si un port est libre sur localhost
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

# Exécute une commande système
def run_command(command, check=True):
    print(f"👉 {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"❌ Erreur lors de : {command}")
    return result

# Vérifie si le conteneur existe
def container_exists(name):
    result = subprocess.run(
        'docker ps -a --format "{{.Names}}"',
        shell=True, capture_output=True, text=True
    )
    return name in result.stdout.strip().splitlines()

# Vérifie si l’image Docker existe
def image_exists(name):
    result = subprocess.run(
        'docker images --format "{{.Repository}}"',
        shell=True, capture_output=True, text=True
    )
    return name in result.stdout.strip().splitlines()

# Script principal
def main():
    # Vérifie que le port n’est pas occupé
    if is_port_in_use(PORT_HOST):
        raise RuntimeError(f"🚫 Le port {PORT_HOST} est déjà utilisé. Arrête l'application ou choisis un autre port.")

    # Supprime le conteneur existant s’il y en a un
    if container_exists(CONTAINER_NAME):
        print("🗑 Suppression de l’ancien conteneur...")
        run_command(f"docker rm -f {CONTAINER_NAME}")

    # Supprime l’image Docker si elle existe déjà
    if image_exists(IMAGE_NAME):
        print("🧹 Suppression de l’image Docker précédente...")
        run_command(f"docker rmi -f {IMAGE_NAME}")

    # Re-construit l’image
    print("🔨 Construction de la nouvelle image Docker...")
    run_command(f"docker build -t {IMAGE_NAME} .")

    # Lance le conteneur
    print("🚀 Lancement du conteneur...")
    run_command(f"docker run -d -p {PORT_HOST}:{PORT_CONTAINER} --name {CONTAINER_NAME} {IMAGE_NAME}")

    print(f"✅ L'API est accessible sur : http://localhost:{PORT_HOST}/docs")

if __name__ == "__main__":
    main()
