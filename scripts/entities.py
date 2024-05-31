import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):        # inicializace + zpřístupnění
        self.game = game
        self.type = e_type
        self.pos = list(pos)                            # aby každa spawnutá entita měla vlastní list pro pozice
        self.size = size
        self.velocity = [0, 0]                          # velocity je o kolik se změnila poloha např. na ose x každý frame
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}   # definice jakým směrem padám
        
        self.action = ''
        self.anim_offset = (-3, -3)                     # "rezervuji" si 3 pixely na každou stranu pro např. animaci běhu, kdee panáček má nohy před sebou/za sebou
        self.flip = False                               # mám animace jen na 1 stranu, případně se zrcadlí "True"
        self.set_action('idle')                         # nese informaci, která animace zrovna běží
        
        self.last_movement = [0, 0]
    
    def rect(self):                                       # udělá obdelník se kterým můžeme mít kolizi kolize = obdelník narazí na obdelník
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])    
    
    def set_action(self, action):           # když se nová animace nerovná animaci právě běžící, tak ji přepíše a bude se provádět nová
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])   # o kolik se mi to actually posune sčítam např gravitaci(padá dolů) (velocity) + movement šipkama (doprava doleva)
        
        self.pos[0] += frame_movement[0]        # update pozice na ose X
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:       # pokud se pohybuju doprava
                    entity_rect.right = rect.left       # pravý obdelnik postavy narazí do  levého boku překážky
                    self.collisions['right'] = True
                if frame_movement[0] < 0:       # update pozice na ose Y
                    entity_rect.left = rect.right       # levý obdelnik postavy narazí do pravého boku překážky
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                
        if movement[0] > 0:                     # určuje jestli jdeme doleva, či doprava a podle toho flipuje animaci
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)           # max rychlost padání je 5, pokud je rychlost padání menší než 5, tak každý frame zrychlí o 0.1
        
        if self.collisions['down'] or self.collisions['up']:        # když se pohybuji po ose X chci velocity po ose Y 0
            self.velocity[1] = 0    
            
        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):    # render pro ninju (převážně animace)
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        #                              bere zrovna probíhající animaci, flipuje nám animaci dle pohybu

