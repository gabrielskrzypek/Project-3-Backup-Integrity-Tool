from backup_integrity_tool import (
    calculate_sha256,
    get_file_hashes,
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