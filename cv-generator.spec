# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

a = Analysis(
    ['desktop/cv-generator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('shared/templates', 'shared/templates'),
        ('shared/constants.py', 'shared'),
    ],
    hiddenimports=[
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL._tkinter_finder',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.styles',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.pdfgen',
        'jinja2',
        'pdfkit',
        'markdown2',
        'shared',
        'shared.constants',
        'shared.templates',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'tensorflow',
        'torch',
        'fastapi',
        'uvicorn',
        'redis',
        'sqlalchemy',
        'starlette',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CVGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='CVGenerator.app',
        icon=None,
        bundle_identifier='com.cvgenerator.app',
        info_plist={
            'CFBundleName': 'CV Generator',
            'CFBundleDisplayName': 'CV Generator',
            'CFBundleVersion': '1.0.2',
            'CFBundleShortVersionString': '1.0.2',
            'NSHighResolutionCapable': True,
        },
    )
