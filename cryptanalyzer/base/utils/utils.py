import platform
import subprocess


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
