#
# cocos2d
# http://python.cocos2d.org
#

from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import random
import math

import pyglet
from pyglet.window import key
from pyglet.gl import *

import cocos
from cocos.director import director
import cocos.collision_model as cm
import cocos.euclid as eu
# import cocos.actions as ac

from cocos import actions, layer, sprite, scene


#class for movement of main character
class HeroShipMovement(actions.Move):
    def step(self, dt):
        super(HeroShipMovement, self).step(dt)
        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 200 * (keyboard[key.UP] - keyboard[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)


class HeroShip(cocos.sprite.Sprite):
    def __init__(self, image):
        super(HeroShip, self).__init__(image)
        self.image = image
        self.position = (100, 100)
        self.velocity = (0,0)
        self.cshape = cm.AARectShape(eu.Vector2(self.position), 32, 32)


class Asteroid(cocos.sprite.Sprite):
    def __init__(self, image, position):
        super(Asteroid, self).__init__(image)
        self.image = image
        self.position = position
        self.velocity = (0,0)
        self.cshape = cm.CircleShape(eu.Vector2(self.position), 16)
        self.type = 'asteroid'


class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.add_hero()
        self.add_asteroids()
        self.add_asteroid()

        # iterator for "count" method test.
        self.i = 0

        #proximity to check distance between hero & test asteroid.
        self.proximity = (0.0, 0.0)

        self.asteroid_list = set()
        self.remove_asteroid_list = set()
        self.asteroid_list.add(self.asteroid_x)
        self.asteroid_list.add(self.asteroid1)
        self.asteroid_list.add(self.asteroid2)

        # self.counter(self.i)
        self.add_count_label()
        self.add_pos_x_label()
        self.add_proximity_label()

        self.schedule(self.update)

    def add_hero(self):
        heroImage = pyglet.resource.image('hero.png')
        self.hero = HeroShip(heroImage)
        self.hero.do(HeroShipMovement())
        self.add(self.hero)

    def add_asteroids(self):
        aster1Image = pyglet.resource.image('asteroid.png')
        aster1Position = (150, 550)
        aster1Velocity = (0, 1000)

        aster2Image = pyglet.resource.image('asteroid_2.png')
        aster2Position = (200, 500)
        aster2Velocity = (100, 25)

        self.asteroid1 = Asteroid(aster1Image, aster1Position)
        self.asteroid2 = Asteroid(aster2Image, aster2Position)
        self.add(self.asteroid1)
        self.add(self.asteroid2)

        self.asteroid1.do(actions.MoveBy( (0, -600), 4) )
        self.asteroid2.do(actions.MoveBy( (100, -600), 8) )

    def add_asteroid(self):
        aster1Image = pyglet.resource.image('asteroid.png')
        aster1Position = (320, 240)
        aster1Velocity = (0, 0)
        self.asteroid_x = Asteroid(aster1Image, aster1Position)
        self.add(self.asteroid_x)

    def boom(self):
        self.msg_boom = cocos.text.Label('BOOM!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        self.msg_boom.position = 320, 440
        self.add(self.msg_boom)

    def add_count_label(self):
        self.msg_counter = cocos.text.Label("TEST",
                                 font_name='Times New Roman',
                                 font_size=16,
                                 anchor_x='center', anchor_y='center')
        self.msg_counter.position = (50, 450)
        self.add(self.msg_counter)

    def add_pos_x_label(self):
        self.msg_pos_x = cocos.text.Label("TEST",
                                 font_name='Times New Roman',
                                 font_size=16,
                                 anchor_x='center', anchor_y='center')
        self.msg_pos_x.position = (200, 25)
        self.add(self.msg_pos_x)

    def add_proximity_label(self):
        self.msg_proximity = cocos.text.Label("TEST",
                                 font_name='Times New Roman',
                                 font_size=16,
                                 anchor_x='center', anchor_y='center')
        self.msg_proximity.position = (400, 50)
        self.add(self.msg_proximity)

    def update_count_label(self, count_in):
        count = count_in
        self.msg_counter.element.text = (str(count))

    def update_pos_x_label(self):
        self.msg_pos_x.element.text = (str(self.hero.position))

    def update_proximity_label(self):
        # self.msg_proximity.element.text = (str(self.asteroid_x.position))
        self.msg_proximity.element.text = (str(self.proximity))

    def counter(self, count_in):
        count = count_in
        self.msg_counter = cocos.text.Label('Count = ' + str(count),
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        msg_x = 120
        self.msg_counter.position = (120, 240)
        self.add(self.msg_counter)

    def check_proximity(self):
        for asteroid in self.asteroid_list:
            self.proximity = (abs(asteroid.position[0] - self.hero.position[0]),
                              abs(asteroid.position[1] - self.hero.position[1]))
            # if ((self.hero.position[0] > 500.0 )and (self.hero.position[1] > 500.0)):
            if ((self.proximity[0] < 25.0 ) and (self.proximity[1] < 25.0)):
                self.boom()

    def remove_asteroid(self):
        for asteroid in self.asteroid_list:
            if (asteroid.position[1] < 10):
                self.remove_asteroid_list.add(asteroid)

        for removable_asteroid in self.remove_asteroid_list:
            self.asteroid_list.remove(removable_asteroid)
            self.remove(removable_asteroid)
        self.remove_asteroid_list.clear()

    def update(self, dt):
        self.i = (self.i + 1)

        self.update_count_label(self.i)
        self.update_pos_x_label()
        self.check_proximity()
        self.update_proximity_label()
        self.remove_asteroid()


if __name__ == "__main__":

    global keyboard

    # director init takes the same arguments as pyglet.window
    # cocos.director.director.init()
    director.init(width=640, height=480, autoscale=True, resizable = True)

    #initializing pyglet, which allows for keyboard import for character movement
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    #creating a background layer
    background_layer = layer.Layer()
    background = sprite.Sprite('space_wallpaper.jpeg')
    background.position = (350, 300)
    background_layer.add(background)


    game_layer = GameLayer()

    # A scene that contains the layer hello_layer
    # main_scene = cocos.scene.Scene(hello_layer, game_layer)
    main_scene = cocos.scene.Scene(background_layer, game_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
