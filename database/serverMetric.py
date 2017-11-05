class ServerMetric:
    cpu = 0.0
    ram = 0.0
    status = "OK"
    error_text = ""

    def __init__(self, cpu=None, ram=None, error_text=""):
        self.cpu = cpu
        self.ram = ram
        if error_text != "":
            self.error_text = error_text
            self.status = "ERROR"
