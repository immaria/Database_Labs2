import colorama
from colorama import Fore
import atexit
from stor.controller import Controller

from menu import Menu
from redisserv.redisserv import RedisServer


class UserController(object):
    def __init__(self):
        self.serv = RedisServer()
        self.menu = 'Main menu'
        self.curr_user_id = -1
        self.loop = True
        atexit.register(self.sign_out)
        self.start()

    def start(self):
        from data import menu_list
        try:
            while self.loop:
                choice = Controller.make_choice(menu_list[self.menu].keys(), self.menu)
                Controller.considering_choice(self, choice, list(menu_list[self.menu].values()))

        except Exception as e:
            Menu.show_error(str(e))

    def registration(self):
        usernmm=self.serv.registration(*Controller.get_func_arguments(self.serv.registration))
        colorama.init()
        print(Fore.GREEN + "\n Congratulations!\n You have been successfully\n registered) " + Fore.RESET)

    def sign_in(self):
        user_id = self.serv.sign_in(*Controller.get_func_arguments(self.serv.sign_in))
        self.curr_user_id = user_id
        self.menu = 'User menu'
        print(Fore.GREEN + f"\n Good to see you again! " + Fore.RESET)
    def inbox_message(self):
        messages = self.serv.get_messages(self.curr_user_id)
        Menu.print_list("-" * 30 + "\n My messages: ", messages)

    def get_message_statistics(self):
        statistics = self.serv.get_message_statistics(self.curr_user_id)
        Menu.show_item(statistics)

    def sign_out(self):
        if self.curr_user_id != -1:
            self.serv.sign_out(self.curr_user_id)
            self.menu = 'Main menu'
            self.curr_user_id = -1

    def send_message(self):
        self.serv.create_message(*Controller.get_func_arguments(self.serv.create_message, 1),
                                           self.curr_user_id)


