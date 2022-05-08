import re
from unittest import result
from netmiko import ConnectHandler
from paramiko import RSAKey
from setuptools import Command

def loopbackConfig(params,delete=False):
    """"""
    Command = "int loopback 62070085"
    if delete:
        Command = "no int loopback 62070085"
    with ConnectHandler(**params) as ssh:
        result = ssh.send_command("show ip int br | include Loop")
        if len(result) == 0 and delete == False:
            ssh.send_config_set([Command,"ip address 192.168.1.1 255.255.255.0","no shut"])
        result = ssh.send_command("show ip int br | include Loop")
    print(result)

device_ip = "10.0.15.102"
username = "admin"
key_file = "id_rsa.pub"
# key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

device_params = {"device_type": "cisco_ios",
                "ip": device_ip,
                "username": username,
                "password": "cisco",
                "use_keys": False,
                "key_file": key_file
                }

loopbackConfig(device_params)
