import json

import pygame

AUTOTILE_MAP = {                                                   # pravidla pro autotiling
    tuple(sorted([(1, 0), (0, 1)])): 0,                            # porovnává sousedící tiles a podle toho nastavuje daný tile
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}             # má smysl jen pro trávy a kameny

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}               # všechny tiles
        self.offgrid_tiles = []         # všechny tiles mimo grid
        
    def extract(self, id_pairs, keep=False):      #fce pro získání souřadnic, kde je určitý typ tilu pro následné animace (zjistí, kde je strom, aby se tam mohl spwnout padající list)
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:         # když se daný typ a varianta rovná hledaným tak se mi přidají do matches[], abych s nimi mohl dále pracovat
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:            #když je daný typ a varianta v id_pairs, 
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()          #zjistíme pro ni souřadnice
                matches[-1]['pos'][0] *= self.tile_size                 # a velikost
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches               # vrací hodnoty které potřebubjeme pro hledané typy a varianty
    
    def tiles_around(self, pos):             # tato funkce načíta hodnoty kolem ninjy pro kontrolu kolize
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))       # // je dělení beze zbytku (zahodí ho)
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):    # fce pro ukládání mapy z editor.py
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)  # pro .json zapisuji jako slovník
        f.close()
        
    def load(self, path):   # načítá map.json 
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        
    def solid_check(self, pos): # pokud je pod enemákem a ze šikma před ním solid tile jde dál, jestli ne, tak se otočí a jde na druhou stranu
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):     # projde všechny tiles v tiles_around podle pozice hráče
            if tile['type'] in PHYSICS_TILES:    # a když je tile v Physics tiles (je tráva nebo kámen)
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects                            # přidají se do listu obdelník všchny obdelníky kde tiles sousedí s trávou nebo kamenem
    
    def autotile(self):                     #automaticky mi upravuje, který tile se mi placne do mapy (mezi hlínu nedá trávu)
        for loc in self.tilemap:            # má smysl jen pro trávy a kameny
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:   #všechny sousedící tiles na gridu
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:   # přepisuje typ tilu podle sousedících
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))    
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):        # zjistí zda-li daný typ je tráva či kámen a jestli odpovídá pravidlům, jestli ano nastaví danou variantu
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
             # offset odečítám, protože kamera se pohne doprava tak vše na screenu se pohne doleva
            
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1): 
            # chceme renderovat pouze pixely co jsou  na obrazovce podle pozice kamery, kterou zde zjišťujeme pomocí offset[0] // self.tile_size --> tím zjistíme levý horní pixel
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))