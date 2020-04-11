# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['c:/Users/patri/Desktop/BIT Term 5/ADEV-3005 Programming in Python/Code/Final_Project/Weather_Processing_App/weather_gui.py'],
             pathex=['C:\\Users\\patri\\Desktop\\BIT Term 5\\ADEV-3005 Programming in Python\\Code\\Final_Project\\Weather_Processing_App'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='weather_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='weather_gui')
