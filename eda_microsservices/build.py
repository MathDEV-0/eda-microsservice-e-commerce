import os
import threading
import shutil

threads = []


def run_gradle_command(app):
    # Detecta se gradle está disponível
    gradle_cmd = None

    if shutil.which("gradle"):
        gradle_cmd = "gradle"
    else:
        # fallback para wrapper
        if os.name == "nt":
            gradle_cmd = "gradlew.bat"
        else:
            gradle_cmd = "./gradlew"

    command = f"cd {app} && {gradle_cmd} build -x test"
    return os.system(command)


def build_application(app):
    threads.append(threading.current_thread())

    print(f"Building application {app}")
    result = run_gradle_command(app)

    if result != 0:
        print(f"Error building {app}")
    else:
        print(f"Application {app} finished building!")

    threads.remove(threading.current_thread())


def docker_compose_up():
    print("Running containers!")
    os.system("docker-compose up --build -d")
    print("Pipeline finished!")


def build_all_applications():
    print("Starting to build applications!")

    apps = [
        "order-service",
        "orchestrator-service",
        "product-validation-service",
        "payment-service",
        "inventory-service"
    ]

    for app in apps:
        t = threading.Thread(target=build_application, args=(app,))
        t.start()


def remove_remaining_containers():
    print("Removing all containers.")
    os.system("docker-compose down")

    containers = os.popen('docker ps -aq').read().split('\n')
    containers = [c for c in containers if c]

    if containers:
        print(f"There are still {containers} containers created")
        for container in containers:
            print(f"Stopping container {container}")
            os.system(f"docker container stop {container}")

        os.system("docker container prune -f")


if __name__ == "__main__":
    print("Pipeline started!")

    build_all_applications()

    # espera todas as threads terminarem
    while len(threads) > 0:
        pass

    remove_remaining_containers()
    threading.Thread(target=docker_compose_up).start()