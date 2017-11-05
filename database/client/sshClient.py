import paramiko


class Client:
    sshClient = None
    sshHost = None
    sshUser = None
    sshSecret = None
    sshPort = None

    def __init__(self, sshHost, sshPort, sshUser, sshSecret):
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshHost = sshHost
        self.sshUser = sshUser
        self.sshSecret = sshSecret
        self.sshPort = sshPort

    def run_comand(self, command):
        self.sshClient.connect(hostname=self.sshHost,
                               username=self.sshUser,
                               password=self.sshSecret,
                               port=self.sshPort)
        stdin, stdout, stderr = self.sshClient.exec_command(command)
        out = stdout.read()
        error = stderr.read()
        self.sshClient.close()
        if str(out) == 'b\'\'':
            return "ERROR", str(error)
        draft_response_str = str(out)
        return "OK", self.remove_unnecessary_symbols(draft_response_str)

    def remove_unnecessary_symbols(self, input_str):
        return input_str[3:input_str.__len__() - 3]
