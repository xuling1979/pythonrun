# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# 获取 Python 环境中的 tcl/tk 路径
python_path = sys.prefix
tcl_lib = os.path.join(python_path, 'tcl')
tk_lib = os.path.join(python_path, 'tk')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        # 手动添加 tcl/tk 动态库
        ('tcl86t.dll', os.path.join(tcl_lib, 'tcl86t.dll'), 'tcl'),
        ('tk86t.dll', os.path.join(tk_lib, 'tk86t.dll'), 'tk'),
    ],
    datas=[
        # 添加 tcl/tk 库文件
        (tcl_lib, 'tcl'),
        (tk_lib, 'tk'),
    ],
    hiddenimports=[
        'tkinter',
        '_tkinter',
    ],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 改为 False 以便显示窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
