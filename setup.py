import sys
from cx_Freeze import setup, Executable

setup(
    name="Squba",
    description='https://github.com/Sylph1de/Squba',
    version='0.5',
    url='https://github.com/Sylph1de/Squba',
    download_url='https://github.com/Sylph1de/Squba',
    author='Sylph1de',
    author_email='undefinedpietro@gmail.com',
    executables=[Executable(
        "main.py", base=None, target_name='sq', icon='Icon.ico')],
    options={
        'build_exe': {
            'include_files': ['Icon.ico']
        },
        'bdist_msi': {
            'upgrade_code': "{D5CD6E19-2545-32C7-A62A-4595B28BCDC3}",
            'add_to_path': True,
            'target_name': 'Squba',
            'install_icon': 'Icon.ico',
        }
    }
)
