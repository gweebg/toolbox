#!/bin/python

"""
Automatically install any font familly with any version from Nerd Fonts.

Environmental variables:
    FONTS (str) - comma separated list of the font familly names
    VERSION (str) - version number of the font, 'latest' is allowed
    FONTS_DIR (str) - full path of where to install the fonts

Defaults:
    FONTS - "CascadiaCode, CodeNewRoman, DejaVuSansMono,
             FiraCode, FiraMono, Hack, Iosevka, JetBrainsMono,
             NerdFontsSymbolsOnly, Noto, Ubuntu, UbuntuMono"
    VERSION - "latest"
    FONTS_DIR - "$HOME/.local/share/fonts"
"""

import os
import shutil
import urllib.request
import zipfile

DEFAULT_FONTS: str = "CascadiaCode, CodeNewRoman, DejaVuSansMono, FiraCode, FiraMono, Hack, Iosevka, JetBrainsMono, NerdFontsSymbolsOnly, Noto, Ubuntu, UbuntuMono"

FONTS: list[str] = map(
    lambda f: f.strip(), os.environ.get("FONTS", DEFAULT_FONTS).split(",")
)
VERSION: str = os.environ.get("VERSION", "latest")
BASE_URL: str = "https://github.com/ryanoasis/nerd-fonts/releases/"


def get_fonts_dir() -> str:
    default_font_dir: str = os.environ.get("HOME")
    if not default_font_dir:
        raise Exception("$HOME env variable is not defined")

    default_font_dir += "/.local/share/fonts"
    return os.environ.get("FONTS_DIR", default_font_dir)


FONTS_DIR: str = os.environ.get("FONTS_DIR", get_fonts_dir())


def maybe_create_font_dir() -> None:
    if not os.path.exists(FONTS_DIR):
        os.makedirs(FONTS_DIR, exist_ok=True)
        print(f"created font directory '{FONTS_DIR}'")

    print(f"using font directory '{FONTS_DIR}'")


def get_download_url(font: str) -> str:
    zip_file: str = f"{font}.zip"
    if VERSION == "latest":
        download_url: str = BASE_URL + "latest/download/" + zip_file
    else:
        download_url: str = BASE_URL + f"download/v{VERSION}/{zip_file}"

    return download_url


def download_and_unzip_font(font_name: str) -> None:
    download_url: str = get_download_url(font_name)
    out_file_path: str = FONTS_DIR + f"/{font_name}.zip"

    if os.path.exists(out_file_path.replace(".zip", "")):
        print(f"font '{font_name}' already exists, skipping...")
        return

    print(f"downloading font '{font_name}' from '{download_url}'...")
    with urllib.request.urlopen(download_url) as response, open(
        out_file_path, "wb"
    ) as out_file:
        shutil.copyfileobj(response, out_file)

    print(f"extracting font '{font_name}' to '{FONTS_DIR}'...")
    with zipfile.ZipFile(out_file_path, "r") as zip_ref:
        zip_ref.extractall(out_file_path.replace(".zip", ""))

    print(f"cleaning up '{font_name}'...")
    os.remove(out_file_path)


def download_fonts() -> None:
    print("\ninstalling fonts...\n")
    for font in FONTS:
        download_and_unzip_font(font)
        print(f"font '{font}' setup complete\n")


def main() -> None:
    print(f"using VERSION='{VERSION}'")
    print(f"using FONTS='{FONTS}'")
    maybe_create_font_dir()
    download_fonts()
    print("all fonts setup complete")


if __name__ == "__main__":
    SystemExit(main())
