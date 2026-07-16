from argparse import Namespace
from pathlib import Path
import re

import pytest

from backup_integrity_tool import (
    calculate_sha256,
    get_file_hashes,
    compare_directories,
    generate_report,
    validate_directory,
    copy_missing_files,
    overwrite_modified_files,
    validate_cli_options,
    main,
)



def test_calculate_sha256_same_content(tmp_path):
    file_path = tmp_path / "Sample.txt"
    file_path.write_text("Hash control")

    first_hash = calculate_sha256(file_path)
    second_hash = calculate_sha256(file_path)

    assert first_hash == second_hash


def test_calculate_sha256_different_content(tmp_path):
    first_file_path = tmp_path / "first.txt"
    second_file_path = tmp_path / "second.txt"

    first_file_path.write_text("Hash control")
    second_file_path.write_text("Hash control: different")

    first_hash = calculate_sha256(first_file_path)
    second_hash = calculate_sha256(second_file_path)

    assert first_hash != second_hash    


def test_get_file_hashes_nested_file(tmp_path):
    nested_folder_path = tmp_path / "Contents_folder"
    nested_folder_path.mkdir()

    nested_file_path = nested_folder_path / "Sample.txt"
    nested_file_path.write_text("Sample contents.")

    result = get_file_hashes(tmp_path)

    assert "Contents_folder/Sample.txt" in result
    assert result["Contents_folder/Sample.txt"] == calculate_sha256(nested_file_path)


def test_get_file_hashes_ignores_directories(tmp_path):
    nested_folder_path = tmp_path / "Empty_folder"
    nested_folder_path.mkdir()

    result = get_file_hashes(tmp_path)

    assert "Empty_folder" not in result
    assert result == {}


