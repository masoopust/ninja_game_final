import os
import sys
import math
import random

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark

class Game:
    def __init__(self):
        pygame.init()                                                        #inicializace pygame

        pygame.display.set_caption('ninja game')                             #jméno okna
        self.screen = pygame.display.set_mode((640, 480))                    #souřadnice 0,0 jsou vlevo nahoře
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))                          # udělal jsem 2 display pro efektíky (aby se particly atd.. renderovaly před vše)

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = {                                                 # zpřístupnění daných obrázků, anamací apod...
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),     # animace trvá 6 framů
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),          #animace listu trvá 20 framů
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }
        
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),                # načtení sound efektů
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        
        self.sfx['ambience'].set_volume(0.2)                            # nastavení hlasitostí pro každý zvuk
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        
        self.clouds = Clouds(self.assets['clouds'], count=16)

        # HRÁČ
        self.player = Player(self, (50, 50), (8, 15))                       # spawne panáčka na pozici 50,50 o velikosti 8x15
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.level = 0
        self.load_level(self.level)    # načítá level podle proměnné
        
        self.screenshake = 0
        
    def load_level(self, map_id):        # načítá daný level
        self.tilemap.load('data/maps/' + str(map_id) + '.json')      # mění se jen číslo mapy
        
        self.leaf_spawners = []           # seznam spawnerů listů
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):  #projede každý strom, pro který se zjistí souřadnice a přidá mu spawner listů
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) # přidá spawner listu v zjištěných souřadnicích stromu ,díky fci extract(), o 4 pixely ho posune po obou osách
            
        self.enemies = []  # seznam enemáků (abych jich mohl mít více)
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):        # hledá pixelové souřadnice spawnerů(panáčka/enemáka daného v mapě) v mapách
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']     # spawne ninju na této pozici
                self.player.air_time = 0            # na zemi
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))  # pokud spawner NENÍ varianta 0 tj. ninja, spawne enemáka o velikosti 8,15
            
        self.projectiles = []            # seznamy pro projektily, particly a sparky
        self.particles = []
        self.sparks = []           # sparks 
        
        self.scroll = [0, 0]
        self.dead = 0                   #    bere smrt ninjy
        self.transition = -30
        
    def run(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)     # puštění soundů
        pygame.mixer.music.play(-1)
        
        self.sfx['ambience'].play(-1)
        
        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets['background'], (0, 0))                      # přidá se pozadí
            
            self.screenshake = max(0, self.screenshake - 1)
            
            if not len(self.enemies):    # když zabiju všechny enemáky
                self.transition += 1        # provede se transition
                if self.transition > 30:        # "zavře level černým screenem a otevře další"
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)   # načte další level, když je blackscreen
            if self.transition < 0:
                self.transition += 1
            
            if self.dead:    #  když ninja umře
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:  # po 40 framech se načte level znovu
                    self.load_level(self.level)
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30     # kamera se mi pohybuje s panáčkem (centruje ho na střed) osa X
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30    # kamera se mi pohybuje s panáčkem (centruje ho na střed) osa Y
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))                                              # kamera se bude pohybovat po celých číslech (int), nemůžu  řešit desetinná čísla
            
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:        # random.random je desetinné číslo 0-1 * 49999 způsobí, že se list nespawne každý frame, jakokdyby to tam nebylo
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)    # pozice spawnutí je někdě mezi 0-1 díky random.random()
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))   # velocity je rychlost padání frame je velikost listu
            
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():  # spawnuje enemáky do mapy
                kill = enemy.update(self.tilemap, (0, 0))  # když je kill True
                enemy.render(self.display, offset=render_scroll)
                if kill:  # pokud je enemák zabit odstraní se ze seznamu a není dále renderován
                    self.enemies.remove(enemy)
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))   # na ose Y je 0 protože platformer je zleva doprava a naopak
                self.player.render(self.display, offset=render_scroll)
            
            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]        # měním jen souřadnici X, Y se neměnní a měním ji směrem (direction), v tomto případě += projectile[1]
                projectile[2] += 1                       # timer + 1
                img = self.assets['projectile']         
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1])) # zobrazení střely
                if self.tilemap.solid_check(projectile[0]): # když narazí do zdi projektil zmizí
                    self.projectiles.remove(projectile)
                    for i in range(4):                       #  udělá 4 sparky
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))  # udělá spark (4), když střela narazí na zeď
                elif projectile[2] > 360:       # když projektil letí déle než 6s zmizí
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:     # když nejsem v prvních 50framech dashe (tj. jsem na cooldownu nebo normalně chodím, či skáču)
                    if self.player.rect().collidepoint(projectile[0]):    #  když střela zasáhne ninju
                        self.projectiles.remove(projectile)                         # odebere střelu
                        self.dead += 1          # ninjovy se započítá smrt a prevede vše, kde je DEAD
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):                              # udělá 30 sparků, když střela zasáhne ninju
                            angle = random.random() * math.pi * 2     # v náhodných úhlech a rychlostech
                            speed = random.random() * 5                 # a rychlostech
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                        
            for spark in self.sparks.copy():        # pro každý spark
                kill = spark.update()           # spark se updatne po killu a zmizí
                spark.render(self.display, offset=render_scroll)
                if kill:                             # a zmizí
                    self.sparks.remove(spark)
                    
            display_mask = pygame.mask.from_surface(self.display)           # maska se používá pro 2 barvy většinou bíla a černá
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))   # rozdílné barvy pro siluety a zbytek
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
                self.display_2.blit(display_sillhouette, offset)   # dělá lehké "stíny" a zvýrazní to frontend hry
            
            for particle in self.particles.copy():                                      
                kill = particle.update()                # voláme update a checkuji jestli nedopadl na zem ---> kill
                particle.render(self.display, offset=render_scroll)     
                if particle.type == 'leaf':            # když particle je list, tak list padá po "sinusovce"
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:    # jestli dopadl odstraní se
                    self.particles.remove(particle)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()                                    #nekonečný cyklus mi kontroluje zmačknutí křížku, popřípadě quitne hru
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:                   #kontroluje zmáčknutí left klávesy
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:                  #kontroluje zmáčknutí right klávesy
                        self.movement[1] = True
                    if event.key == pygame.K_UP:                     #kontroluje zmáčknuti šipky nahoru
                        if self.player.jump():                       # volá fci jump() (změna velocity natvrdo by byla infinity jump glitch) 
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:                      # kontroluje zmáčknutí Xka volá fci Dash
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:                  #kontroluje puštění left klávesy
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:                 #kontroluje puštění right klávesy
                        self.movement[1] = False
                        
            if self.transition:     # transition a nastavení černého kruhu 
                transition_surf = pygame.Surface(self.display.get_size())   
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))  #  transparentní bílá
                self.display.blit(transition_surf, (0, 0))
                
            self.display_2.blit(self.display, (0, 0))
            
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            pygame.display.update()             # update obrazovky
            self.clock.tick(60)                 # 60FPS    SELF--> pointer na třídu

Game().run()