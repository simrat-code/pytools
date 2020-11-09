#
# control the VBox virtual machines from command line
#
import subprocess
import sys


class VMS():   

    def __init__(self):  
        if sys.platform.startswith('win'):
            self.base_cmd = 'C:/Program Files/Oracle/VirtualBox/VBoxManage.exe'
        elif sys.platform.startswith('linux'):
            self.base_cmd = '/usr/bin/vboxmanage'
        else:
            print('unable to determine platform')
            raise 'unknown'
        self.dict_vms = {}
        self.status = ""


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


    def start_vms(self):
        self.list_all()
        vm_list = input("start vms <enter '0' to back>: ")
        if vm_list[0] == '0':
            return

        for i in vm_list.split(' '):
            num = int(i)
            vms = self.dict_vms[num]
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


    def save_all_running(self):
        # populate the dict with current running vms
        self.list_running()
        if not self.dict_vms:
            return
        for i, vms in self.dict_vms.items():
            print("[{}] saving: {}".format(i, vms))
            cmd = ["controlvm", vms, "savestate"]
            self.execute_vms(cmd)


    def save_vm(self):
        # show all currently running VMs
        self.list_running()
        choice = int(input("enter input <0 to exit>: "))
        if choice == 0:
            return
        cmd = ['controlvm', self.dict_vms[choice], 'savestate']
        self.execute_vms(cmd, show_cmd=True, show_result=True)


    def restart_vm(self):
        # show all currently running VMs
        self.list_running()
        choice = int(input("enter input <0 to exit>: "))
        if choice == 0:
            return
        cmd = ['controlvm', self.dict_vms[choice], 'reset']
        self.execute_vms(cmd, show_cmd=True, show_result=True)


def ping_test():
    ip = input('enter IPv4: ')
    command = ['ping', '-n', '1', ip]
    p1 = subprocess.Popen(command,
                            stderr = subprocess.STDOUT,
                            stdout = subprocess.PIPE)
    (out, err) = p1.communicate()
    if out:
        print(out.decode('utf-8'))
    else:
        print(err.decode('utf-8'))
 

def display_menu():
    print("\t1  ping test")
    print("\t2  show running vms")
    print("\t3  start vms")
    print("\t4  save all running vms")
    print('\t5  save vm')
    print('\t6  restart vm')
    print('\t0  exit')


if __name__ == "__main__":
    vms = VMS()
    while True:
        display_menu()
        choice = int(input("enter input: "))
        if choice == 1:
            ping_test()
        elif choice == 2:
            vms.list_running()
        elif choice == 3:
            vms.start_vms()
        elif choice == 4:
            vms.save_all_running()
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
