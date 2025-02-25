from PyInstaller.utils.hooks import collect_submodules, collect_data_files, copy_metadata

hiddenimports = collect_submodules('filterpy')
datas = collect_data_files('filterpy')
datas += copy_metadata('filterpy')