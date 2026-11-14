import os
import zipfile

def package_skill():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(root_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    zip_path = os.path.join(dist_dir, "ugreen_vaultsense_skill.zip")

    include_dirs = ["vaultsense", "docs", "tests"]
    include_files = [
        "manifest.json",
        "SKILL.md",
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        "LICENSE",
        "README.md",
        "DEVPOST_UGREEN_SUBMISSION.md"
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in include_files:
            fp = os.path.join(root_dir, f)
            if os.path.exists(fp):
                zipf.write(fp, arcname=f)

        for d in include_dirs:
            dp = os.path.join(root_dir, d)
            if os.path.exists(dp):
                for root, _, files in os.walk(dp):
                    for file in files:
                        if "__pycache__" in root or file.endswith(".pyc"):
                            continue
                        full_path = os.path.join(root, file)
                        arc_name = os.path.relpath(full_path, root_dir)
                        zipf.write(full_path, arcname=arc_name)

    print(f"Skill successfully packaged: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    package_skill()
