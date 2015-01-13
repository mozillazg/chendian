# -*- mode: python -*-
a = Analysis(['parser.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='chendian.exe',
          debug=False,
          strip=None,
          upx=True,
          # console=True,
          # version='version.txt',
          icon='icon.ico'
          )
