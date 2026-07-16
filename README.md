# Backup Integrity Tool

Backup Integrity Tool is a Python command-line application that checks whether a backup directory is consistent with a source directory.

It compares files recursively using relative paths and SHA256 hashes. The tool can detect which files are identical, missing from the backup, extra in the backup, or modified.

# Currently implemented:

- Initial project structure.
- SHA256 hash calculation for individual files.
- Recursive file scanning.
- File hash collection using relative paths.
- Source and backup directory comparison.
- Detection of:
  - identical files,
  - files missing from backup,
  - extra files in backup,
  - modified files.
- Text report generation.
- Optional report saving with timestamped filenames.
- Custom output directory with `--output`.
- `--no-save` mode.
- Command-line arguments with `argparse`.
- Source and backup path validation.
- Optional backup creation with `--create-backup`.
- Copying of files missing from the backup.
- Automatic creation of missing subdirectories.
- Optional overwrite of modified backup files with `--overwrite`.
- `--dry-run` mode for previewing copy and overwrite actions.
- Verification after backup updates.
- Validation of incompatible CLI options:
  - `--overwrite` requires `--create-backup`.
  - `--dry-run` requires `--create-backup`.
- Clean CLI error messages without full tracebacks.
- Errors are written to `stderr` and return exit code `1`.
- 23 pytest tests covering:
  - hash calculation,
  - recursive scanning,
  - directory comparison,
  - report generation,
  - path validation,
  - missing-file copying,
  - subdirectory creation,
  - overwrite behavior,
  - dry-run behavior,
  - CLI option validation,
  - clean CLI error handling.
- Readme usage examples.


## Technologies

- Python
- pathlib
- hashlib
- argparse
- datetime
- shutil
- pytest

## Installation

Clone the repository:

```bash
git clone git@github.com:gabrielskrzypek/Backup-Integrity-Tool.git
cd Backup-Integrity-Tool
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install development dependencies:

```bash
pip install -r dev-requirements.txt
```

## Usage

Compare a source directory with a backup directory:

```bash
python backup_integrity_tool.py \
  --source source_data \
  --backup backup_data
```

Run without saving a report:

```bash
python backup_integrity_tool.py \
  --source source_data \
  --backup backup_data \
  --no-save
```

Save reports in a custom directory:

```bash
python backup_integrity_tool.py \
  --source source_data \
  --backup backup_data \
  --output reports
```

Copy files missing from the backup:

```bash
python backup_integrity_tool.py \
  --source source_data \
  --backup backup_data \
  --create-backup
```

Preview backup changes without modifying files:

```bash
python backup_integrity_tool.py \
  --source source_data \
  --backup backup_data \
  --create-backup \
  --dry-run \
  --no-save
```

Copy missing files and overwrite modified backup files:

```bash
python backup_integrity_tool.py \
  --source source_data \
  --backup backup_data \
  --create-backup \
  --overwrite
```

Display the CLI help:

```bash
python backup_integrity_tool.py --help
```

## Report categories

The tool classifies files into four categories:

- `OK`: the file exists in both directories and has the same SHA256 hash.
- `MISSING_IN_BACKUP`: the file exists in the source but not in the backup.
- `EXTRA_IN_BACKUP`: the file exists in the backup but not in the source.
- `MODIFIED`: the file exists in both directories, but its SHA256 hashes are different.

## Safety

- Extra files in the backup are reported but never deleted.
- Modified files are not replaced unless `--overwrite` is used.
- `--dry-run` previews copy and overwrite actions without modifying files.
- Invalid CLI option combinations are rejected before file operations begin.
- The directories are compared again after a real backup update.

## Running tests

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

The current test suite contains 23 tests covering:

- SHA256 hash calculation.
- Recursive directory scanning.
- Directory comparison.
- Report generation.
- Path validation.
- Missing-file copying.
- Subdirectory creation.
- Overwrite behavior.
- Dry-run behavior.
- CLI option validation.
- Clean CLI error handling.

## Project status

Completed.