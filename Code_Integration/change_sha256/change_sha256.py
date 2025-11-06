import hashlib, os, shutil
from fastapi.responses import JSONResponse


def change_sha256(original_path):
    sha256_dir=r"./filedata/sha256"
    os.makedirs(sha256_dir, exist_ok=True)
    try:
        sha256_hash = hashlib.sha256()
        with open(original_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        hash_hex = sha256_hash.hexdigest()

        new_file_name = f"{hash_hex}.exe"
        new_file_path = os.path.join(sha256_dir, new_file_name)

        shutil.copy2(original_path, new_file_path)
        return {"status_code": 200, "content": new_file_path}

    except Exception as e:
        return {"status_code": 400, "content": f"sha256 변환 실패 : {e}"}
