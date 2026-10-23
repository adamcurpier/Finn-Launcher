# Finn Launcher

A minimalist, high-contrast home screen for the **TCL FLIP 4 5G** using the **Flipfull** launcher-overlay system.

Finn Launcher features monochrome Labrador artwork, a clock, and four simple menu entries: **Applications**, **Messages**, **Calendar**, and **Notes**. It is designed for physical-key navigation and a distraction-reduced phone experience.

> **Compatibility / status:** Developed and tested on a T-Mobile TCL FLIP 4 5G (model T4-4-0W, build `TCL/Gflip_5G_TMO:14/UKQ1.241125.001`) with Flipfull installed. The installer successfully reproduced every file and its contents from the Finn Launcher installation tested on the developer’s phone when run against the developer's original TCL launcher. **A fresh installation on a second phone has not yet been verified.** Other models, carriers, firmware versions, and launcher revisions may not be compatible.

## What it does

- Shows a minimal home-screen menu: Applications, Messages, Calendar, Notes.
- **Down:** cycle through menu entries.
- **Center/OK:** open the selected entry. Applications opens the TCL's native app list.
- **Up:** leave control to the native quick-settings action.
- **Right:** leave control to the native camera shortcut.
- **Left:** no custom action; existing system behavior is preserved.
- Displays a custom black-and-white Labrador wallpaper within the launcher.

The device's **system** wallpaper should also be set to the supplied solid-black image. This prevents the previous system wallpaper briefly appearing when returning to Finn Launcher. The black image is *not* automatically installed as the system wallpaper by the builder.

## Choose your calendar edition

Finn Launcher offers two editions with the same minimalist interface and keypad controls:

- **KaiOS Calendar (default):** Opens the TCL's built-in Calendar app.
- **Greg Calendar:** Opens the separately installed Greg Calendar app. Install Greg from KaiStore before choosing this edition. The tested device registers Greg at `http://greg.localhost/manifest.webmanifest`.

Build the original KaiOS Calendar edition:

```powershell
py .\build_finn_launcher.py ..\original-launcher.zip
```

Build the Greg Calendar edition:

```powershell
py .\build_finn_launcher.py ..\original-launcher.zip --greg
```

The two builds are saved separately in `..\Finn-Launcher-Build\application.zip` and `..\Finn-Launcher-Greg-Build\application.zip`. Both require the owner's compatible, unmodified TCL launcher ZIP.

**Notification-friendly layout:** Both editions position the four-item menu 78px above the bottom of the display. This preserves space beneath Notes for native missed-call and unread-message icons and their numeric counters. The layout was visually tested with and without notifications on the developer's TCL Flip 4 5G.

## Prerequisites

1. A compatible **TCL FLIP 4 5G** and a functioning **Flipfull** installation. Install Flipfull by following its own documentation first. This project **does not** install Flipfull or enable phone debugging/root access.
2. A computer with **Python 3** and **Android Platform Tools (ADB)** installed.
3. A working ADB connection with permission to run `adb root` on the device. Ensure USB debugging/developer access is set up according to your device's Flipfull instructions.
4. **Your own original, unmodified, compatible TCL launcher** `application.zip`. Do not build from an already-customized Finn Launcher image. This repository **does not provide TCL's original proprietary software**.
5. A verified backup of your original launcher saved **off the phone** before you install anything.

**Risk notice:** These steps replace the active launcher overlay on a modified phone. A mistake or incompatible firmware may leave the home screen unusable. Continue only if you are comfortable with ADB-based recovery. This is an independent community project, not affiliated with TCL, T-Mobile, KaiOS, or Flipfull.

## Repository files

| File | Purpose |
| --- | --- |
| `build_finn_launcher.py` | Builds a launcher ZIP from the owner's original TCL ZIP. Does not access the phone. |
| `finn-launcher.js` | Default edition: menu behavior and built-in KaiOS Calendar. |
| `finn-launcher-greg.js` | Alternative edition: same menu with Greg Calendar integration. |
| `finn-launcher.css` | Minimal text/menu styling. |
| `finn-launcher-wallpaper.css` | Displays the Finn artwork on the launcher background. |
| `Finn-Launcher-Wallpaper.png` | Monochrome Labrador home-screen artwork. |
| `Finn-Launcher-System-Black.png` | Solid-black image to choose as the phone's system wallpaper. |

This repository intentionally **does not** include the full modified `application.zip` because that would redistribute TCL's original app files.

## Build and install (Windows PowerShell example)

The following assumes that `adb` is on your PATH and that PowerShell is open in the repository directory. If ADB is installed elsewhere, substitute its full path (for example `C:\platform-tools\adb.exe`). Run **one command at a time** and inspect the output at each step.

### 1. Connect and verify your original launcher backup

```powershell
adb devices
adb root
adb shell id
Test-Path ..\original-launcher.zip
```

The `adb shell id` command should report `uid=0(root)`. The input ZIP must be a **verified, unmodified, compatible TCL launcher** preserved from your own installation. Do not assume the currently active overlay is original: it may already contain Finn Launcher or another customization. Never overwrite a known-good original backup with an unverified pull. Keep a separate copy of `original-launcher.zip` in a safe location off the phone. If the overlay location is absent, stop and consult Flipfull's documentation for your specific installation instead of guessing another path.

