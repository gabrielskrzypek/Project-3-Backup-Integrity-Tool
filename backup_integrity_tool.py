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


def compare_directories(source_path, backup_path):

    """
    Compare source and backup directories using relative_paths and SHA256

    Args:
        source_path: Path to the source directory
        backup_path: Path to the backup directory

    Return:
        Dictionary with lists of Ok, missing, extra, and modified files.
    """
    source_hashes = get_file_hashes(source_path)
    backup_hashes = get_file_hashes(backup_path)

    results = {
        "ok": [],
        "missing_in_backup": [],
        "extra_in_backup": [],
        "modified": [],
    }
    for relative_file_path, source_hash in source_hashes.items():
        if relative_file_path not in backup_hashes:
            results["missing_in_backup"].append(relative_file_path)
        elif source_hash == backup_hashes[relative_file_path]:
            results["ok"].append(relative_file_path)
        else:
            results["modified"].append(relative_file_path)

    for relative_file_path in backup_hashes:
        if relative_file_path not in source_hashes:
            results["extra_in_backup"].append(relative_file_path)

    return results

def generate_report(results, source_path, backup_path):
    """
    Generate a report using the results dictionary and source/backup paths.

    Args:
        results: Dictionary returned by compare_directories().
        source_path: Path to the source directory.
        backup_path: Path to the backup directory.

    Returns:
        Report formatted as a string.
    """
    source_path = Path(source_path)
    backup_path = Path(backup_path)

    lines = []

    lines.append("Backup Integrity Tool")
    lines.append("=====================")
    lines.append("")
    lines.append(f"Source: {source_path}")
    lines.append(f"Backup: {backup_path}")
    lines.append("")
    lines.append("Summary:")
    lines.append(f"- OK files: {len(results['ok'])}")
    lines.append(
        f"- Missing in backup: {len(results['missing_in_backup'])}"
    )
    lines.append(
        f"- Extra in backup: {len(results['extra_in_backup'])}"
    )
    lines.append(f"- Modified files: {len(results['modified'])}")
    lines.append("")
    lines.append("Details:")
    lines.append("")

    categories = {
        "OK files": results["ok"],
        "Missing in backup": results["missing_in_backup"],
        "Extra in backup": results["extra_in_backup"],
        "Modified files": results["modified"],
    }

    for title, file_paths in categories.items():
        lines.append(f"{title}:")

        if file_paths:
            for file_path in file_paths:
                lines.append(f"- {file_path}")
        else:
            lines.append("- None")

        lines.append("")

    return "\n".join(lines).rstrip()


def main():
    result = compare_directories("source_data", "backup_data")
    report = generate_report(result, "source_data", "backup_data")
    print(report)


if __name__ == "__main__":
    main()
