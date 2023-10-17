import pygame as pg
from random import randint,choice
v=pg.Vector2
print("Hello world")
print("Sasha knows how to pull!")
class Mono:
    def __init__(self):
        self.children=[]
        self.active=True
    def start(self):
        pass

    def update(self):
        if not self.active:
            return 
        for child in self.children:
            child.update()
    def draw(self,screen):
        if not self.active:
            return 
        for child in self.children:
            child.draw(screen)
class BlockSpawner(Mono):
    last_block=None
    spawner= None
    def spawn_block(self):
        BlockSpawner.last_block=Block(choice(self.blocks),v(randint(0,9),randint(0,2)),choice(self.colors),30)
        self.children.append(BlockSpawner.last_block)
    def update(self):
        if not self.active:
            return 
        Mono.update(self)
    def __init__(self,frames_delay):
        BlockSpawner.spawner=self
        Mono.__init__(self)
        self.frames_delay=frames_delay
        self.colors=[(255,165,0),(255,0,0),(255,255,0),(0,128,0),(66,170,255),(0,47,167),(139,0,255),(153,102,204),(127,255,212),(251,206,177),(205,38,130),
                                (250,231,181),(250,231,181),(48,213,200),(0,49,83),(119,221,231),(171,205,239),(255,219,139),
                                (176,63,53),(221,173,175),(249,132,229),(218,189,171),(175,238,238),(152,251,152),(206,210,58),(213,113,63),(191,255,0)]
        self.b1=[v(1,0),v(0,1),v(0,2)]
        self.b2=[v(0,1),v(1,0),v(2,0)]
        self.b3=[v(1,0),v(0,1),v(1,1)]
        self.b4=[v(-1,0),v(0,1),v(1,1)]
        self.b5=[v(0,-1),v(0,1),v(0,2)]
        self.b6=[v(0,-1),v(1,0),v(1,1)]
        self.b7=[v(1,-1),v(1,0),v(-1,0),v(-1,-1)]
        self.b8=[v(0,-1),v(-1,0),v(-1,1),v(1,-1)]
        self.b9=[v(0,-1),v(-1,0),v(1,0),v(0,1)]
        self.b10=[v(0,-1),v(-1,0),v(1,0)]
        self.blocks=[self.b1,self.b2,self.b3,self.b4,self.b5,self.b6,self.b7,self.b8,self.b9,self.b10]
        self.spawn_block()
class Player(Mono):
    def update(self):
        if Input.get_key_down(pg.K_SPACE):
            print("player нажал пробел")
        if Input.get_key_down(pg.K_9):
            print("player нажал 9")
        if Input.get_key_down(pg.K_8):
            print("player нажал 8")
        if Input.get_key_down(pg.K_7):
            print("player нажал 7")
        if Input.get_key_down(pg.K_6):
            print("player нажал 6")
        if Input.get_key_down(pg.K_5):
            print("player нажал 5")
        if Input.get_key_down(pg.K_TAB):
            print("player нажал tab")
        if Input.get_key_down(pg.K_UP):
            print("player нажал up")
        if Input.get_key_down(pg.K_DOWN):
            print("player нажал down")
            BlockSpawner.last_block.position+=v(0,1)
        if Input.get_key_down(pg.K_LEFT):
            print("player нажал left")
            BlockSpawner.last_block.position+=v(-1,0)
            BlockSpawner.last_block.fix_position()
        if Input.get_key_down(pg.K_RIGHT):
            print("player нажал right")
            BlockSpawner.last_block.position+=v(1,0)
            BlockSpawner.last_block.fix_position()
        if Input.get_key_down(pg.K_PERIOD):
            print("player нажал .")
            BlockSpawner.last_block.rotate_right()
            BlockSpawner.last_block.fix_position()
        if Input.get_key_down(pg.K_COMMA):
            print("player нажал ,")
            BlockSpawner.last_block.rotate_left()
            BlockSpawner.last_block.fix_position()
class Block(Mono):
    def rotate_right(self):
        for i in range(len(self.tiles)):
            self.tiles[i]=rotate_right(self.tiles[i])
    def rotate_left(self):
        for i in range(len(self.tiles)):
            self.tiles[i]=rotate_left(self.tiles[i])
    def fix_position(self):
        for tile in self.tiles:
            p = self.position + tile
            if p.x < 0:
                self.position+=v(1,0)
                self.fix_position()
                return
            if p.x > 11:
                self.position+=v(-1,0)
                self.fix_position()
                return

    def draw(self, screen):
        for tile in self.tiles:
            curr_pos = self.position + tile
            pg.draw.rect(screen,self.color,(curr_pos.x*self.size,curr_pos.y*self.size,self.size,self.size))
            pg.draw.rect(screen,(0,0,0),(curr_pos.x*self.size,curr_pos.y*self.size,self.size,self.size),5)
    def __init__(self,tiles,position,color,size):
        Mono.__init__(self)
        self.tiles=[v()]+tiles
        self.position=position
        self.color=color
        self.size=size
        self.moving = True
    def update(self):
        if not self.moving:
            return
        if Input.frames%10==0 and self.moving:
            self.position+=v(0,1)
        for tile in self.tiles:
            curr_pos = self.position + tile
            if curr_pos.y==21:
                self.moving = False
                BlockSpawner.spawner.spawn_block()
                break
class Game:
    def __init__(self):
        pg.init()
        self.screen=pg.display.set_mode((30*12,30*22))
        self.clock=pg.time.Clock()
        self.monos=[Player(),BlockSpawner(20)]
        self.frames=0
        self.run()

    def run(self):
        self.running=True
        while self.running:
            self.screen.fill("purple")
            Input.update(pg.event.get(),self)
            for mono in self.monos:
                mono.update()
            for mono in self.monos:
                mono.draw(self.screen)
            self.clock.tick(40)
            pg.display.update()
        pg.quit()
class Input:
    @staticmethod
    def get_key_down(key):
        return pg.KEYDOWN in Input.events and Input.events[pg.KEYDOWN].key == key
    frames = 0
    @staticmethod
    def update(events,game):
        Input.frames += 1
        Input.events = {e.type: e for e in events}
        game.running = not pg.QUIT in Input.events
def rotate_right(vector):
    return v(vector.y, -vector.x)
def rotate_left(vector):
    return v(-vector.y,vector.x)
game=Game()
