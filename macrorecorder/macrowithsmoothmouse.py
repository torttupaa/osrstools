import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener, KeyCode
from pynput.keyboard import Controller as ctrl
import random
import pyautogui as pg


delay = 0.8 #staattinen
rnd_add_mult = 7 #klikkaus osuma alueen koko +- PX

button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')
map_key = KeyCode(char='m')
map_key_drop = KeyCode(char='n')
curse_key = KeyCode(char='a')
drop_key = KeyCode(char='z')
pause_key = KeyCode(char='p')



class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
        self.autocurse = False
        self.autodrop = False
        self.Pause = False
        self.maplist_curse = []
        self.maplist_drop = []


    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def mapper_curse(self):
        self.maplist_curse.append(mouse.position)

    def mapper_drop(self):
        self.maplist_drop.append(mouse.position)

    def auto_curse(self):
        self.autocurse = True

    def auto_curse_stop(self):
        self.autocurse = False

    def auto_drop(self):
        self.autodrop = True

    def pause(self):
        self.Pause = True

    def unpause(self):
        self.Pause = False


    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def gen_mouse_path(self,new_pos, last_pos, del_lay):

        xS = []
        yS = []

        checkpoints = 5 #montako random välipistettä hiiren liikeradalla
        time_div_ratio = 5 #kuinka paljon nopeemmin hiiri liikkuu keskvaiheen kun paadyt

        k = (new_pos[1] - last_pos[1]) / (new_pos[0] - last_pos[0])

        if new_pos[0] > last_pos[0]:
            for i in range(checkpoints):
                xS.append(random.randint(last_pos[0], new_pos[0]) + random.randint(0, rnd_add_mult * 2) - rnd_add_mult)
            xS.sort()
        else:
            for i in range(checkpoints):
                xS.append(random.randint(new_pos[0], last_pos[0]) + random.randint(0, rnd_add_mult * 2) - rnd_add_mult)
            xS.sort(reverse=True)

        viime_x = last_pos[0]
        viime_y = last_pos[1]

        for x in xS:
            y = int((k * (x - viime_x)) + viime_y)
            yS.append(y)
            viime_x = x
            viime_y = y

        xS.append(new_pos[0])
        yS.append(new_pos[1])

        paadyt_time = del_lay / time_div_ratio
        keskiaika = del_lay - paadyt_time


        keskiaikasteppi = paadyt_time/2
        paatysteppi = keskiaika / (checkpoints - 1)


        masterlista = []

        for dick in range(len(xS)):
            masterlista.append([xS[dick], yS[dick], keskiaikasteppi])

        masterlista[0][2] = paatysteppi
        masterlista[-1][2] = paatysteppi
        return masterlista

    def run(self):
        viime_koordi = mouse.position
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay+((random.randint(0,20))/100))

            if self.autocurse:
                try:
                    for koord in self.maplist_curse:
                        rand_koord = (koord[0]+random.randint(0,rnd_add_mult*2)-rnd_add_mult,koord[1]+random.randint(0,rnd_add_mult*2)-rnd_add_mult)
                        movelist = self.gen_mouse_path(rand_koord, viime_koordi, (self.delay+((random.randint(0,20))/100)))
                        for osa in movelist:
                            pg.moveTo(osa[0],osa[1],osa[2])
                        mouse.click(self.button)
                        #print(mouse.position)
                        viime_koordi = rand_koord
                except:
                    pass

                #self.autodrop = False
            if self.autodrop:
                mouse.position = self.maplist_drop[0]
                mouse.click(self.button)
                time.sleep(0.2)
                with keyboard.pressed(Key.shift):
                    for koord in self.maplist_drop:
                        if koord != self.maplist_drop[0]:
                            mouse.position = koord
                            mouse.click(self.button)
                            time.sleep(0.2)
                self.autodrop = False
                self.autocurse = False

            while self.Pause:
                time.sleep(0.2)

            time.sleep(0.1)

keyboard = ctrl()
mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()

    elif key == map_key:
        click_thread.mapper_curse()

    elif key == map_key_drop:
        click_thread.mapper_drop()

    elif key == curse_key:
        print(click_thread.maplist_curse)
        if click_thread.autocurse:
            click_thread.auto_curse_stop()
        else:
            click_thread.auto_curse()

    elif key == drop_key:
        click_thread.auto_drop()

    elif key == pause_key:
        if click_thread.Pause:
            click_thread.unpause()
        else:
            click_thread.pause()


with Listener(on_press=on_press) as listener:
    listener.join()
