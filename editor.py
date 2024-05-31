import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners'),
        }
        
        self.movement = [False, False, False, False]    # pro pohyb kamery místo ninji
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]             # chceme mít zaplý scroll 
        
        self.tile_list = list(self.assets)     # vyberu všechny assets ---> decor, grass,...
        self.tile_group = 0                    # určuje s čím zrovna pracuji (grass nebo decor nebo stone nebo ...)
        self.tile_variant = 0                  # určuje s čím přesně zrovna pracuji (grass1 nebo grass2 nebo..)

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))        # černé pozadí pro přehlednost
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2     # pohyb kamerou na ose X   pomoci wasd
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2     # pohyb kamerou na ose Y
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)      # renderuje nám mapu
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()     # ukazuje nám, který tile zrovna máme
            current_tile_img.set_alpha(100)                                                  # nastáví tile na skoro transparentní   
            
            mpos = pygame.mouse.get_pos()         # dává souřadnice kurzoru myši
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)
            
            if self.clicking and self.ongrid:       # podmínka pro přidání "tile" na mapu 
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
                # vybírá a pamatuje si :    X souřadnici            Y souřadnici     typ                                      variantu
            if self.right_clicking:                                                          # pokud zmáčknu pravé tlačítko ....
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]                                      # smažu "tile" na kterém mám kurzor myši
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
            
            self.display.blit(current_tile_img, (5, 5))    # zobrazuje aktualně vybraný "tile" o velikosti 5 a 5
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:        # konrtoluje zmačknuti tlačítka myši
                    if event.button == 1:                        # 1 je levé tl. myši
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:               # 3 je pravé tl. myši  (2 je kolečko)
                        self.right_clicking = True
                    if self.shift:          # když držím shift tak listuju mezi (grass1 nebo grass2 nebo grass3, ...)
                        if event.button == 4:        # 4 je kolečko myši nahoru 
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])  # loopuju používám modulo
                        if event.button == 5:       # 5 je kolečko myši dolu
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                            
                    else:     # když nedržím shift tak nahoru dolu listuju mezi typy (grass, decor, stone, ...)
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:   # přu puštění tlačítka opět nastavuje na False == nedržím == klidový stav
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:             #klavesa a
                        self.movement[0] = True
                    if event.key == pygame.K_d:             #klavesa d
                        self.movement[1] = True
                    if event.key == pygame.K_w:             #klavesa w
                        self.movement[2] = True
                    if event.key == pygame.K_s:             #klavesa s
                        self.movement[3] = True 
                    if event.key == pygame.K_g:             #klavesa g  slouží pro flipování tilů
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:             #klavesa t   autotile fce (napsaná v tilemap.py )
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:             #klavesa o jako (output), uloží výstup editoru.py jako map.json
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:     #kontroluje držení shiftu
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()