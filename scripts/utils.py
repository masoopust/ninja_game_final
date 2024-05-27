import os

import pygame

BASE_IMG_PATH = 'data/images/'      # zkratka abych nemusel vypisovat pokaždé celou cestu

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))         # černé pozadí se stane transparentní
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):      # os.listdir vezme cestu o vezme všechny soubory co jsou na té cestě
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:        # class animation se stará o animace
    def __init__(self, images, img_dur=5, loop=True):       #img_dur je jak dlouho (kolik framu se ukaže danimace
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0                                      # díky této proměnné víme, v jaké fázi animace jsme

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop) # pro všechny animace máme tyto proměnnné proto zavádíme fci copy(), abychom to nemuseli furt vypisovat
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))  # díky modulu to krásně loopuje a navazuje na sebe
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)  # vezme menší hodnotu a podle ní nastaví animaci. -1 máme protože to vybírá z listu a první pozice v listu je 0
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True        # animace skončí
    
    def img(self):       # vrací hodnotu podle které se vybírá jaká animace se vyrenderuje
        return self.images[int(self.frame / self.img_duration)]