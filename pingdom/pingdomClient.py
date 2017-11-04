from datetime import datetime, timedelta, timezone

from pingdom.api import Api
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

    def get_metrics(self, period):
        metrics = []
        from_time = datetime.now() - timedelta(minutes=period)
        from_timestamp = from_time.timestamp();
        params = {"includeanalysis": "true", "from": from_timestamp}
        for check_name, check_id in self.checks.items():

            result_response = self.api.send("get", "results", check_id, {}, params)['results']
            check_results = []
            for metric in result_response:
                responsetime = None
                if "responsetime" in metric:
                    responsetime = metric["responsetime"]
                result = CheckResult(metric["time"], metric["status"], responsetime, metric["statusdesc"])
                check_results.append(result)
            metrics.append(Metric(check_name, check_results))

        return metrics

