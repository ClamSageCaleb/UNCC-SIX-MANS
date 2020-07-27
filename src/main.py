from bot.bot import main as botMain
from gui.gui import main as eelMain
from multiprocessing import Process

if __name__ == '__main__':
    p1 = Process(target=eelMain)
    p1.start()
    p2 = Process(target=botMain)
    p2.start()

    p1.join()
    p2.join()
