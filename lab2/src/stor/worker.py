import random
import time
from threading import Thread
import redis
from menu import Menu
class Worker(Thread):

    def __init__(self, delay):
        Thread.__init__(self)
        self.lp = True
        self.re = redis.Redis(charset="utf-8", decode_responses=True)
        self.delay = delay

    def run(self):
        while self.lp:
            message = self.re.brpop("queue:")
            if message:
                message_id = int(message[1])

                self.re.hmset(f"message:{message_id}", {
                    'status': 'checking'
                })
                message = self.re.hmget(f"message:{message_id}", ["sender_id", "receiver_id"])
                sender_id = int(message[0])
                receiver_id = int(message[1])
                self.re.hincrby(f"user:{sender_id}", "queue", -1)
                self.re.hincrby(f"user:{sender_id}", "checking", 1)
                time.sleep(self.delay)
                is_spam = random.random() > 0.6
                pipeline = self.re.pipeline(True)
                pipeline.hincrby(f"user:{sender_id}", "checking", -1)
                if is_spam:
                    sender_username = self.re.hmget(f"user:{sender_id}", 'login')[0]
                    pipeline.zincrby("spam:", 1, f"user:{sender_username}")
                    pipeline.hmset(f"message:{message_id}", {
                        'status': 'blocked'
                    })
                    pipeline.hincrby(f"user:{sender_id}", "blocked", 1)
                    pipeline.publish('spam', f"User {sender_username} sent spam message: \"%s\"" %
                                     self.re.hmget("message:%s" % message_id, ["text"])[0])
                    print(f"User {sender_username} sent spam message: \"%s\"" % self.re.hmget("message:%s" % message_id, ["text"])[0])
                else:
                    pipeline.hmset(f"message:{message_id}", {
                        'status': 'sent'
                    })
                    pipeline.hincrby(f"user:{sender_id}", "sent", 1)
                    pipeline.sadd(f"sent to:{receiver_id}", message_id)
                pipeline.execute()

    def stop(self):
        self.lp = False


if __name__ == '__main__':
    try:
        loop = True
        workers_count = 5
        workers = []
        for x in range(workers_count):
            worker = Worker(random.randint(0, 3))
            worker.setDaemon(True)
            workers.append(worker)
            worker.start()
        while True:
            pass
    except Exception as e:
        Menu.show_error(str(e))
