import paramiko
import pytest
import yaml


def ssh_checkout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    print(out)
    client.close()
    if text in out and exit_code == 0:
        return True
    else:
        return False


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"{local_path} in {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_files(host, user, passwd, remote_path, local_path, port=22):
    print(f"{remote_path} in {local_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "1111", "p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "1111", "echo '1111' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "1111", "echo '1111' | sudo -S dpkg -s p7zip-full", "Status: install ok installed"))
    return all(res)


with open('config.yaml') as f:
    config = yaml.safe_load(f)

def test_for_command_true():
    # Как я поняла должна показываться папка /home/user2
    # в ней должен лежать уже p7zip-full.deb который мы клали удалено
    # значит ls должен вернуть что он там
    # сервер уц меня так и не установился, проверить не могу, но надеюсь логика такая
    # на мак сервер что-то уж очень замедрено ставится и не поднимается
    answer = ssh_checkout("0.0.0.0", str(config['username']), str(config['password']), "ls -l", 'p7zip-full.deb')
    assert answer == True

def test_for_command_false():
    # Этого файла там быть недолжо по логике
    # ничего сложение не придумывается
    answer = ssh_checkout("0.0.0.0", str(config['username']), str(config['password']), "ls -l", 'unkwonw.txt')
    assert answer == True


# test_for_command_true()
# if deploy():
#     print("OK!")
# else:
#     print("NOT OK")


pytest.main()