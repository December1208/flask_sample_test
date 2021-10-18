import sqlalchemy
from flask_sample_test.sample_data import SampleEnvironment


class SampleTest(object):
    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db
        self.inspector = None
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        self.db = db or self.db
        self.inspector = sqlalchemy.inspect(db.engine)
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['flask_sample_test'] = self

    def create_env(self, sample_data_list):
        return SampleEnvironment(db=self.db, sample_data_list=sample_data_list)
