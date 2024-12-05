# Hexscape

## Story/Manifesto

- add a dialog to the game
  - "Where am I?"
  - "What am I doing here?"
  - "I guess all I can do is keep moving..."
  - (*after some momentum is gained) "I know I can find a way."
- emphasis on memory, sounds, attention to details
- the big picture should be gaining confidence, and persevering through failure/the unknown
- you can't go back. you can't know if which way youre heading is the right way or not, but you have to keep moving.

## Map

- save the tilemap in a .json
- generate in an irregular shape
- make holes, rooms, forks, loops
- generate with a more meaningful goal/exit point

## Visual FX

- parallax effect to center the 'camera' on the ball
- add some 'bumping' animation for running into a wall
- ball glows stronger and stronger the closer you are to the 'waypoints'

## Audio FX

- add excitement to the music as the player progresses/gains more confidence
  - add a layer to the music for each waypoint discovered
  - needs a good kick drum line
  - snare
  - hihat
  - guitar

## Gameplay Mechanics

### Waypoints

- add waypoints and rooms around them
  - RED lets you break through walls (a limited number of times)
  - ORANGE lights the path to the nearest waypoint for a few seconds
  - YELLOW lights up all the tiles surrounding you (and the walls) temporarily
  - GREEN highlights the other waypoints on the map temporarily
  - PURPLE teleports you to another waypoint (or within __(randint(level-1, level+1))__ distance of one)
  - BLUE boosts every move to the longest possible (**find a better way to phrase this lmao)
