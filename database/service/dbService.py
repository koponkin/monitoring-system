from datetime import datetime, timedelta
from flask import current_app

from database.client import sshClient, dbClient
from database.dbMetric import DbMetric
from database.serverMetric import ServerMetric
from database.service.metricModel import MetricModel


class DbService:
    sshClient = None
    dbClient = None
    working_db = None

    def __init__(self, db, config):
        self.working_db = db
        self.sshClient = sshClient.Client(config['DB_INFO_SSH_HOST'],
                                          config['DB_INFO_SSH_PORT'],
                                          config['DB_INFO_SSH_USER'],
                                          config['DB_INFO_SSH_SECRET'])
        self.dbClient = dbClient.Client(
            config['DB_INFO_DB_HOST'],
            config['DB_INFO_DB_PORT'],
            config['DB_INFO_DB_NAME'],
            config['DB_INFO_DB_USER'],
            config['DB_INFO_DB_SECRET']
        )

    def get_metrics(self, period):
        from_time = datetime.now() - timedelta(minutes=period)
        result = []
        for model in self.working_db.session.query(MetricModel).filter(MetricModel.date > from_time).order_by(MetricModel.date.desc()):
            metric = ServerMetric(cpu=model.cpu, ram=model.ram)
            db_metric = DbMetric(metric, model.connection_count, model.date)
            result.append(db_metric)
        return result


    def get_metric_from_sevice(self):
        current_time = datetime.now()
        server_metrics = self.get_server_metrics()
        connections_count = self.dbClient.get_count_db_connections()
        return DbMetric(server_metrics, connections_count, current_time)

    def get_server_metrics(self):
        status, result = self.sshClient.run_comand('top -b -n 1 | grep postgres')
        if status == "OK":
            cpu, ram = self.parse_ssh_output_to_metric(result)
            return ServerMetric(cpu=cpu, ram=ram)
        return ServerMetric(error_text=result)

    def parse_ssh_output_to_metric(self, input_str):
        server_response_arr = input_str.split('\\n')
        full_cpy_usage = 0
        full_ram_usage = 0
        for server_response_row in server_response_arr:
            cpu, ram = self.parse_ssh_row(server_response_row)
            full_cpy_usage = full_cpy_usage + cpu
            full_ram_usage = full_ram_usage + ram
        return full_cpy_usage, full_ram_usage

    def parse_ssh_row(self, server_response_row):
        row_params = server_response_row.split("  ")
        return float(row_params[6]), float(row_params[7])

    def pickData(self):
        db_metric = self.get_metric_from_sevice()
        model = MetricModel(
            date=db_metric.date,
            connection_count=db_metric.connection_count,
            cpu=db_metric.cpu,
            ram=db_metric.ram,
            status=db_metric.status,
            error_text=db_metric.error_text
        )
        self.working_db.session.add(model)
        self.working_db.session.commit()
