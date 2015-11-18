__author__ = 'samhauck'
import pyglet
from pyglet.window import key
import cocos
from cocos import actions, layer, sprite, scene
from cocos.director import director

def main():

    global keyboard

    #  initialzing the director. the director creates the window for the game
    director.init(width=500, height= 300, autoscale=True, resizable = True)

    #  creating a layer using the cocos2d platform
    #  different layers are used for each aspect of the game, i.e. the main character or background
    player_layer = layer.Layer()

    #creating a Sprite for the main character
    heroShip = sprite.Sprite('boss.png')

    #adding the main character to the 'player_layer' layer
    player_layer.add(heroShip)

    #initializing the main character's position and velocity
    heroShip.position = (100, 100)
    heroShip.velocity = (0, 0)

    #initializing pyglet, which allows for keyboard import for character movement

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    #assigning the movement class to the heroShip sprite
    heroShip.do(heroShipMovement())

    main_scene = scene.Scene(player_layer)

    director.run(main_scene)



#class for movement of main character
class heroShipMovement(actions.Move):
    def step(self, dt):
        super(heroShipMovement, self).step(dt)
        velocity_x = 100 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 100 * (keyboard[key.UP] - keyboard[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)



main()


