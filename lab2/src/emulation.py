import random
from threading import Thread
from redisserv.redisserv import RedisServer
from faker import Faker
from stor.admin import AdminController
from menu import Menu


fake = Faker()

def emulation():
    fake = Faker()
    users_count = 5
    users = [fake.profile(fields=['username'], sex=None)['username'] for u in range(users_count)]
    threads = []
    try:
        for i in range(users_count):
            threads.append(EmulationController(users[i], users, users_count, random.randint(100, 5000)))
        for thread in threads:
            thread.start()
        AdminController()
        for thread in threads:
            if thread.is_alive():
                thread.stop()
    except Exception as e:
        Menu.show_error(str(e))


class EmulationController(Thread):
    def __init__(self, username, users_list, users_count, loop_count):
        Thread.__init__(self)
        self.quant_loop = loop_count
        self.serv = RedisServer()
        self.usrs_list = users_list
        self.users_quant = users_count
        self.serv.registration(username)
        self.usr_id = self.serv.sign_in(username)

    def run(self):
        while self.quant_loop > 0:
            message_text = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
            receiver = self.usrs_list[random.randint(0, self.users_quant - 1)]
            self.serv.create_message(message_text, receiver, self.usr_id)
            self.quant_loop -= 1

        self.stop()

    def stop(self):
        self.serv.sign_out(self.usr_id)
        self.quant_loop = 0
