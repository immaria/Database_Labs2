from src.stor.user import UserController
from src.stor.admin import AdminController
from src.stor.controller import Controller

menu_list = {
    'Main menu': {
        'Login to account': UserController.sign_in,
        'Create an account': UserController.registration,
        'Exit': Controller.stop_loop,
    },
    'User menu': {
        'Send a message': UserController.send_message,
        'Inbox messages': UserController.inbox_message,
        'My messages statistics': UserController.get_message_statistics,
        'Sign out': UserController.sign_out
    },
    'Admin menu': {
        'Online users': AdminController.get_online_users,
        'Events': AdminController.get_events,
        'Most senders': AdminController.get_top_senders,
        'Most spamers': AdminController.get_top_spamers,
        'Sign out': Controller.stop_loop,
    }
}

roles = {
    'utilizer': 'Utilizer menu',
    'admin': 'Admin menu'
}

special_parameters = {
    'role': '(admin or utilizer)'
}
