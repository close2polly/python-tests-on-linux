import pytest
import subprocess
import string
import os

def run_command(command, text, punctuation_mode=False):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if process.returncode == 0 and not error:
        if punctuation_mode:
            words = output.decode().split()
            changedWords = [word.strip(string.punctuation) for word in words]
            return text in changedWords
        else:
            words = output.decode()
            return text in words
    return False


def test_list_files_True():
    assert run_command('ls', '1.py', True) == True

def test_list_files_False():
    assert run_command('ls', '1.py', True) == False

def test_7z_archive_zip():
    # Делалось на маке, есть только такой пакет
    # brew install p7zip
    assert run_command('7z a test.7z text1.txt', 'Everything is Ok') == True
    assert os.path.exists('./test.7z')

def test_7z_archive_unzip():
    assert run_command('7z x test.7z -aou', 'Everything is Ok') == True
    assert os.path.exists('./text1_1.txt')


# Не получилось поставить виртуальную машину, пишет что не поддерживается 
# Callee RC:
# VBOX_E_PLATFORM_ARCH_NOT_SUPPORTED (0x80bb0012)
# sudo apt install libarchive-zip-perl - неудалось поставить и протестить

pytest.main()




