import sys
from cx_Freeze import setup,Executable

exe = Executable(
        script  = 'snowball_fight.py',
        icon    = 'icns\\snowball.ico'
        )
includefiles    = ['snd\\',
                   'imgs\\',
                   'docs\\',
                   'fnts\\',
                   'player.py',
                   'level.py',
                   'projectile.py']
includes = []
excludes = []
packages = ['pygame']

setup(
    name        = 'Snowball Fight',
    version     = '0.1',
    description = 'null',
    options     = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [exe]
)
