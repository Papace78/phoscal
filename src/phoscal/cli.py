import typer
import json
import os
from typer import Option

from phoscal.cleaning import Cleaner

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def clean(
    directory: str = Option(
        ".",
        "-d",
        "--directory",
        help="Photo directory to clean",
    ),
    ext: str = Option(
        ".jpg",
        "-e",
        "--extension",
        help="Reference file extension used for filtering the photos.",
    ),
    force: bool = Option(False, "-f", "--force", help="Don't prompt for confirmation"),
):
    cleaner = Cleaner(directory)
    all_files_in_dir = cleaner.list_all_files_in_dir()
    extension_file_mapping = cleaner.build_extension_file_mapping(all_files_in_dir)
    orphans = cleaner.find_orphans(extension_file_mapping, ext)
    files_to_delete = cleaner.list_files_to_delete(orphans)

    do_delete = True
    if not force:
        typer.echo("You are about to delete: ")
        typer.echo(
            json.dumps(
                {ext: [f.filename for f in files] for ext, files in orphans.items()},
                indent=2,
            )
        )
        do_delete = typer.confirm("Are you sure ?")

    if do_delete:
        cleaner.delete_files(files_to_delete)
        typer.echo("Files deleted.")


@app.command()
def list_orphans(
    directory: str = Option(
        ".",
        "-d",
        "--directory",
        help="Photo directory to clean",
    ),
    ext: str = Option(
        ".jpg",
        "-e",
        "--extension",
        help="Reference file extension used for filtering the photos.",
    ),
):
    cleaner = Cleaner(directory)
    all_files_in_dir = cleaner.list_all_files_in_dir()
    extension_file_mapping = cleaner.build_extension_file_mapping(all_files_in_dir)
    orphans = cleaner.find_orphans(extension_file_mapping, ext)
    for _, files in orphans.items():
        for file in files:
            fullpath = os.path.join(cleaner.dir_path, file.filename)
            typer.echo(fullpath)
