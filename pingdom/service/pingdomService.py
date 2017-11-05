from datetime import datetime, timedelta

from pingdom.client.pingdomClient import PingdomClient
from pingdom.metric import CheckResult, Metric


class PingdomService:
    client = None

    def __init__(self, config):
        self.client = PingdomClient(
            config["PINGDOM_USERNAME"],
            config["PINGDOM_PASSWORD"],
            config["PINGDOM_APIKEY"]
        )

    def get_metrics(self, period):
        metrics = []
        from_time = datetime.now() - timedelta(minutes=period)
        from_timestamp = from_time.timestamp()
        server_response = self.client.get_metrics(from_timestamp)
        for response in server_response:
            check_results = []
            for metric in response['check_response']:
                responsetime = None
                if "responsetime" in metric:
                    responsetime = metric["responsetime"]
                result = CheckResult(metric["time"], metric["status"], responsetime, metric["statusdesc"])
                check_results.append(result)
            metrics.append(Metric(response['check_name'], check_results))
        return metrics