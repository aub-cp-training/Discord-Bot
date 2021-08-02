import json
from helper.cTime import MyDate
from cDatabase.DB_Session import DB_Session

config = json.load(open('config.json', 'r'))
database_session = DB_Session("db_session")

class Session:
    _date = MyDate()
    _id, duration, topic, desc, host = int(), int(), str(), str(), str()

    def __init__(self, date = "", duration = "", topic = "", host = "", desc = "", _id = -1):
        if _id == -1:
            description = desc.split(" ")
            description = description if "\"" == description[0][0] else ["\"" + x + "\"" for x in description]
            self._date = date
            self.duration = duration
            self.topic = topic if "[" == topic[0] else ("[" + topic + "]")
            self.host = host
            self.desc = "\n".join(description)
            self._id = len(database_session.db) + 1
        else:
            self._id = _id
            self.fill_values()

    def create(self): database_session.create(self)

    def delete(self): database_session.delete(self)

    def fill_values(self):
        info = database_session.get(self._id)
        self._date = info['date']
        self.duration = info['duration']
        self.topic = info['topic']
        self.host = info['host']
        self.desc = info['desc']

    def is_found(self): 
        for session in database_session.values():
            if (session['date'] == str(self._date) 
                and session['duration'] == self.duration 
                and session['topic'] == self.topic
                and session['host'] == self.host
                and session['desc'] == self.desc): return True
        return False

    def change(self, other): database_session.change(self, other)

    def __str__(self): return "ACM Session: " + self.topic + " | " + str(self.date)