from pathlib import Path
import hashlib


def calculate_sha256(file_path):

    """
    Calculate the SHA256 hash of a file.

    Args:
        file_path: Path to the file.

    Returns:
        SHA256 hash as a hexadecimal string.
    """
    
    file_path = Path(file_path)

    sha256_hash = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def main():
    print("Backup Integrity Tool")


if __name__ == "__main__":
    main()
