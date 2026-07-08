# Backup Integrity Tool

Backup Integrity Tool is a Python command-line application that checks whether a backup directory is consistent with a source directory.

It compares files recursively using relative paths and SHA256 hashes, then generates a clear integrity report showing which files are identical, missing from the backup, extra in the backup, or modified.

The tool can also optionally create or update a backup by copying missing files from the source directory, with safe defaults, overwrite control, and dry-run support.