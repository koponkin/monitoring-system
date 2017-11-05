from datetime import datetime

from flask import json


class Metric:
    service_name = ""
    check_results = []

    def __init__(self, service_name, check_results):
        self.service_name = service_name
        self.check_results = check_results

    def to_json(self):
        return json.dumps({"service_name": self.service_name,
                    "results": [e.to_dic() for e in self.check_results]})

    def to_dic(self):
        return {
                    "service_name": self.service_name,
                    "results": [e.to_dic() for e in self.check_results]
                }


class CheckResult:
    date = None
    status = "up"
    responsetime = 0
    statusdesc = "OK"

    def __init__(self, timestamp, status, responsetime, statusdesc):
        self.date = datetime.fromtimestamp(timestamp)
        self.status = status
        self.responsetime = responsetime
        self.statusdesc = statusdesc

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        return {"date": self.date,
                "status": self.status,
                "responsetime": self.responsetime,
                "statusdesc": self.statusdesc}

