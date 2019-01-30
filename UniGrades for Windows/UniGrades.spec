# -*- mode: python -*-

from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\main.py'],
             pathex=['C:\\Users\\antho\\Desktop\\UniGrades for Windows'],
             binaries=[],
             datas=[
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\home_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\create_schedule.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\schedule_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\course_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\assignment_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\course_view_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\category_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\category_edit_screen.kv', '.' ),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\schedules', 'schedules'),
('C:\\Users\\antho\\Desktop\\unigrades\\unigrades\\res', 'res')
],
             hiddenimports=['kivy.garden'],
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
          name='UniGrades',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe, Tree('C:\\Users\\antho\\Desktop\\unigrades\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
		    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='UniGrades')
