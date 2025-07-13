# hook-dlib.py
from PyInstaller.utils.hooks import collect_all

def hook(hook_api):
    datas, binaries, hiddenimports = collect_all('dlib')
    hook_api.add_datas(datas)
    hook_api.add_binaries(binaries)
    hook_api.add_imports(*hiddenimports)