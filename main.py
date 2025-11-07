import math
import random
from pygame import Rect

WIDTH = 500
HEIGHT = 500
running = False


# enemy class!
class Enemy(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        
    def destroy(self):
        # creates new explosion
        new_explosion = Explosion('explosion1', pos=self.pos)
        explosion_list.append(new_explosion)
        # deletes itself
        enemy_list.remove(self)
        print('destroyed ship')
        
        
        
    pass

# explosion!
class Explosion(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = ['explosion3', 'explosion2', 'explosion1', 'explosion2', 'explosion3']
        self.current_frame = 0
        # set out to delete itself upon creation like ourselves
        clock.schedule_interval(self.next_frame, 0.1)
        
        
    def next_frame(self):
        self.current_frame += 1
        print('running explosion')
        
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
    pass


# bullet class 
class Bullet(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 10
    
    
    # for handling traveling
    def shoot(self):
        angle = math.radians(self.angle)
        self.x += math.sin(angle) * self.speed
        self.y -= math.cos(angle) * self.speed
        
    # detects hit on enemy ships
    def hit(self, enemy):
        enemy.destroy()
        bullet_list.remove(self)
        print('removed bullet')
        
        
        
        
        
        
    

    
    pass




hero = Hero('hero', center=(WIDTH/2, HEIGHT/2))
test_enemy = Enemy(f'enemy{random.randint(1, 3)}')
start = Actor('buttonlong_blue', center=(WIDTH / 2, 100))
music = Actor('buttonlong_blue', center=(WIDTH / 2, 175))
exit = Actor('buttonlong_blue', center=(WIDTH / 2, 250))





#### middleware
####
####
bullet_list = []
enemy_list = []
explosion_list = []
MAX_ENEMYS = 5
# whenever a new enemy is to be spawned, this is called
def spawn_enemy(): 
    global running
    if len(enemy_list) < MAX_ENEMYS and running:
        new_enemy = Enemy(f'enemy{random.randint(1, 3)}', center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        enemy_list.append(new_enemy)
        print(f'{len(enemy_list)} enemys!!!!')
    # new_enemy.draw()
    
    

    
    
    
    
#  whenever enemy moves in direction to hero, run this function. Purpose is to normalize speed.
def enemy_to_hero_vec(enemy, hero):
    x_vec = hero.x - enemy.x
    y_vec = hero.y - enemy.y
    dist = ((x_vec ** 2) + (y_vec ** 2)) ** (0.5)
    if (dist == 0):
        return (0, 0)
    return ((x_vec / dist), (y_vec / dist))



####
####
####


clock.schedule_interval(spawn_enemy, 5)





    



def draw():
    screen.clear()
    ##### game screen
    if running:
        hero.draw()
        test_enemy.draw()
        for enemy in enemy_list: 
           enemy.angle = enemy.angle_to(hero) + 90
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
        music.draw()
        screen.draw.text('MUSIC ON', center=music.pos)
        exit.draw()
        screen.draw.text('EXIT', center=exit.pos)
        
        
        pass
        
        
    
    
def on_mouse_down(pos, button):
    global running
    ## moves hero to click (found a better way to move with animate. Might change enemy movement later)
    if running:
        
        HERO_SPEED = 100
        animate(hero, pos=pos, duration=(hero.distance_to(pos) / HERO_SPEED))
        hero.angle = hero.angle_to(pos) + 90
        # hero.pos = pos
        
        pass
    
    else: 
        if (start.collidepoint(pos) and (button == 1)):
            print('clicked start')
            # running = True
            start.image = 'buttonlong_blue_pressed'
        elif (music.collidepoint(pos) and (button == 1)):
            music.image = 'buttonlong_blue_pressed'
        elif (exit.collidepoint(pos) and (button == 1)):
            exit.image = 'buttonlong_blue_pressed'
        pass
  
  
  
            
            
def on_mouse_up(pos, button):
    global running
    
    if running:
        pass
    else:
        if (button == 1):
            start.image = 'buttonlong_blue'    
            exit.image = 'buttonlong_blue'
            music.image = 'buttonlong_blue'
        if (start.collidepoint(pos)):
            running = True
        elif (music.collidepoint(pos)):
            pass # add music controlling later
        elif (exit.collidepoint(pos)):
            quit()
            
            
            
            
def on_key_down(key):
    global running
    if running:
        if key == keys.SPACE:
            bullet1 = Bullet('cannonball', pos=hero.center)
            print(hero.angle)
            print(hero.angle - 90)
            bullet1.angle = - (hero.angle - 90) 
            print(bullet1.angle)
            bullet2 = Bullet('cannonball', pos=hero.center)
            bullet2.angle = - (hero.angle + 90)
            bullet_list.append(bullet1)
            bullet_list.append(bullet2)
        
        
        
        
        pass
    else: 
        pass
    
def update():
    global running
    
    
    #### GAME IS RUNNING
    if running:
        
        
        ## moves bullets
        for bullet in bullet_list:
            bullet.shoot()
            if bullet.collidelist(enemy_list) != -1:
                enemy_to_destroy = enemy_list[bullet.collidelist(enemy_list)]
                bullet.hit(enemy_to_destroy)
        
        ## check for colision of hero and enemy
        if hero.collidelist(enemy_list) != -1:

            running = False
            enemy_list.clear()
            hero.pos = (WIDTH / 2, HEIGHT / 2)
        
        
        
        ## angulates enemys to hero
        for enemy in enemy_list:
            enemy.angle = enemy.angle_to(hero) + 90
        
        ### moves enemys to hero
        ENEMY_SPEED = 1
        PUSH_FORCE = 0.5
        
        for i in range(len(enemy_list)):
            # gets each enemy
            enemy = enemy_list[i]
            # copy of enemy list minus the one we are at
            list_no_i = enemy_list[:]
            list_no_i.pop(i)
            
            # creates move vector and already calculates distance to hero
            x_move, y_move = enemy_to_hero_vec(enemy, hero)
            x_move *= ENEMY_SPEED
            y_move *= ENEMY_SPEED
            
            
            # list of collisions of i-enemy
            enemy_collision = enemy.collidelistall(list_no_i)
            
        
            
            # if there's colision, we'll have to push other enemys away
            if (len(enemy_collision) > 0): 
                for colliding in enemy_collision:
                    
                    # create push-away vector and normalizes it
                    x_push = enemy.x - enemy_list[colliding].x
                    y_push = enemy.y - enemy_list[colliding].y
                    
                    push_dist = ((x_push ** 2) + (y_push ** 2)) ** (0.5)
                    if push_dist > 0:
                        x_move += (x_push / push_dist) * PUSH_FORCE
                        y_move += (y_push / push_dist) * PUSH_FORCE
            
            move_value = ((x_move ** 2) + (y_move) ** 2) ** (0.5)
            # finally adds movement to enemy
            enemy.x += x_move / move_value
            enemy.y += y_move / move_value
        pass



    #### AT MENU
    else:         
        pass
                
                
                
                
        
    
    
            