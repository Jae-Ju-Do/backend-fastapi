import hashlib
import shutil
from pathlib import Path


def change_sha256(original_path: str, output_dir: str = None):
    try:
        original_file = Path(original_path)
        if not original_file.exists():
            return {"status_code": 400, "content": f"File not found: {original_path}"}

        # 1. SHA256 해시 계산
        sha256_hash = hashlib.sha256()
        with open(original_file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        hash_hex = sha256_hash.hexdigest()

        # 2. 새 파일 경로 설정
        new_file_name = f"{hash_hex}.exe"

        if output_dir:
            # 지정된 출력 디렉토리가 있으면 거기로 이동
            target_dir = Path(output_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            new_file_path = target_dir / new_file_name
        else:
            # 없으면 현재 디렉토리에서 이름만 변경
            new_file_path = original_file.parent / new_file_name

        # 3. 파일 이름 변경 (이동)
        shutil.move(str(original_file), str(new_file_path))

        return {"status_code": 200, "content": new_file_path}

    except Exception as e:
        return {"status_code": 400, "content": f"sha256 변환 실패 : {e}"}
