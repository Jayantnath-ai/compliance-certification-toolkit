import os, json, requests

def download_all(registry_path="modules/regulations/registry.json",
                 output_dir="modules/regulations/specifications"):
    os.makedirs(output_dir, exist_ok=True)
    with open(registry_path) as f:
        regs = json.load(f)
    for reg in regs:
        url, rid = reg["url"], reg["id"]
        ext = os.path.splitext(url)[1] or ".pdf"
        out = os.path.join(output_dir, f"{rid}{ext}")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(out, "wb") as w:
            w.write(resp.content)
    return len(regs)
