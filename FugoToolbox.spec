# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources'), ('plugins', 'plugins')],
    hiddenimports=['PySide6.QtPrintSupport', 'PySide6.QtSvg', 'PySide6.QtXml', 'openpyxl', 'xlrd', 'pandas', 'sqlite3', 'tkinter', 'tkinter.ttk', 'plotly', 'plotly.graph_objects', 'plotly.express', 'docx', 'pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.parsing', 'pandas._libs.tslibs.offsets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FugoToolbox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['E:\\VScode_project\\FugoTools\\resources\\icons\\favicon (1).ico'],
)
