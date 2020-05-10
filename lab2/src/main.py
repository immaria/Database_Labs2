from src.stor.controller import Controller
from src.stor.user import UserController
from  emulation import emulation

if __name__ == "__main__":
    choice = Controller.make_choice(["Main mode", "Emulation mode"], "Program menu")
    if choice == 0:
        UserController()
    elif choice == 1:
        emulation()
