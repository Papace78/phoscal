import pytest

from phoscal.cleaning import Cleaner, File
from phoscal.exceptions import FileExtensionNotFound


def test_build_extension_file_mapping():
    files = ["P1.jPg", "P1.raw", "P2.RAW", "P3.jpg", "P3.raw"]
    expected = {
        ".jpg": [File("P1.jPg"), File("P3.jpg")],
        ".raw": [File("P1.raw"), File("P2.RAW"), File("P3.raw")],
    }
    actual = Cleaner.build_extension_file_mapping(files)
    assert actual == expected


def test_find_orphans():
    ext_file_mapping = {
        ".jpg": [File("P1.jPg"), File("P3.jpg")],
        ".raw": [File("P1.raw"), File("P2.RAW"), File("P3.raw")],
    }
    ref_file_ext = ".jpg"
    expected = {".jpg": [], ".raw": [File("P2.RAW")]}
    actual = Cleaner.find_orphans(ext_file_mapping, ref_file_ext)
    assert actual == expected


def test_find_orphans_raises():
    ext_file_mapping = {
        ".jpg": [File("P1.jPg"), File("P3.jpg")],
        ".raw": [File("P1.raw"), File("P2.RAW"), File("P3.raw")],
    }
    ref_file_ext = ".unknown"
    with pytest.raises(FileExtensionNotFound):
        _ = Cleaner.find_orphans(ext_file_mapping, ref_file_ext)


def test_list_files_to_delete():
    orphans = {
        ".jpg": [],
        ".raw": [File("P2.RAW")],
        ".png": [File("P10.png"), File("P45.PNG")],
    }
    expected = [
        File("P2.RAW"),
        File("P10.png"),
        File("P45.PNG"),
    ]
    actual = Cleaner.list_files_to_delete(orphans)
    assert actual == expected


def test_assert_true_is_false():
    assert True