def test_compare_directories_missing_file(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    (source_path / "Sample.txt").write_text("Only in source")
    
    result = compare_directories(source_path, backup_path)
    
    assert result["ok"] == []
    assert result["missing_in_backup"] == ["Sample.txt"]
    assert result["extra_in_backup"] == []
    assert result["modified"] == []


def test_compare_directories_ok(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    (source_path / "Sample.txt").write_text("Same content")
    (backup_path / "Sample.txt").write_text("Same content")

    result = compare_directories(source_path, backup_path)
    
    assert result["ok"] == ["Sample.txt"]
    assert result["missing_in_backup"] == []
    assert result["extra_in_backup"] == []
    assert result["modified"] == []


def test_compare_directories_modified(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    (source_path / "Sample.txt").write_text("Same content")
    (backup_path / "Sample.txt").write_text("Different content")

    result = compare_directories(source_path, backup_path)
    
    assert result["ok"] == []
    assert result["missing_in_backup"] == []
    assert result["extra_in_backup"] == []
    assert result["modified"] == ["Sample.txt"]


def test_compare_directories_extra(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    (backup_path / "Extra.txt").write_text("Extra in backup")

    result = compare_directories(source_path, backup_path)
    
    assert result["ok"] == []
    assert result["missing_in_backup"] == []
    assert result["extra_in_backup"] == ["Extra.txt"]
    assert result["modified"] == []


def test_generate_report_all_check(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    results = {
        "ok": ["ok_sample.txt"],
        "missing_in_backup": ["missing_sample.txt"],
        "extra_in_backup": ["extra_sample.txt"],
        "modified": ["modified_sample.txt"],
    }

    report = generate_report(results, source_path, backup_path)

    assert "Backup Integrity Tool" in report
    assert "=====================" in report
    assert f"Source: {source_path}" in report
    assert f"Backup: {backup_path}" in report

    assert "Summary:" in report
    assert "- OK files: 1" in report
    assert "- Missing in backup: 1" in report
    assert "- Extra in backup: 1" in report
    assert "- Modified files: 1" in report

    assert "Details:" in report

    assert "OK files:" in report
    assert "- ok_sample.txt" in report

    assert "Missing in backup:" in report
    assert "- missing_sample.txt" in report

    assert "Extra in backup:" in report
    assert "- extra_sample.txt" in report

    assert "Modified files:" in report
    assert "- modified_sample.txt" in report


def test_generate_report_none_for_empty_categories(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    results = {
        "ok": [],
        "missing_in_backup": [],
        "extra_in_backup": [],
        "modified": [],
    }

    report = generate_report(results, source_path, backup_path)

    assert report.count("- None") == 4


def test_validate_directory_returns_path(tmp_path):
    directory_path = tmp_path / "Source"
    directory_path.mkdir()

    result = validate_directory(directory_path, "Source")

    assert result == directory_path
    assert isinstance(result, Path)


def test_validate_directory_raises_if_path_does_not_exist(tmp_path):
    directory_path = tmp_path / "nonexistent"

    expected_message = (
        f"Source directory does not exist: {directory_path}"
    )

    with pytest.raises(
        FileNotFoundError,
        match=re.escape(expected_message),
    ):
        validate_directory(directory_path, "Source")


def test_validate_directory_raises_if_path_is_not_directory(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("content")
    expected_message = (
        f"Source path is not a directory: {file_path}"
    )

    with pytest.raises(
        NotADirectoryError,
        match=re.escape(expected_message),
    ):
        validate_directory(file_path, "Source")


def test_copy_missing_files_copies_file(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    source_file_path = source_path / "missing.txt"
    source_file_path.write_text("Missing file content")

    copied_files = copy_missing_files(
        source_path,
        backup_path,
        ["missing.txt"],
    )

    backup_file_path = backup_path / "missing.txt"

    assert copied_files == ["missing.txt"]
    assert backup_file_path.exists()
    assert backup_file_path.read_text() == "Missing file content"
    assert calculate_sha256(source_file_path) == calculate_sha256(
        backup_file_path
    )


def test_copy_missing_files_creates_parent_directories(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    source_nested_path = source_path / "documents"
    source_nested_path.mkdir()

    source_file_path = source_nested_path / "manual.txt"
    source_file_path.write_text("Manual content")

    copied_files = copy_missing_files(
        source_path,
        backup_path,
        ["documents/manual.txt"],
    )

    backup_file_path = backup_path / "documents" / "manual.txt"

    assert copied_files == ["documents/manual.txt"]
    assert backup_file_path.exists()
    assert backup_file_path.read_text() == "Manual content"
    assert calculate_sha256(source_file_path) == calculate_sha256(
        backup_file_path
    )


def test_copy_missing_files_dry_run_does_not_copy_file(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    source_file_path = source_path / "missing.txt"
    source_file_path.write_text("Missing file content")

    copied_files = copy_missing_files(
        source_path,
        backup_path,
        ["missing.txt"],
        dry_run=True,
    )

    backup_file_path = backup_path / "missing.txt"

    assert copied_files == ["missing.txt"]
    assert not backup_file_path.exists()


def test_overwrite_modified_files_replaces_backup_file(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    source_file_path = source_path / "modified.txt"
    backup_file_path = backup_path / "modified.txt"

    source_file_path.write_text("Current source content")
    backup_file_path.write_text("Old backup content")

    overwritten_files = overwrite_modified_files(
        source_path,
        backup_path,
        ["modified.txt"],
    )

    assert overwritten_files == ["modified.txt"]
    assert backup_file_path.exists()
    assert backup_file_path.read_text() == "Current source content"
    assert calculate_sha256(source_file_path) == calculate_sha256(
        backup_file_path
    )


def test_overwrite_modified_files_dry_run_does_not_modify_backup(tmp_path):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    source_file_path = source_path / "modified.txt"
    backup_file_path = backup_path / "modified.txt"

    source_file_path.write_text("Current source content")
    backup_file_path.write_text("Old backup content")

    overwritten_files = overwrite_modified_files(
        source_path,
        backup_path,
        ["modified.txt"],
        dry_run=True,
    )

    assert overwritten_files == ["modified.txt"]
    assert backup_file_path.read_text() == "Old backup content"


def test_validate_cli_options_accepts_valid_combination():
    args = Namespace(
        create_backup=True,
        overwrite=True,
        dry_run=True,
    )

    validate_cli_options(args)


def test_validate_cli_options_raises_if_overwrite_without_create_backup():
    args = Namespace(
        create_backup=False,
        overwrite=True,
        dry_run=False,
    )

    with pytest.raises(
        ValueError,
        match=re.escape("--overwrite requires --create-backup."),
    ):
        validate_cli_options(args)


def test_validate_cli_options_raises_if_dry_run_without_create_backup():
    args = Namespace(
        create_backup=False,
        overwrite=False,
        dry_run=True,
    )

    with pytest.raises(
        ValueError,
        match=re.escape("--dry-run requires --create-backup."),
    ):
        validate_cli_options(args)

def test_main_shows_clean_error_for_missing_source(monkeypatch, capsys, tmp_path):
    
    backup_path = tmp_path / "Backup"
    backup_path.mkdir()

    nonexistent_source = tmp_path / "nonexistent"

    monkeypatch.setattr(
        "sys.argv",
        [
            "backup_integrity_tool.py",
            "--source",
            str(nonexistent_source),
            "--backup",
            str(backup_path),
            "--no-save",
        ],
    )

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert (
        f"Error: Source directory does not exist: {nonexistent_source}"
        in captured.err
    )
    assert "Traceback" not in captured.err


def test_main_shows_clean_error_for_overwrite_without_create_backup(
    monkeypatch,
    capsys,
    tmp_path,
):
    source_path = tmp_path / "Source"
    backup_path = tmp_path / "Backup"

    source_path.mkdir()
    backup_path.mkdir()

    monkeypatch.setattr(
        "sys.argv",
        [
            "backup_integrity_tool.py",
            "--source",
            str(source_path),
            "--backup",
            str(backup_path),
            "--overwrite",
        ],
    )

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert (
        "Error: --overwrite requires --create-backup."
        in captured.err
    )
    assert "Traceback" not in captured.err