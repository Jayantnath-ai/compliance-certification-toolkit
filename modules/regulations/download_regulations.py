import os
import requests
import json

def download_regulations(registry_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(registry_path, "r") as f:
        regs = json.load(f)

    for reg in regs:
        url = reg["url"]
        rid = reg["id"]
        name = reg["name"]
        print(f"Downloading {rid}: {name}")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            ext = os.path.splitext(url)[1] or ".pdf"
            file_path = os.path.join(output_dir, f"{rid}{ext}")
            with open(file_path, "wb") as out_file:
                out_file.write(response.content)
            print(f"Saved to {file_path}")
        except Exception as e:
            print(f"Failed to download {rid}: {e}")

if __name__ == "__main__":
    registry = "modules/regulations/registry.json"
    output_directory = "modules/regulations/specifications"
    download_regulations(registry, output_directory)
