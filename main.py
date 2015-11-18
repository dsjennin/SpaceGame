__author__ = 'samhauck'
import pyglet
from pyglet.window import key
import cocos
from cocos import actions, layer, sprite, scene
from cocos.director import director


#  initialzing the director. the director creates the window for the game
director.init(width=500, height= 300, autoscale=True, resizable = True)

#  creating a layer using the cocos2d platform
#  different layers are used for each aspect of the game, i.e. the main character or background
player_layer = layer.Layer()

#creating a Sprite for the main character
heroShip = sprite.Sprite('addimagehere.jpg')

#adding the main character to the 'player_layer' layer
player_layer.add(heroShip)


