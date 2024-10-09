#!/bin/python

"""
Back up all your installed GNOME Extensions to another folder automatically.

Environmental variables:
    EXTENSIONS_DIR (str) - full path of where the extensions are located
    BACKUP_DIR (str) - full path to where to backup the extensions

Defaults:
    EXTENSIONS_DIR - "$HOME/.local/share/gnome-shell/extensions"
    BACKUP_DIR - "%HOME/.gnome-backup/extensions"
"""

import os
import shutil


def get_home_dir() -> str:
    home_dir: str = os.environ.get("HOME")
    if not home_dir:
        raise Exception("$HOME env variable is not defined")

    return home_dir


def get_extensions_dir_or_default() -> str:
    default = get_home_dir() + "/.local/share/gnome-shell/extensions"
    return os.environ.get("EXTENSIONS_DIR", default)


EXTENSIONS_DIR: str = os.environ.get(
    "EXTENSIONS_DIR", default=get_extensions_dir_or_default()
)


def get_backup_dir_or_default() -> str:
    default = get_home_dir() + "/.gnome-backup/extensions"
    return os.environ.get("BACKUP_DIR", default=default)


BACKUP_DIR: str = os.environ.get("BACKUP_DIR", default=get_backup_dir_or_default())


def backup_extensions() -> None:
    if os.path.exists(BACKUP_DIR):
        overwrite: bool = input(
            f"backup directory '{BACKUP_DIR}' already exists, do you want to overwrite it ? (y/N) "
        ).lower() in ["y", "yes"]

        if overwrite:
            shutil.rmtree(BACKUP_DIR)

    if not os.path.exists(EXTENSIONS_DIR):
        print(f"extensions directory '{EXTENSIONS_DIR}' does not exist, skipping...")
        return

    shutil.copytree(EXTENSIONS_DIR, BACKUP_DIR)


def main() -> None:
    print(f"using EXTENSION_DIR='{EXTENSIONS_DIR}'")
    print(f"using BACKUP_DIR='{BACKUP_DIR}'")
    backup_extensions()
    print("gnome extensions backed up successfully")


if __name__ == "__main__":
    SystemExit(main())
