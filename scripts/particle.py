class Particle:                                                             # třída pro samotné padající listy
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame
    
    def update(self):  # když tato fce vrátí True smaže se particle
        kill = False
        if self.animation.done:     # když skončí animace nastaví se kill na true
            kill = True
        
        self.pos[0] += self.velocity[0]             # pohyb animace
        self.pos[1] += self.velocity[1]
        
        self.animation.update()         #update animace
        
        return kill
    
    def render(self, surf, offset=(0, 0)):      # renderuje danou animaci
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
    