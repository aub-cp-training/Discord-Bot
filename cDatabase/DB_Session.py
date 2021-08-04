import json
from cDatabase.KV_Database import KV_Database

config = json.load(open('config.json', 'r'))

class DB_Session(KV_Database):
    def __init__(self, path): 
        super().__init__(path)

    def create(self, session):
        session_id = max(list(self.db.keys()) + [0]) + 1
        self.db[session_id] = {
            'date': str(session._date), 
            'duration': session.duration,
            'topic': session.topic,
            'host': session.host,
            'desc': session.desc,
        }
        self.save()
        return session_id

    def delete(self, session):
        del(self.db[session._id])
        self.save()
        return True

    def change(self, session1, session2):
        session_id = session1._id
        self.db[session_id] = {
            'date': str(session2._date), 
            'duration': session2.duration,
            'topic': session2.topic,
            'host': session2.host,
            'desc': session2.desc,
        }
        self.save()