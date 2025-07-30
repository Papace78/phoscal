import os
from dataclasses import dataclass, field
from collections import defaultdict

from phoscal.exceptions import FileExtensionNotFound


@dataclass
class File:
    filename: str
    basename: str = field(init=False)
    ext: str = field(init=False)

    def __post_init__(self):
        self.basename, ext = os.path.splitext(self.filename)
        self.ext = ext.lower()


class Cleaner:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    @staticmethod
    def build_extension_file_mapping(files: list[str]) -> dict[str, list[File]]:
        res = defaultdict(list)
        for filename in files:
            file = File(filename)
            res[file.ext].append(file)
        return res

    @staticmethod
    def find_orphans(
        ext_file_mapping: dict[str, list[File]],
        ref_file_ext: str,
    ) -> dict[str, list[File]]:
        if ref_file_ext not in ext_file_mapping:
            raise FileExtensionNotFound(
                f"{ref_file_ext} not in extensions {ext_file_mapping.keys()}"
            )
        ref_basenames = [f.basename for f in ext_file_mapping[ref_file_ext]]
        orphans = {
            ext: [*filter(lambda f: f.basename not in ref_basenames, files)]
            for ext, files in ext_file_mapping.items()
        }
        return orphans

    @staticmethod
    def list_files_to_delete(orphans: dict[str, list[File]]) -> list[str]:
        return [file for _, files in orphans.items() for file in files]

    def delete_files(self, files_to_delete: list[File]) -> None:
        for file in files_to_delete:
            full_path = os.path.join(self.dir_path, file.filename)
            os.remove(full_path)
