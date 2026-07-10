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

def get_file_hashes(folder_path):

    """
    Calculate the SHA256 hash of all files in folder path.

    Args:
        folder_path: Path to the folder to scan.

    Returns:
        A dictionary with file_relative_paths as keys and SHA256 hashes as values
    """
    folder_path = Path(folder_path)

    file_hashes = {}

    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            relative_file_path = file_path.relative_to(folder_path)
            file_hashes[str(relative_file_path)] = calculate_sha256(file_path)

    return file_hashes

def main():
    print("Backup Integrity Tool")


if __name__ == "__main__":
    main()
