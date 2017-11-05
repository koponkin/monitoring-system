import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class PickDataScheduler:
    dbService = None

    def __init__(self, dbService):
        self.dbService = dbService

    def run(self):
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=self.pickData,
            trigger=IntervalTrigger(minutes=1),
            )
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

    def pickData(self):
        self.dbService.pickData()