import pytest
import subprocess
import string
import datetime
import yaml


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



with open('config.yaml') as f:
    data = yaml.safe_load(f)


def get_stat_info():
    with open('stat.txt', 'a') as file:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        file_count = data['file_count']

        file_size = data['file_size']

        # на мак не нашла файла /proc/loadavg, но есть команда sysctl -n vm.loadavg
        process = subprocess.Popen('sysctl -n vm.loadavg', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        loadavg, error = process.communicate()

        stat_info = f'{current_time}, {file_count}, {file_size}  {loadavg}\n'

        file.write(stat_info)




@pytest.fixture(autouse=True)
def get_stat():
    get_stat_info()


def test_list_files_True(get_stat):
    assert run_command('ls', '1.py', True) == True

def test_list_files_False(get_stat):
    assert run_command('ls', '1.py', True) == False