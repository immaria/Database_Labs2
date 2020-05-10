from threading import Thread
import datetime
import logging
import redis

class EventListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.r = redis.Redis(charset="utf-8", decode_responses=True)
        self.evnts = []

    def run(self):
        pubsub = self.r.pubsub()
        pubsub.subscribe(['users', 'spam'])
        for item in pubsub.listen():
            if item['type'] == 'message':
                message = " %s at '%s'" % (item['data'], datetime.datetime.now())
                self.evnts.append(message)
                logging.info(message)

    def get_events(self):
        return self.evnts
