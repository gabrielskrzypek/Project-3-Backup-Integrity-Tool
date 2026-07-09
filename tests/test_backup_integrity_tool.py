from backup_integrity_tool import calculate_sha256


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

