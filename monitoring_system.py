from flask import Flask, url_for, render_template, Response, request, json

from database.pickDbDataSheduller import PickDataScheduler
from database.service.dbService import DbService
from database.service.metricModel import db
from pingdom.service.pingdomService import PingdomService


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@192.168.0.104:5432/postgres"
    app.config.from_pyfile("config.cfg")
    db.init_app(app)
    db.app = app
    return app


app = create_app()

db_service = DbService(db, app.config)
pingdom_service = PingdomService(app.config)
pick_data_scheduler = PickDataScheduler(db_service)
pick_data_scheduler.run()


@app.route('/index')
def hello_index():
    return render_template("index.html")


@app.route('/db/monitor')
def hello_db_monitor():
    period = int(request.args.get('period', default=5))
    metrics = db_service.get_metrics(period)
    return Response(response=metrics_array_to_json(metrics),
                    status=200,
                    mimetype="application/json")


@app.route('/pingdom/monitor')
def pingdom_monitoring_data():
    period = int(request.args.get('period', default=5))
    metrics = pingdom_service.get_metrics(period)
    return Response(response=metrics_array_to_json(metrics),
                    status=200,
                    mimetype="application/json")


def metrics_array_to_json(metrics):
    return json.dumps([e.to_dic() for e in metrics])


with app.test_request_context():
    print(url_for('pingdom_monitoring_data'))

if __name__ == '__main__':
    app.run()
