from src.stor.controller import Controller
from redisserv.listener import EventListener
from redisserv.redisserv import RedisServer
from menu import Menu


class AdminController(object):
    def __init__(self):
        self.serv = RedisServer()
        self.loop = True
        self.listnr = EventListener()
        self.listnr.start()
        self.start()

    def start(self):
        from data import menu_list
        try:
            menu = "Admin menu"
            while self.loop:
                choice = Controller.make_choice(menu_list[menu].keys(), menu)
                Controller.considering_choice(self, choice, list(menu_list[menu].values()))
        except Exception as e:
            Menu.show_error(str(e))


    def get_events(self):
        events = self.listnr.get_events()
        Menu.print_list("Events: ", events)

    def get_online_users(self):
        online_users = self.serv.get_online_users()
        Menu.print_list("Online users: ", online_users)

    def get_top_senders(self):
        top_senders = self.serv.get_top_senders(
            *Controller.get_func_arguments(self.serv.get_top_senders))
        Menu.print_list("Most senders: ", top_senders)

    def get_top_spamers(self):
        top_spamers = self.serv.get_top_spamers(
            *Controller.get_func_arguments(self.serv.get_top_spamers))
        Menu.print_list("Most spamers: ", top_spamers)