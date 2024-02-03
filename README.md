
# TheWarGame


A doom like raycaster in python created as part of a school project for the end of the high school year.
The game is presented as a first person shooter (fps) where you play as a
soldier who teleports from place to place and eliminates the aliens who have invaded
the world and different spaces. Cross different original maps in
a retro pixel art style. The story is still developing, the futures
story mode levels will come later with updates.

## Demo

[![Watch the video](https://raw.githubusercontent.com/deltahmed/TheWarGame/main/Media/demo.png)](https://www.youtube.com/watch?v=teRpmBCHo3Q)

## Prerequisites
- To be able to play the game you must have installed a **recent version of
python 3**,
- the libraries required for the game to work properly are available by clicking only on the .bat file provided or type :
```
pip install -r requirements.txt
```
- lunch the main.pyw file from the game source files.

## Game launch

Choose the different parameters for launching the game, a classic launch would be
```
- Windows size : 1000x600
- textures and 3d projection : Medium
- field of vision : Normal
- FPS blocking : 60
```
> The python interpreter being very slow, do not overdo the graphics settings on a less powerful machine and block the fps on a powerful machine.


![Game Luncher](https://raw.githubusercontent.com/ahmedmathsinfo/TheWarGame/main/Media/GameLuncher.jpg)



### Several choices are available to you :
- the tutorial which teaches the basics of the game,
- the story mode consisting of only one level for now, 3 saves only are available for this mode, *the possibility of deleting a backup is not not yet implemented (the only way to delete game data is by the developer tools Game\tools\cleardata.pyw)*,
- The infinite mode which is played endlessly with random worlds and monster positions, *(two level are available for the moment)*,the best score that you have made in this made, is stored in statistics menu.

![alt](https://raw.githubusercontent.com/ahmedmathsinfo/TheWarGame/main/Media/Menu.jpg)

## How to Play
### Everything is explained in game
![alt](https://raw.githubusercontent.com/ahmedmathsinfo/TheWarGame/main/Game/media/objets/z3.png)
![alt](https://raw.githubusercontent.com/ahmedmathsinfo/TheWarGame/main/Game/media/objets/z5.png)
![alt](https://raw.githubusercontent.com/ahmedmathsinfo/TheWarGame/main/Game/media/objets/z8.png)

# Map Creation
## Prerequisites
- Same as game prerequisites
- lunch the main.pyw file from the MapCreator source files.
## Presentation
A tool that allows you to draw maps, its only for developer beacause of its complexity of understanding and its bugs caused by the Tcl interpreter of Tkinter and also because of its weak bugs protection **(you have to know what you are doing)**
## Use
- Texture mode: we draw the textures
- Room mode: create a room by having previously selected a sky and a floor and choose the door with the click wheel
- Entity mode: we draw the objects and monster, we can choose the point player appearance with double click wheel
# Sources and inspirations
## Inspirations 
- [Doom and Wolfenstein Raycasting](https://guy-grave.developpez.com/tutoriels/jeux/doom-wolfenstein-raycasting/)
- [Raycasting C tutorial](https://lodev.org/cgtutor/raycasting3.html#Introduction)
- [Coder Space](https://github.com/StanislavPetrovV)

## Textures sources 
- [Retro games texture pack](https://little-martian.itch.io/retro-texture-pack)
- [2d pixel art cacodaemon sprites](https://elthen.itch.io/2d-pixel-art-cacodaemon-sprites)
- [Retro games sprites pack](https://little-martian.itch.io/retro-sprite-pack)
- [all assets are from itch.io](https://itch.io/)

