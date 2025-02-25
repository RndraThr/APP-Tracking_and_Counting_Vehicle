# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('models/yolov8n.onnx', 'models'),
        ('assets/logo.png', 'assets'),
        ('assets/logo_sc.png', 'assets'),
        ('assets/icon.ico', 'assets')
    ],
    hiddenimports=[
        'filterpy',
        'filterpy.kalman',
        'filterpy.common',
        'filterpy.stats',
        'numpy.core._methods',
        'numpy.lib.format',
        'numpy.core',
        'numpy.random',
        'torch',
        'torchvision',
        'cv2',
        'PIL',
        'pymysql',
        'onnxruntime',
        'onnx'
    ],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartCounting',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SmartCounting',
)