**Do not commit `original-launcher.zip` to GitHub.** It contains TCL software.

### 2. Build Finn Launcher

Choose the calendar edition you want to install.

**KaiOS Calendar (default):**

```powershell
py .\build_finn_launcher.py ..\original-launcher.zip
$buildPath = '..\Finn-Launcher-Build\application.zip'
```

**Greg Calendar (requires Greg installed from KaiStore):**

```powershell
py .\build_finn_launcher.py ..\original-launcher.zip --greg
$buildPath = '..\Finn-Launcher-Greg-Build\application.zip'
```

Use the selected `$buildPath` for the remaining installation steps.

The builder checks compatibility, rejects an already-customized source ZIP, and verifies ZIP integrity. If it reports an unsupported launcher, stop rather than bypassing its safety checks.

### 3. Verify the build before installing

```powershell
Get-FileHash $buildPath -Algorithm SHA256
```

Record the resulting SHA-256 digest; it will be specific to the generated package. The builder performs a ZIP integrity check as well.

### 4. Stage on the phone and compare checksums

```powershell
adb push $buildPath /data/local/userinit/overlays/launcher/application.zip.finn-stage
adb shell chmod 666 /data/local/userinit/overlays/launcher/application.zip.finn-stage
adb shell sha256sum /data/local/userinit/overlays/launcher/application.zip.finn-stage
```

**Do not proceed unless** the on-phone SHA-256 is identical to the hash reported for the build on your computer.

### 5. Activate Finn Launcher

```powershell
adb shell mv -f /data/local/userinit/overlays/launcher/application.zip.finn-stage /data/local/userinit/overlays/launcher/application.zip
adb shell sha256sum /data/local/userinit/overlays/launcher/application.zip
adb reboot
```

The installed filename **must** be `application.zip`; Finn Launcher is the name of the project, not the overlay filename. A full reboot is needed for Flipfull to load the replacement launcher. Confirm that the menu, clock, Applications list, Messages, Calendar, Notes, and native shortcuts work as expected.

### 6. Set the solid-black system wallpaper

1. Transfer `Finn-Launcher-System-Black.png` to the phone. On the tested device, **Windows Bluetooth File Transfer** worked (Windows Run dialog → `fsquirt`).
2. On the phone, open **Settings → Wallpaper → Gallery** and select the solid-black image as the **system wallpaper**.
3. Do **not** select `Finn-Launcher-Wallpaper.png` as the system wallpaper: Finn Launcher already displays that artwork internally. Selecting it a second time can produce a doubled image.
4. Keep the black image in Gallery; the phone also creates its own internal saved wallpaper copy.

## Recovery / rollback

**Before making changes, keep your original unmodified launcher ZIP on your computer.** If Finn Launcher does not load or breaks the home screen but ADB still works, reconnect and restore the original backup:

```powershell
adb root
adb shell id
Get-FileHash ..\original-launcher.zip -Algorithm SHA256
adb push ..\original-launcher.zip /data/local/userinit/overlays/launcher/application.zip.rollback-stage
adb shell chmod 666 /data/local/userinit/overlays/launcher/application.zip.rollback-stage
adb shell sha256sum /data/local/userinit/overlays/launcher/application.zip.rollback-stage
```

Verify that the staged SHA-256 matches the computer's backup before continuing. Only after the hashes match, activate the rollback and reboot:

```powershell
adb shell mv -f /data/local/userinit/overlays/launcher/application.zip.rollback-stage /data/local/userinit/overlays/launcher/application.zip
adb reboot
```

Confirm that the backup is the original TCL/Flipfull-compatible launcher before running those commands. If ADB is unavailable, use the recovery procedure documented for your specific Flipfull installation. Do not factory-reset as an automatic first troubleshooting step.

## Troubleshooting

- **Builder says unsupported launcher:** Stop. The input's TCL firmware or launcher code may differ from the tested build, or the input may already be modified. Do not blindly alter or bypass the compatibility checks.
- **No menu or broken Apps action:** Verify the correct Flipfull overlay path and that the staged file's SHA-256 matched the build. A full device reboot is required for activation. Roll back if in doubt.
- **Finn image appears twice:** You likely selected Finn's Labrador PNG as both system wallpaper and launcher artwork. Set the **system wallpaper** to `Finn-Launcher-System-Black.png` instead.
- **An old wallpaper briefly flashes:** Verify the solid-black system wallpaper is selected. A short restoration delay after exiting another app is normal on the tested phone.
- **`Permission denied` via ADB:** Recheck `adb root` and `adb shell id`. Root access may reset after a reboot.

## Development / licensing notes

The Python builder changes only two files in an owner-supplied TCL launcher: `dist/vendors.js` (a narrow bridge addition) and `index.html` (three references to Finn Launcher code and styles). It adds five independent Finn Launcher files and removes no original file. Development checks showed no missing, extra, or byte-different file *contents* compared with the verified working Finn Launcher reference after building with the developer's backup. ZIP metadata/compression may differ.

**Do not publish** the original or generated TCL `application.zip`, stock recovery ZIPs, or any other proprietary system app assets to the public repository. Only publish the standalone builder, custom files, and documentation. Review third-party dependencies and licenses before adding anything else.

This README describes the tested device and procedure; it is not a warranty of compatibility with every Flipfull or TCL firmware version.
