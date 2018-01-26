import os
from netaddr import IPNetwork, IPAddress
# from app import db
# from app import *
# from app.models import User, AZS, RU, AZS_Type, DZO, Hardware, Status, Models_gate, Models_router, Region_mgmt

# test function
def test_function():
    # print(db)
    # from netaddr import IPNetwork, IPAddress
    print('>>> Scheduler - IS WORKING!')
    return '>>> Scheduler - IS WORKING!'

# get subnets from cisco-like backups
class Get_subnets():
    interfaces = {}
    hostname = ''


    def __init__(self, hostname):
        self.hostname = hostname

    def subnet_translate(self, s):
        if s == '255.255.255.252':
            return '/30'
        elif s == '255.255.255.248':
            return '/29'
        elif s == '255.255.255.240':
            return '/28'
        elif s == '255.255.255.224':
            return '/27'
        elif s == '255.255.255.192':
            return '/26'
        else:
            return '/32'

    def get_dict(self):
        try:
            # backups folder:
            backup_folder = '/home/makzzz/outside/backup/'
            gate_3k = False

            folders = []

            link = os.walk(backup_folder + self.hostname)
            for root, dirs, files in link:
                if dirs == []:
                    folders.append({'folder': root, 'created': os.path.getctime(root)})
            folders.sort(key=(lambda x: x['created']))

            # не найдена папка с бекапами
            if len(folders) > 0:
                folder_last = folders[-1]['folder']

                interfaces = {}
                with open(folder_last+'/running-config', 'r') as config_file:
                    next_line = False
                    temp_int = ''
                    subnet = ''
                    for line in config_file.readlines():
                        if next_line is True:
                            next_line = False
                            if line.startswith(' ip address'):
                                int_ip = line.split()[2]
                                int_mask = self.subnet_translate(line.split()[3])
                                interface = 'eth' + temp_int.split('/')[1]
                                interfaces[interface] = str(IPAddress(IPNetwork(int_ip+int_mask).cidr))

                                # if IPAddress(ip) in IPNetwork(int_ip+int_mask):
                                    # subnet = str(IPNetwork(int_ip+int_mask).cidr)
                                    # interface = 'eth' + temp_int.split('/')[1] + ' ' + subnet
                                    # break
                        if 'interface GigabitEthernet0' in line:
                            temp_int = line.split()[1]
                            next_line = True

                self.interfaces = interfaces
                return interfaces
        except Exception as e:
            print('Error:', e)

    def __repr__(self):
        return self.hostname


# a = Get_subnets('AZS-CHL-022-CSP-206')
# print(a)
# print(a.get_dict())
