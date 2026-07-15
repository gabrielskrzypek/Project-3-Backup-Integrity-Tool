from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import shutil

DEFAULT_OUTPUT_PATH = Path("output_data")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare a source directory with a backup directory using SHA256 hashes."
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source directory.",
    )

    parser.add_argument(
        "--backup",
        required=True,
        help="Path to the backup directory.",
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Print the report without saving it to a file.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help="Directory where report files will be saved.",
    )

    parser.add_argument(
        "--create-backup",
        action="store_true",
        help="Copy files missing from the backup directory.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would be copied without making changes.",
    )   

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite modified files in the backup with source versions.",
    )

    return parser.parse_args()


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


def validate_directory(directory_path, directory_name):
    """
    Validate that a path exists and is a directory.

    Args:
        directory_path: Path to validate.
        directory_name: Human-readable name used in error messages.

    Raises:
        FileNotFoundError: If the path does not exist.
        NotADirectoryError: If the path is not a directory.
    """
    directory_path = Path(directory_path)

    if not directory_path.exists():
        raise FileNotFoundError(
            f"{directory_name} directory does not exist: {directory_path}"
        )
    
    if not directory_path.is_dir():
        raise NotADirectoryError(
            f"{directory_name} path is not a directory: {directory_path}"
        )
    
    return directory_path


def copy_missing_files(source_path, backup_path, missing_files, dry_run=False,):
    """
    Copy missing files from the backup directory.

    Args:
        source_path: Path to the source directory
        backup_path: Path to the backup directory
        missing_files: List of relative paths missing from the backup.
        dry_run: If True, show planned actions without copying files.

    Returns:
        List of relative paths copied or planned for copying.
    """
    source_path = Path(source_path)
    backup_path = Path(backup_path)

    copied_files = []

    for relative_file_path in missing_files:
        source_file_path = source_path / relative_file_path
        backup_file_path = backup_path / relative_file_path

        copied_files.append(relative_file_path)

        if dry_run:
            continue

        backup_file_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(
            source_file_path,
            backup_file_path,
        )

    return copied_files


def overwrite_modified_files(
    source_path,
    backup_path,
    modified_files,
    dry_run=False,
):
    """
    Overwrite modified backup files with the corresponding source files.

    Args:
        source_path: Path to the source directory.
        backup_path: Path to the backup directory.
        modified_files: List of modified relative file paths.
        dry_run: If True, show planned actions without overwriting files.

    Returns:
        List of relative paths overwritten or planned for overwriting.
    """
    source_path = Path(source_path)
    backup_path = Path(backup_path)

    overwritten_files = []

    for relative_file_path in modified_files:
        source_file_path = source_path / relative_file_path
        backup_file_path = backup_path / relative_file_path

        overwritten_files.append(relative_file_path)

        if dry_run:
            continue

        shutil.copy2(
            source_file_path,
            backup_file_path,
        )

    return overwritten_files


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

    report = "\n".join(lines).rstrip()

    return report


def save_report(report, output_path, source_path, backup_path):
    """
    Save report in the output path.

    Args:
        report: Report formatted as a string.
        output_path: Path to the output directory.
        source_path: Path to the source directory.
        backup_path: Path to the backup directory.

    Returns:
        Report.txt file in output path.
    """

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    source_name = Path(source_path).name
    backup_name = Path(backup_path).name

    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Report_{timestamp}_{source_name}-{backup_name}.txt"
    filepath = output_path / filename

    filepath.write_text(report, encoding="utf-8")

    return filepath
    

def main():
    args = parse_args()

    source_path = validate_directory(args.source, "Source")
    backup_path = validate_directory(args.backup, "Backup")
    output_path = Path(args.output)

    results = compare_directories(source_path, backup_path)
    report = generate_report(results, source_path, backup_path)
    
    print(report)

    if args.create_backup:
        copied_files = copy_missing_files(
            source_path,
            backup_path,
            results["missing_in_backup"],
            dry_run=args.dry_run,
        )
        
        overwritten_files = []

        if args.overwrite:
            overwritten_files = overwrite_modified_files(
                source_path,
                backup_path,
                results["modified"],
                dry_run=args.dry_run,
            )
    print("")

    if args.dry_run:
        print("Dry-run mode: no files were modified.")

        if copied_files:
            print("Files that would be copied:")
            for relative_file_path in copied_files:
                print(f"- {relative_file_path}")
        else:
            print("No missing files to copy")
            
        if args.overwrite:
            if overwritten_files:
                print("Files that would be overwritten:")
                for relative_file_path in overwritten_files:
                    print(f"- {relative_file_path}")
            else:
                print("No modified files to overwrite.")

    else:
        if copied_files:
            print("Copied files:")
            for relative_file_path in copied_files:
                print(f"- {relative_file_path}")
        else:
            print("No missing files to copy.")
        
        if args.overwrite:
            if overwritten_files:
                print("Overwritten files:")
                for relative_file_path in overwritten_files:
                    print(f"- {relative_file_path}")
            else:
                print("No modified files to overwrite.")

        if copied_files or overwritten_files:
            results = compare_directories(
                source_path,
                backup_path,
            )

            report = generate_report(
                results,
                source_path,
                backup_path,
            )

            print("")
            print("Verification after backup update:")
            print("")
            print(report)

    if args.no_save:
        print("")
        print("Report was not saved.")
    else:
        save_report_path = save_report (
            report,
            output_path,
            source_path,
            backup_path,
        )
        print("")
        print(f"Report saved to: {save_report_path}")

if __name__ == "__main__":
    main()
