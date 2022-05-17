import requests
import config
from pprint import pprint
import pydig
from influx_line_protocol import Metric, MetricCollection


class AVN_Metrics_Forwarder:
    def __init__(self, avn_token, project, service, dyna_token=None):
        self.aiven_token = avn_token
        self.dyna_token = dyna_token
        self.project = project
        self.service = service

    def get_avn_metrics(self):
        metrics_response = requests.post(
            config.AIVEN_URL.format(self.project, self.service),
            headers={'Authorization': 'aivenv1 {}'.format(self.aiven_token)},
            json={"period": "hour"})
        pprint(metrics_response.json())

    def get_prom_metrics(self, prom_config):
        SVC_IPS = pydig.query(prom_config["url"], 'A')
        pprint(SVC_IPS)
        for IP in SVC_IPS:
            response = requests.get(
                "https://{}:{}/metrics".format(IP, prom_config["port"]),
                auth=(prom_config['user'], prom_config['pass']),
                verify=False)
            self.parse_metrics(response.text.split('\n'))

    def put_dynatrace_metrics(self, metric):
        post_response = requests.post(
            config.DYNATRACE_URL,
            headers={"Authorization": "Api-Token {}".format(self.dyna_token)},
            data=metric)
        pprint(post_response)

    def parse_metrics(self, metrics):
        for line in metrics:
            if not line.startswith("#") and line.find("{") != -1:
                if line[:line.index("{")] in config.METRICS:
                    line = line.replace("host", "dt.entity.host")
                    line = line.replace("{", ",")
                    line = line.replace("}", "")
                    print(line)
                    self.put_dynatrace_metrics(line)


if __name__ == "__main__":
    a = AVN_Metrics_Forwarder(config.AIVEN_TOKEN, "dev-sandbox",
                              "mkos-kafka-dynatrace", config.DYNATRACE_TOKEN)
    # a.get_avn_metrics()
    a.get_prom_metrics(config.PROMETHEUS_CONFIG)
