import math
import random
from pygame import Rect

WIDTH = 1000
HEIGHT = 1000
running = False
SOUNDS = False
bullet_list = []
enemy_list = []
explosion_list = []
MAX_ENEMYS = 5


# enemy class!
class Enemy(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SPEED = 1
        # for handling collisions bettween other enemys
        self.PUSH_FORCE = 0.5
        
        
        
    def destroy(self):
        # creates new explosion
        new_explosion = Explosion('explosion1', pos=self.pos)
        explosion_list.append(new_explosion)
        # deletes itself
        enemy_list.remove(self)
        
        
        
    def move_to_hero(self, hero, other_enemies):
        ###
        ### this method creates x_move and y_move for the enemy, 
        ### considering other enemys that might be close to the one that
        ### this function is being ran at
        ###
        
        # angles to hero always
        self.angle = self.angle_to(hero.pos) + 90
        
        # creates x_move and y_move considering only hero
        x_move, y_move = enemy_to_hero_vec(self, hero)
        x_move *= self.SPEED
        y_move *= self.SPEED
        
        # list of all collisions for checking push forces
        enemy_collision = self.collidelistall(other_enemies)
        if (len(enemy_collision) > 0):
            for index in enemy_collision:
                colliding_enemy = other_enemies[index]
                
                x_push = self.x - colliding_enemy.x
                y_push = self.y - colliding_enemy.y
                # for normalization
                push_dist = ((x_push ** 2) + (y_push ** 2)) ** (0.5)
                if push_dist > 0:
                    x_move += (x_push / push_dist) * self.PUSH_FORCE
                    y_move += (y_push / push_dist) * self.PUSH_FORCE
        # finally moves
        self.x += x_move
        self.y += y_move
        
        pass
        
        
        
    pass

# explosion class!
class Explosion(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = ['explosion3', 'explosion2', 'explosion1', 'explosion2', 'explosion3']
        self.current_frame = 0
        # set out to delete itself upon creation like ourselves
        clock.schedule_interval(self.next_frame, 0.1)
        if SOUNDS:
            sounds.explosion_sound.play()
        
    def next_frame(self):
        self.current_frame += 1
        
        if self.current_frame < len(self.frames):
            self.image = self.frames[self.current_frame]
        else:
            clock.unschedule(self.next_frame)
            if self in explosion_list:
                explosion_list.remove(self)

# hero class!
class Hero(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SPEED = 100
        
    def move(self, pos):
        ### 
        ### moves hero to position
        ###
        animate(self, pos=pos, duration=(self.distance_to(pos) / self.SPEED))
        self.angle = self.angle_to(pos) + 90
        
    def shoot(self):
        ###
        ### creates two bullets
        ###
        bullet1 = Bullet('cannonball', pos=self.center)
        bullet1.angle = - (self.angle - 90) 
        bullet2 = Bullet('cannonball', pos=self.center)
        bullet2.angle = - (self.angle + 90)
        bullet_list.append(bullet1)
        bullet_list.append(bullet2)
    pass

# bullet class 
class Bullet(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 10
        if SOUNDS:
            sounds.shoot_sound.play()
    
    
    # for handling traveling
    def shoot(self):
        angle = math.radians(self.angle)
        self.x += math.sin(angle) * self.speed
        self.y -= math.cos(angle) * self.speed
        
    # detects hit on enemy ships
    def hit(self, enemy):
        enemy.destroy()
        bullet_list.remove(self)

    pass


hero = Hero('hero', center=(WIDTH/2, HEIGHT/2))
start = Actor('buttonlong_blue', center=(WIDTH / 2, 100))
music_button = Actor('buttonlong_blue', center=(WIDTH / 2, 175))
exit = Actor('buttonlong_blue', center=(WIDTH / 2, 250))





#### 
#### middleware
####

# whenever a new enemy is to be spawned, this is called
def spawn_enemy(): 
    if running and len(enemy_list) < MAX_ENEMYS:
        # random side
        side = random.randint(0, 3)

        if side == 0: # top
            pos = (random.randint(0, WIDTH), -50)
        elif side == 1: # right
            pos = (WIDTH + 50, random.randint(0, HEIGHT))
        elif side == 2: # bottom
            pos = (random.randint(0, WIDTH), HEIGHT + 50)
        else: # left
            pos = (-50, random.randint(0, HEIGHT))

        new_enemy = Enemy(f'enemy{random.randint(1, 3)}', center=pos)
        enemy_list.append(new_enemy)    
    

#  whenever enemy moves in direction to hero, run this function. Purpose is to normalize speed.
def enemy_to_hero_vec(enemy, hero):
    x_vec = hero.x - enemy.x
    y_vec = hero.y - enemy.y
    dist = ((x_vec ** 2) + (y_vec ** 2)) ** (0.5)
    if (dist == 0):
        return (0, 0)
    return ((x_vec / dist), (y_vec / dist))



####
#### schedules
####

# tries to spawn enemy every second
clock.schedule_interval(spawn_enemy, 1)

###
### actions
###

def draw():
    screen.clear()
    ##### game screen
    if running:
        hero.draw()
        for enemy in enemy_list: 
           enemy.draw()
        for bullet in bullet_list:
            bullet.draw()
        for explosion in explosion_list:
            explosion.draw()
        
    
    else:
    ## initial screen
        screen.clear()
        start.draw()
        screen.draw.text('START', center=start.pos)
        music_button.draw()
        if SOUNDS:
            screen.draw.text('MUSIC ON', center=music_button.pos)
        else:
            screen.draw.text('MUSIC OFF', center=music_button.pos)
        exit.draw()
        screen.draw.text('EXIT', center=exit.pos)
        screen.draw.text('Press spacebar to shoot!', center=(WIDTH / 2, 325))
        screen.draw.text('Move with mouse clicks', center=(WIDTH / 2, 400))
        
        
        pass
              
def on_mouse_down(pos, button):
    # clicks for game running
    global running
    ## moves hero to click (found a better way to move with animate. Might change enemy movement later)
    if running:
        hero.move(pos)
        
        pass
    
    # clicks for menu
    else: 
        if (start.collidepoint(pos) and (button == 1)):
            # running = True
            start.image = 'buttonlong_blue_pressed'
        elif (music_button.collidepoint(pos) and (button == 1)):
            music_button.image = 'buttonlong_blue_pressed'
        elif (exit.collidepoint(pos) and (button == 1)):
            exit.image = 'buttonlong_blue_pressed'
        pass
  
def on_mouse_up(pos, button):
    global running
    global SOUNDS
    
    if running:
        pass
    
    # clicks for game menu
    else:
        if (button == 1):
            start.image = 'buttonlong_blue'    
            exit.image = 'buttonlong_blue'
            music_button.image = 'buttonlong_blue'
        if (start.collidepoint(pos)):
            running = True
        elif (music_button.collidepoint(pos)):
            SOUNDS = not SOUNDS
            if SOUNDS:
                music.play('theme') 
            else:
                music.stop()        
            pass # add music controlling later
        elif (exit.collidepoint(pos)):
            quit()
            
def on_key_down(key):
    global running
    if running:
        ## shooting logic
        if key == keys.SPACE:
            hero.shoot()
        pass
    else: 
        pass
    
def update():
    global running
    global SOUNDS

    #### GAME IS RUNNING
    if running:
        
        ## bullet logic for moving and hiting enemy
        for bullet in bullet_list:
            bullet.shoot()
            enemy_hit_index = bullet.collidelist(enemy_list) 
            if enemy_hit_index != -1:
                enemy_to_destroy = enemy_list[enemy_hit_index]
                bullet.hit(enemy_to_destroy)
        
        ## check for colision of hero and enemys and goes back to menu
        if hero.collidelist(enemy_list) != -1:

            running = False
            enemy_list.clear()
            bullet_list.clear()
            hero.pos = (WIDTH / 2, HEIGHT / 2)
            hero.angle = 0
        
        # runs enemy movement
        if len(enemy_list) > 0:
            for i, enemy in enumerate(enemy_list):
                other_enemies = enemy_list[:i] + enemy_list[i + 1:]
                enemy.move_to_hero(hero, other_enemies)
        pass

    #### AT MENU
    else:         
        pass