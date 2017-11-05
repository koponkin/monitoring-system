from datetime import datetime, timedelta

from pingdom.client.api import Api
from pingdom.metric import CheckResult, Metric


class PingdomClient:
    def __init__(self, username, password, apikey, api_version='2.1'):
        """
        :param username: account main email
        :param password: account password
        :param apikey: Pingdom api key
        """
        self.username = username
        self.password = password
        self.apikey = apikey
        self.api = Api(username, password, apikey, api_version)
        self.checks = {}
        for item in self.api.send('get', "checks")['checks']:
            self.checks[item["name"].lower()] = item['id']

    def get_server_time(self):
        servertime_timestamp = self.api.send("get", "servertime")["servertime"]
        return datetime.fromtimestamp(servertime_timestamp)

    def get_metrics(self, from_timestamp):
        params = {"includeanalysis": "true", "from": from_timestamp}
        metrics_array = []
        for check_name, check_id in self.checks.items():
            check_response = self.api.send("get", "results", check_id, {}, params)['results']
            metrics_array.append({
                                    "check_name": check_name,
                                    "check_response": check_response
                                  })
        return metrics_array

