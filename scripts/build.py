#!/usr/bin/env python3
"""Build CV Generator executable using PyInstaller."""
import subprocess
import sys
import os
import platform
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
SPEC_FILE = os.path.join(ROOT_DIR, "cv-generator.spec")


def clean():
    for d in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"Cleaned {d}")


def build():
    print(f"Building on {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Root: {ROOT_DIR}")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--distpath",
        DIST_DIR,
        "--workpath",
        BUILD_DIR,
        SPEC_FILE,
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    if result.returncode != 0:
        print(f"Build failed with code {result.returncode}")
        sys.exit(result.returncode)

    print(f"\nBuild complete! Output in {DIST_DIR}")

    executable_name = "CVGenerator"
    if platform.system() == "Windows":
        executable_name += ".exe"

    exe_path = os.path.join(DIST_DIR, executable_name)
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"Executable: {exe_path} ({size_mb:.1f} MB)")
    elif platform.system() == "Darwin":
        app_path = os.path.join(DIST_DIR, "CVGenerator.app")
        if os.path.exists(app_path):
            print(f"App bundle: {app_path}")
        else:
            print("WARNING: No output found")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
    else:
        clean()
        build()
