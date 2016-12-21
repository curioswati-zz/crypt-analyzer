import os
import platform
import subprocess

from django.conf import settings
from django.core.files import File

from .. import models


def get_system_config():
    sysconfig = {}

    os = platform.system()
    if os == "Linux":
        command = "cat /proc/cpuinfo"
        cpu_info = subprocess.check_output(command, shell=True).strip()

        if not type(cpu_info) == str:
            cpu_info = cpu_info.decode()

        clock_speed = cpu_info.split('@')[1].split(' ')[1].split('\n')[0]
        sysconfig['clock_speed'] = clock_speed

        cores = cpu_info.split('\n')[12].split(':')[1].strip()
        sysconfig['cpu'] = cores

        command = "cat /proc/meminfo"
        ram_info = subprocess.check_output(command, shell=True).strip()

        if not type(ram_info) == str:
            ram_info = ram_info.decode()

        ram_size = int(ram_info.split('\n')[0].split(':')[1].strip().split(' ')[0]) / 1024.0**2
        sysconfig['ram'] = ram_size

        sysconfig['architecture'] = platform.architecture()[0]

        return sysconfig


def save_encrypted_file(filename, content):
    '''
    saves the encrypted file to database.
    '''

    filename = settings.MEDIA_ROOT + '/files/' + filename
    with open(filename, 'wb+') as f:
        encrypted_file = File(f)
        encrypted_file.write(content)

        file_instance = models.EncryptedFile(name=filename,
                                             file_data=encrypted_file)
        file_instance.save()

    # remove the original file(before database upload) from filesystem
    os.remove(filename)

    return file_instance
