import subprocess
import string

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


print(run_command('ls', '1.py', True))