class Enemy(PhysicsEntity):                  # třída pro enemáka   má své vlastní animace
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)      #super().init bere init z před
        
        self.walking = 0
        
    def update(self, tilemap, movement=(0, 0)):           #update fce pro enemáky
        if self.walking:                                   # pokud enemák chodí:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):   #použije fci solid_check pro kontrolu okraje
                if (self.collisions['right'] or self.collisions['left']):   # otáčí všechny enemákovi animace podle toho na jakou stranu jde
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:    # enemák se zastaví a pak až vystřelí
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):  # pokud je ninja a enemák 16 pixelů od sebe na ose X a zároveň musí být na stejné souřadnici Y 
                    if (self.flip and dis[0] < 0):  # pokud je enemák natočen doleva a ninja je na levé straně od enemáka 
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0]) # vystřelí střelu doleva
                        for i in range(4): # udělá 4 sparky
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))  # udělá spark (4) za projektilem při střele doleva
                    if (not self.flip and dis[0] > 0):  # pokud je enemák natočen doprava a ninja je na pravé straně od enemáka 
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])  # vystřelí střelu doprava
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))        # udělá spark (4) za projektilem při střele doprava
        elif random.random() < 0.01:                    # pokud enemák stojí
            self.walking = random.randint(30, 120)      # nastaví jeho rychlost na 0,5-2x rychlost (protože 60fps)
        
        super().update(tilemap, movement=movement)
        
        if movement[0] != 0:    # pokud pohyb na ose X není 0 bude animace run
            self.set_action('run')
        else:                   # jinak je animace idle ---> stojíci enemák
            self.set_action('idle')     
            
        if abs(self.game.player.dashing) >= 50:                     # při dashi
            if self.rect().colliderect(self.game.player.rect()):    # když narazí ninja do enemáka
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                for i in range(30):                                   # udělá stejný efekt "exploze", jako když je ninja zastřelen
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True                                         # vrací True ----> všechny killy se mi provedou
            
    def render(self, surf, offset=(0, 0)):    # render pro enemy třídu
        super().render(surf, offset=offset)
        
        if self.flip:   # flipování zbraně podle enemáka 
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))          # posouvá zbraň o 4 pixely od panáčka

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1               # dává hráči 1 jump
        self.wall_slide = False
        self.dashing = 0
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        
        if self.air_time > 240:         # když přepadnu přes okraj resp. padám víc jak 240 framů, tak umřu a restart levelu
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1
        
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1  # přidá mi opět jump, jakmile se dotknu země
            
        self.wall_slide = False  # každý frame se mi automaticky nastaví na False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:     # pokud narazí levá či pravá strana hráče do zdi a zároveň je ve vzduchu provede se :
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)  # zpomaluje "klouzání" ninji po stěně
            if self.collisions['right']:    # kontroluje ze které strany je panáček na zdi, kvůli animaci
                self.flip = False
            else:                       # obrací animaci
                self.flip = True            
            self.set_action('wall_slide')
        
        if not self.wall_slide:              # zajišťuje, že se nepřepíše animace wall slidu, ikdyž splňuje níže uvedené podmínky pro animace 
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:            # pokud pohyb na ose X není 0 ---> animace RUN
                self.set_action('run')
            else:                             # jinak animace ----> idle
                self.set_action('idle')
        
        if abs(self.dashing) in {60, 50}:   # přidává particly na posledních 10 framů dashe
            for i in range(20):                                     # udělá 20x ----> 20 náhodných particlů
                angle = random.random() * math.pi * 2               # vypočítává úhly ve, kterých se kolem ninjy udělají particly
                speed = random.random() * 0.5 + 0.5                 # vypočítává náhodnou rychlost 20 particlů
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:    # zpomaluje dashování (stejné jako u jumpu)
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:        # zpomaluje dashování na druhou stranu
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:  # na posledních 10 framech dashe se mi ninja rychle zpomalí, avšak nestopne na místě
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:  # toto zároveň slouží jako cooldown na další dash, dokud nebude 60 bude stále "probíhat dash" a nezpustí se další viz. řádek č.228
                self.velocity[0] *= 0.1 
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]    # udává náhodná čísla pro místo spawnutí particlů
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))  # přidává mi "burst" pokud ninja dashuje
                
        if self.velocity[0] > 0:     # zpomaluje odraz od zdi (abych neskočil teoreticky do nekonečna)
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:                       # zpomaluje odraz od zdi (abych neskočil teoreticky do nekonečna)
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:    # když nejsme v posledních 10 framech dashe tak je ninja "neviditelný"
            super().render(surf, offset=offset)
            
    def jump(self):
        if self.wall_slide:       # wall slide jump
            if self.flip and self.last_movement[0] < 0:  # pokud narážim na zeď zleva a stále tam směřuji
                self.velocity[0] = 3.5              # odpíchne ninju od zdi doprava s rychlostí 3.5
                self.velocity[1] = -2.5             # odpíchne ninju nahoru od zdi o 2.5 (méně než jump, protože se odráží od zdi, ať to má "realný efekt")
                self.air_time = 5                    # update animace
                self.jumps = max(0, self.jumps - 1)     # wall jump funguje i s 0 jumpuma zbývajícíma (mohu vyskočit nahoru na zeď)
                return True
            elif not self.flip and self.last_movement[0] > 0:    # to stejné akorát dopava
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:        # jestli má hráč jump provede se
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5   # proměnnná, která změní animaci instantně
            return True
    
    def dash(self):
        if not self.dashing:                 # pokud ninja nedashuje už
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60     # 60 je jak dlouho bude dash probíhat a znamínko na jakou stranu (- doleva)
            else:
                self.dashing = 60       #  + doprava