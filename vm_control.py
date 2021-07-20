#
# control the VBox virtual machines from command line
#
import subprocess
import sys


class VMS():   

    def __init__(self):
        print("\t" + "="*28)
        if sys.platform.startswith('win'):
            self.base_cmd = 'C:/Program Files/Oracle/VirtualBox/VBoxManage.exe'
            self.pingopt = "-n"
            print("\t== vm-control for Windows ==")
        elif sys.platform.startswith('linux'):
            self.base_cmd = '/usr/bin/vboxmanage'
            self.pingopt = "-c"
            print("\t==  vm-control for Linux  ==")
        else:
            print('unable to determine platform')
            raise 'unknown'
        print("\t" + "="*28)

        # hold all the created VMs in VBox or
        # the current running VMs
        # it will repopulated based on user choice
        self.dict_vms = {}
        self.status = ""

    def getPingOpt(self):
        return self.pingopt

    def clear_state(self):
        self.dict_vms.clear()
        self.status = ""

    #
    # display VM name(s) on screen
    #
    def show_dict(self):        
        for k, v in self.dict_vms.items():
            print("\t{}  {}".format(k, v))


    def execute_vms(self, cmd, show_cmd=True, show_result=True):
        command = [self.base_cmd] + cmd
        if show_cmd:
            print("[=] executing: {}".format(command))

        p1 = subprocess.Popen(command,
                                stderr = subprocess.STDOUT,
                                stdout = subprocess.PIPE)
        out, err = p1.communicate()
        if not out:
            self.status = err
            print("[=] error: {}".format(self.status) )
            return False
        else:
            self.status = out.decode('utf-8')
            if show_result:
                print("[=] success: \n{}".format(self.status) )
            return True


    def process_output(self, out):
        self.dict_vms.clear()
        # cur_vms = out.splitlines()
        count = 0
        for v in out.splitlines():
            count = count + 1
            # print("line: {}".format(v))
            # fetching VM name and removing surrounding double-quotes
            value = v.split(' {')[0].replace('"', '')
            self.dict_vms[count] = value
        self.show_dict()


    def list_all(self):
        command = ["list", "vms"]
        if self.execute_vms(command, show_cmd=True, show_result=False):
            self.process_output(self.status)
        else:
            # this is error condition
            self.dict_vms.clear()


    def list_running(self):
        command = ["list", "runningvms"]
        if self.execute_vms(command, show_cmd=True, show_result=False):
            self.process_output(self.status)
        else:
            # this is error condition
            self.dict_vms.clear()


    def get_choices(self, all=False):
        self.list_all() if all else self.list_running()
        
        # validates the choices enter
        # it will ignore any invalid choice
        nokeys = len(self.dict_vms.keys())
        text = "enter input <0 to exit>: "
        choices = list(int(v) for v in input(text).split() if int(v) <= nokeys )
        return choices if 0 not in choices else []


    def start_vm(self):
        for i in self.get_choices(all=True):
            vms = self.dict_vms[i]
            choice = input("start \"{}\" headless <y/n> [y]: ".format(vms))
            print("starting {}".format(vms))

            cmd = ["startvm", vms, "--type"]
            if choice == '' or choice == 'y' or choice =='Y':
                cmd.append("headless")
            elif choice == 'n' or choice == 'N':
                cmd.append("separate")
            else:
                print("invalid option")
                return
            self.execute_vms(cmd)


    def save_vm(self):
        for i in self.get_choices(all=False):
            cmd = ['controlvm', self.dict_vms[i], 'savestate']
            self.execute_vms(cmd, show_cmd=True, show_result=True)


    def restart_vm(self):
        for i in self.get_choices(all=False):
            cmd = ['controlvm', self.dict_vms[i], 'reset']
            self.execute_vms(cmd, show_cmd=True, show_result=True)


def getIPv4(ip):
    ipdefault = ['192', '168', '56', 'x']
    # make sure 'ip' don't start with '.'
    # if it does then remove leading '.'
    if (len(ip) == 0):
        # if no IPv4 provided, then ping default gw
        # for-loop inside join (at return call) will do 192, 168, 56 and append ip ie '1'
        # which will make it '192.168.56.1' ie default gw for vbox installation.
        ip = '1'
    else:
        ip = ip if ip[0] != '.' else ip[1:]
    # since there are at most '3' dots in IPv4
    return '.'.join( [ ipdefault[x] for x in range(0, 3 - ip.count('.')) ] + [ip] )
    

def ping_test(pingopt, num = 6):
    # valid inputs will be with or without leading '.'
    # [[[192.]168.]56.]40
    # 40 or .40               will become 192.168.56.40
    # 50.40 or .50.40         will become 192.168.50.40
    # 100.56.40 or .100.56.40 will become 192.100.56.40
    # 172.100.21.40           will become 172.100.21.40

    # getIPv4 will return ip as string
    ip = getIPv4( input('enter IPv4: ') )
    print(f'sending {num} ping packets')
    command = ['ping', pingopt, str(num), ip]
    print(command)
    subprocess.run(command, stderr = sys.stdout, stdout = sys.stdout)
 

def display_menu():
    print("\t1  ping test")
    print("\t2  show running vms")
    print("\t3  start vms")
    print("\t4  --empty--")
    print('\t5  save vms')
    print('\t6  restart vm')
    print('\t0  exit')


if __name__ == "__main__":
    vms = VMS()
    while True:
        display_menu()
        choice = int(input("enter input: "))
        if choice == 1:
            ping_test(vms.getPingOpt())
        elif choice == 2:
            vms.list_running()
        elif choice == 3:
            vms.start_vm()
        elif choice == 4:
            pass
            #vms.save_all_running()
        elif choice == 5:
            vms.save_vm()
        elif choice == 6:
            vms.restart_vm()
        else:
            print("exiting...\n")
            break
        choice = 0
        print("\n\n")
        
# --end--
