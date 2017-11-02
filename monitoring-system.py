from flask import Flask, url_for, render_template, Response, request

from pingdom import pingdomClient

app = Flask(__name__)
app.config.from_pyfile("config.cfg")


@app.route('/index')
def hello_index():
    return render_template("index.html")


@app.route('/pingdom/monitor')
def pingdom_monitoring_data():
    period = int(request.args.get('period'))
    username = "koponkin@gmail.com"
    password = "qwerty"
    apikey = "54zbqho5xq6u1wwdzxluwq5dbew4b779"

    # username = app.config["username"]
    # password = app.config["password"]
    # apikey = app.config["apikey"]

    client = pingdomClient.PingdomClient(username, password, apikey)
    metrics = client.get_metrics(period)
    return Response(response=metrics_array_to_json(metrics),
                    status=200,
                    mimetype="application/json")


def metrics_array_to_json(metrics):
    return [e.to_json() for e in metrics][0]


with app.test_request_context():
    print(url_for('pingdom_monitoring_data'))

if __name__ == '__main__':
    app.run()
