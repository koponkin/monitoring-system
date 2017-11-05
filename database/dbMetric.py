from flask import json


class DbMetric:
    connection_count = 0
    cpu = 0.0
    ram = 0.0
    status = "OK"
    error_text = ""
    date = None

    def __init__(self, server_metric, connection_count, date):
        self.connection_count = connection_count
        self.cpu = server_metric.cpu
        self.ram = server_metric.ram
        self.status = server_metric.status
        self.error_text = server_metric.error_text
        self.date = date

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        return {
            "connection_count": self.connection_count,
            "cpu": self.cpu,
            "ram": self.ram,
            "status": self.status,
            "error_text": self.error_text,
            "date": self.date
        }
