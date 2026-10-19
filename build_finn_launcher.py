r"""Build Finn Launcher from the owner's original TCL Flip 4 5G launcher ZIP.

This script DOES NOT connect to or modify the phone. It writes a new application.zip
in a sibling Finn-Launcher-Build folder; it never overwrites the source ZIP.

Usage (from the project folder):
    py .\Finn-Launcher-GitHub\build_finn_launcher.py .\TCL-Launcher-Recovery-Step234.zip
"""

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile
import sys

ROOT = Path(__file__).resolve().parent
ASSETS = (
    "finn-launcher.js",
    "finn-launcher.css",
    "finn-launcher-wallpaper.css",
    "Finn-Launcher-Wallpaper.png",
    "Finn-Launcher-System-Black.png",
)

OLD_BRIDGE = b'debug:function(){}};t.default=r}'
NEW_BRIDGE = b'debug:function(){}};window.TCLLauncherServices=r;t.default=r}'

ANCHOR = '<script defer="" src="dist/app.bundle.js"></script>'
ADDITIONS = (
    '<link rel="stylesheet" href="finn-launcher.css">',
    '<script defer="" src="finn-launcher.js"></script>',
    '<link rel="stylesheet" href="finn-launcher-wallpaper.css">',
)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: py build_finn_launcher.py ORIGINAL_APPLICATION_ZIP"
        )

    source = Path(sys.argv[1]).resolve()
    output = ROOT.parent / "Finn-Launcher-Build" / "application.zip"
    temporary = output.with_suffix(".zip.tmp")

    if not source.is_file():
        raise SystemExit(f"Original TCL launcher ZIP not found: {source}")
    if source == output or source == temporary:
        raise SystemExit("The original ZIP must be separate from the build output.")

    missing = [name for name in ASSETS if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("Missing Finn Launcher files: " + ", ".join(missing))

    try:
        with ZipFile(source, "r") as original:
            names = original.namelist()
            if len(names) != len(set(names)):
                raise SystemExit("Unsupported launcher ZIP: duplicate entry names.")
            if any(name in names for name in ASSETS):
                raise SystemExit("Source ZIP already contains Finn Launcher files.")
            for required in ("dist/vendors.js", "index.html", "dist/app.bundle.js"):
                if required not in names:
                    raise SystemExit(f"Unsupported launcher ZIP: missing {required}.")

            vendors = original.read("dist/vendors.js")
            if vendors.count(OLD_BRIDGE) != 1:
                raise SystemExit("Unsupported TCL launcher: service bridge does not match exactly once.")
            patched_vendors = vendors.replace(OLD_BRIDGE, NEW_BRIDGE, 1)

            html = original.read("index.html").decode("utf-8")
            newline = "\r\n" if "\r\n" in html else "\n"
            insertion = ANCHOR + newline
            if html.count(insertion) != 1:
                raise SystemExit("Unsupported TCL launcher: HTML insertion point does not match exactly once.")
            patched_html = html.replace(
                insertion,
                insertion + newline.join(ADDITIONS) + newline,
                1,
            ).encode("utf-8")

            output.parent.mkdir(parents=True, exist_ok=True)
            with ZipFile(temporary, "w") as result:
                for entry in original.infolist():
                    data = original.read(entry.filename)
                    if entry.filename == "dist/vendors.js":
                        data = patched_vendors
                    elif entry.filename == "index.html":
                        data = patched_html
                    result.writestr(entry, data)
                for name in ASSETS:
                    result.write(ROOT / name, arcname=name, compress_type=ZIP_DEFLATED)

        with ZipFile(temporary, "r") as check:
            invalid = check.testzip()
            if invalid is not None:
                raise SystemExit(f"Built ZIP failed its integrity test: {invalid}")
        temporary.replace(output)
    except (BadZipFile, UnicodeDecodeError) as exc:
        raise SystemExit(f"Invalid or unsupported launcher ZIP: {exc}") from exc

    print("Finn Launcher build successful.")
    print("Output:", output)
    print("Original TCL files modified: 2")
    print("Finn Launcher files added:", len(ASSETS))
    print("No files were changed on the phone.")


if __name__ == "__main__":
    main()
