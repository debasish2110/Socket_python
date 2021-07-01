"""
File: sample ssh test
Owner: SYS
Copyright: (c) LTTS
"""
#importing modules

import os
import sys
import time
import socket
from ssh2.session import Session
import paramiko

# CONSTANTS / GLOBALS
# HOST = '192.168.29.200' #ip of raspberry pi of instructor
HOST = 'localhost'
PORT = 22
USER = 'hero'    # instructor set user name in the ubuntu 20.04 installed in raspberry pi
#USER = os.getlogin()
PASSWORD = '2110'

# class defination of ssh channel creation
class Ssh_session():
    """
        [summary: class definition]
    """

    _class_var = None

    def __init__(self, host, user, port, password):
        """
        [summary: constructor]
        Args:
            host ([type]): [description]
            user ([type]): [description]
            port ([type]): [description]
            password ([type]): [description]
        """
        self._host = host   #private variable
        self._user = user
        self._port = port
        self._password = password
        self.channel = None  #non private
        self.session = None
    # End of constructor

    def get_channel(self):
        """
        [summary:]
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._host, self._port))

        self.session = Session()
        self.session.handshake(sock)
        self.session.userauth_password(self._user, self._password)
        self.channel = self.session.open_session()
    # End of Function get_channel

    def execute_cmd(self, cmd):
        """[summary: executes remote command]
        Args:
            cmd ([type]): [description]
        """
        size = 0
        data_list = []
        self.channel.execute(cmd)
        s, d = self.channel.read()
        size += s
        data_list.append(d)

        while s > 0:
            s, d = self.channel.read()
            size += s
            data_list.append(d)
        return size, data_list
    # End of function

    def __del__(self):
        """
        [summary: Destroctor]
        """
        #self.channel.close()
        #print("Exit Status: %s" % self.channel.get_exit_status())
        pass
    # End of destroctor
# End of Class


# creating paramiko class
class ssh_paramiko(Ssh_session):
    """
    [New class for ssh using paramiko]
    """
    def __init__(self, host, user, port, password):
        super().__init__(host, user, port, password)  # const of parent class
        self.ssh = None
    # End of const
    
    def paramiko_client(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self._host, self._port, self._user, self._password)

    def paramiko_execute_cmd(self, cmd):
        std_in, std_out, std_err = self.ssh.exec_command(cmd)
        lines = std_out.readlines()
        return lines
    # end of function
# end of class


if __name__ == "__main__":
    ssh_ses_obj = ssh_paramiko(HOST, USER, PORT, PASSWORD) #creating obj
    ssh_ses_obj.get_channel() #creating the channel
    # sending command
    cmd = 'vmstat; ping -c 5 192.168.29.169; exit 0;'
    size, data = ssh_ses_obj.execute_cmd(cmd)

    ssh_ses_obj.paramiko_client()
    data_p = ssh_ses_obj.paramiko_execute_cmd(cmd)
    ssh_ses_obj.channel.close()
    print("Received Size: {} and Data: {}".format(size, data))
    print("paramiko op:", data)
    print("Exit Status: %s" % ssh_ses_obj.channel.get_exit_status())
    sys.exit(0)