import shutil
import pathlib
import os
import argparse
import time
from colorama import Back, Fore, init
from distutils.dir_util import copy_tree

init()


def list_folder(path):
    folders = []
    files = []

    for path in pathlib.Path(path).iterdir():
        if path.is_file():
            files.append(path)

        else:
            folders.append(path)

    print(files)

    return folders, files


def folder_check(folder):
    return f'{folder}/' if not folder.endswith('/') else folder


def get_file_size(file_path):
    size = os.path.getsize(file_path)

    return str(round(size / 1024, 3)) +' kb'


def log(contents):
    context = '+' + '-' * 52 + '+'
    titles = 'Files And Folders', 'Size'
    context += f'\n| {Fore.RED}{titles[0]}{Fore.RESET}' + ' ' * (35 - len(titles[0])) + '| ' + Fore.RED + titles[1] + Fore.RESET + ' ' * (14 - len(titles[1])) + '|'
    context += '\n+' + '-' * 52 + '+'

    for text in contents:
        context += f'\n| {Fore.GREEN + text[0] + Fore.RESET}' + ' ' * (35 - len(text[0])) + '| ' + Fore.YELLOW + text[1] + Fore.RESET + ' ' * (14 - len(text[1])) + '|'

    context += '\n+' + '-' * 52 + '+'

    return context


def write_log(contents):
    context = '+' + '-' * 52 + '+'
    titles = 'Files And Folders', 'Size'
    context += f'\n| {titles[0]}' + ' ' * (35 - len(titles[0])) + '| ' + titles[1] + ' ' * (14 - len(titles[1])) + '|'
    context += '\n+' + '-' * 52 + '+'

    for text in contents:
        context += f'\n| {text[0]}' + ' ' * (35 - len(text[0])) + '| ' + text[1] + ' ' * (14 - len(text[1])) + '|'

    context += '\n+' + '-' * 52 + '+'

    with open(args.log_file, 'a') as f:
        f.write(f'SUCCESS\n{context}\n\n')


def backup():
    paths = args.paths.split(',')

    folders = []
    files = []
    log_info = []

    for path in paths:
        folder_contents = list_folder(path)

        if folder_contents[0]:
            folders.extend(folder_contents[0])

        if folder_contents[1]:
            files.extend(folder_contents[1])

    if not folders and not files:
        with open(args.log_file, 'a') as f:
            f.write('The source folder is empty. Exiting...\n')

        print(f'\n{Fore.RED}The source folder is empty. Exiting...{Fore.RESET}')

        os.abort()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    for folder in folders:
        shutil.copytree(folder, f'{folder_check(args.output)}{folder}', copy_function=shutil.copy2)

    for file in files:
        shutil.copy(file, folder_check(args.output))

        size = get_file_size(file)

        log_info.append((str(file), size))

    for folder in folders:
        size = get_file_size(folder)

        folder = f'{folder}/'

        log_info.append((str(folder), size))
    
    print(f'\n{Fore.GREEN}SUCCESS{Fore.RESET}')
    print(log(log_info))

    write_log(log_info)


args = argparse.ArgumentParser(description='VitBackup')
args.add_argument('-p', '--paths', required=False, default='.', help='Path(s) to folder(s) for backup (comma to separate)')
args.add_argument('-o', '--output', required=False, default='../backup', help='Path to output folder')
args.add_argument('-l', '--log-file', required=False, default='vitbackup.log', help='Path to log file')
args.add_argument('-t', '--time', required=False, default=30, type=int, help='Backup time interval (in seconds)')
args = args.parse_args()

try:
    while True:
        backup()

        time.sleep(args.time)
except KeyboardInterrupt:
    print(f'\n{Fore.RED}Exiting...{Fore.RESET}')

    os.abort()
