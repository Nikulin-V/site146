#  Nikulin Vasily © 2021
import datetime
from threading import Thread

from data import db_session
from data.scheduled_job import ScheduledJob
from tools.tools import safe_remove

models = {
}


class Scheduler(Thread):
    def __init__(self):
        super().__init__()
        self.works = False

    def run(self):
        self.works = True
        db_sess = db_session.create_session()
        for j in db_sess.query(ScheduledJob).all():
            j: ScheduledJob
            if (datetime.datetime.now() - j.datetime) > datetime.timedelta():
                db_sess.delete(j)
                db_sess.commit()
                Task(j).start()
        self.works = False


class Task(Thread):
    def __init__(self, job):
        Thread.__init__(self)
        self.job = job

    def delete_model(self):
        db_sess = db_session.create_session()
        model = db_sess.query(models[self.job.model]).get(str(self.job.object_id))
        if model is None:
            return False
        db_sess.delete(model)
        db_sess.commit()
        return True

    def delete_unused_picture(self):
        path = self.job.object_id
        return safe_remove(path)

    def run(self):
        result = 'Success'
        action = self.job.action
        model = self.job.model
        object_id = self.job.object_id
        if action == 'Delete':
            if not self.delete_model():
                result = 'Failed'
        elif action == 'Delete unused picture':
            if not self.delete_unused_picture():
                result = 'Failed'
        log = f'{datetime.datetime.now()}\t|\t{result.ljust(7, " ")}\t|\t' \
              f'{action.ljust(21, " ")}\t|\t{model.ljust(20, " ")}\t|\t{object_id}\n'
        f = open('logs.txt', 'a')
        f.write(log)
        f.close()
