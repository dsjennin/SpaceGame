#
# cocos2d
# http://python.cocos2d.org
#

# 2015/12/11, DJB:
# OK, the semester's over, but I wanna keep workiing on this. Here's a
# quick list of things we can do to improve and expand the project.
#
# ToDo:
# -GamePlay:
#   -Continuous asteroids.
#   -Shooting.
#   -Boss?
#   -Effects:
#       -Music/Sound
#       -Explosions/Particles
#       -More sprites!
#       -Transitions between levels (once we add levels)
#
# -Environment:
#   -Scrolling background.
#   -Multiple layers.
#
# -Logic:
#   -Scoring.
#       -Keep track of high scores.
#   -Levels.
#
# -Software, Intenal:
#   *GET COLLISION MANAGER WORKING!!!
#       -This is probably the single biggest obstacle.
#       -"check_proximity(self)" is nice 'n all, but I expect the built-in
#        collision manager is far more efficient and flexible.
#   -Meta-data.
#   -Constants.
#       -We should declare a bunch up top to facilitate manipulation.
#   -Refactoring?
#       -I expect there are many ways in which we could optimize
#        memory allocation, etc.
#   -Unit tests.
#       -Seriously? Well, yes. I'm told it's a thing.
#
# -Software, External:
#   -Architecture:
#       -Break out class definitions into header files?
#       -Figure out how to read from and write to files.
#   -Porting?
#       -Different languages?
#           -C++
#           -Objective C / Swift?
#           -Java?
#       -Different platforms?
#           -iOS?
#           -Android?
#           -Windows Phone? HA! Yeah, right...
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
    def keyboard_diffs(self, first, second):
      return keyboard[first] - keyboard[second]

    def keyboard_x(self):
      return self.keyboard_diffs(key.RIGHT, key.LEFT)

    def keyboard_y(self):
      return self.keyboard_diffs(key.UP, key.DOWN)

    def step(self, dt):
        super(HeroShipMovement, self).step(dt)
        self.target.velocity = (self.keyboard_x() * 200, self.keyboard_y() * 200)


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

    @staticmethod
    def random_starting_position():
        xrange = random.randrange(20, 500)
        yrange = 450
        return (xrange, yrange)

    @staticmethod
    def random_offset():
      return (random.randint(-900, 900), -600)

    @staticmethod
    def random_speed():
      return random.randint(3,21)

    def offscreen(self):
      return self.position[1] < 10

class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.add_hero()
        # self.add_asteroid()

        # iterator for "count" method test.
        self.frame_count = 0

        #proximity to check distance between hero & test asteroid.
        self.proximity = (0.0, 0.0)

        self.asteroid_dict = {}

        self.asteroid_list = set()
        self.remove_asteroid_list = set()
        # self.asteroid_list.add(self.asteroid_x)
        # self.asteroid_list.add(self.asteroid1)
        # self.asteroid_list.add(self.asteroid2)

        self.add_count_label()
        self.add_pos_x_label()
        self.add_proximity_label()

        self.schedule(self.update)

    def add_hero(self):
        heroImage = pyglet.resource.image('assets/hero.png')
        self.hero = HeroShip(heroImage)
        self.hero.do(HeroShipMovement())
        self.add(self.hero)

    def add_asteroid(self):
        aster1Image = pyglet.resource.image('assets/asteroid.png')
        aster1Position = (320, 240)
        aster1Velocity = (0, 0)
        self.asteroid_x = Asteroid(aster1Image, aster1Position)
        self.add(self.asteroid_x)

    def generate_asteroids(self):
        if (len(self.asteroid_list) < 10):
            asterImage = pyglet.resource.image('assets/asteroid.png')
            asterPos = Asteroid.random_starting_position()
            
            asteroid = Asteroid(asterImage, asterPos)
            asteroid.do(actions.MoveBy(Asteroid.random_offset(), Asteroid.random_speed()))
            self.asteroid_list.add(asteroid)
            self.add(asteroid)

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

    def increment_frame_count(self):
        self.frame_count = self.frame_count + 1
        self.msg_counter.element.text = (str(self.frame_count))

    def update_pos_x_label(self):
        self.msg_pos_x.element.text = (str(self.hero.position))

    def update_proximity_label(self):
        # self.msg_proximity.element.text = (str(self.asteroid_x.position))
        self.msg_proximity.element.text = (str(self.proximity))

    def check_proximity(self):
        for asteroid in self.asteroid_list:
            self.proximity = (abs(asteroid.position[0] - self.hero.position[0]),
                              abs(asteroid.position[1] - self.hero.position[1]))
            # if ((self.hero.position[0] > 500.0 )and (self.hero.position[1] > 500.0)):
            if ((self.proximity[0] < 25.0 ) and (self.proximity[1] < 25.0)):
                self.boom()

    def remove_asteroid(self):
        to_remove = set()
        for asteroid in self.asteroid_list:
            if (asteroid.offscreen()):
                to_remove.add(asteroid)

        for removable_asteroid in to_remove:
            self.asteroid_list.remove(removable_asteroid)
            self.remove(removable_asteroid)

    def update(self, dt):
        self.generate_asteroids()
        self.increment_frame_count()
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
    background = sprite.Sprite('assets/perseus2.png')
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
