import math
import random
from pygame import Rect

WIDTH = 500
HEIGHT = 500


# enemy class!
class Enemy(Actor):
    pass



# hero class!
class Hero(Actor):
    pass




hero = Hero('hero', center=(WIDTH/2, HEIGHT/2))
test_enemy = Enemy(f'enemy{random.randint(1, 3)}')


# enemy.center = (500, 500)



#### middleware
####
####

enemy_list = []
# whenever a new enemy is to be spawned, this is called
def spawn_enemy(): 

    new_enemy = Enemy(f'enemy{random.randint(1, 3)}', center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    enemy_list.append(new_enemy)
    print(f'{len(enemy_list)} enemys!!!!')
    
    
    
    
    
    
    
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

spawn_enemy()
spawn_enemy()
spawn_enemy()





    



def draw():
    screen.clear()
    hero.draw()
    test_enemy.draw()
    for enemy in enemy_list: 
        enemy.angle = enemy.angle_to(hero) + 90
        enemy.draw()
    
    
    
def on_mouse_move(pos):
    for enemy in enemy_list:
        enemy.angle = enemy.angle_to(hero) + 90
    hero.pos = pos
    
    
def update():
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
                
        # finally adds movemento to enemy
        enemy.x += x_move
        enemy.y += y_move
            # enemy_move = animate(enemy, pos=hero.pos)
        # else:
            # print('colision')
            
        # animate(enemy, duration=2, pos=hero.pos)