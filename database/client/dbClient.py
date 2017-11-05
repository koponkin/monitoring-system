from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


class Client:
    db_engine = None

    def __init__(self, host, port, dbName, user, secret):
        db_url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            user,
            secret,
            host,
            port,
            dbName
        )
        self.db_engine = create_engine(db_url)

    def get_count_db_connections(self):
        connection = self.db_engine.connect()
        count_included_current_select = connection.execute("SELECT count(*) FROM pg_stat_activity").scalar()
        connection.close()
        return count_included_current_select - 1
