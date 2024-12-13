# Hexscape

## Story/Manifesto

- add a dialog to the game
  - "Where am I?"
  - "What am I doing here?"
  - "I guess all I can do is keep moving..."
  - (*after some momentum is gained) "I know I can find a way."
- emphasis on memory, sounds, attention to details. make it impossible to win just by button mashing.
- the big picture should be gaining confidence, and persevering through failure/the unknown. embracing it even, as the cornerstone of progress and growth.
- the player should understand that you can't go back on decisions you've made in the past. it's nearly impossible to know if which way you're headed is the right way or not, but you have to keep moving. keep trying.

## Aesthetics

- every asset either my own hand drawing via aesprite or a primative shape via pyglet
- the HUD includes:
  - a move counter in the top right corner
  - the level in the top left corner
  - the player's currently collected waypoints along the left edge of the screen
  - a menu/settings/pause button either in the top right corner or the bottom right corner

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

### Map/Procedural Maze Generation

- save the tilemap in a map.json?
- parameters for the procedurally generated maze
  - irregular shape
  - loops
  - rooms?
  - 'destination' for each waypoint
  - meaningful goal/exit point

### Waypoints

- add waypoints and rooms around them
  - RED lets you break through walls (a limited number of times)
  - ORANGE lights the path to the nearest waypoint for a few seconds
  - YELLOW lights up all the tiles surrounding you (and the walls) temporarily
  - GREEN highlights the other waypoints on the map temporarily
  - PURPLE teleports you to another waypoint (or within __(randint(level-1, level+1))__ distance of one)
  - BLUE boosts every move to the longest possible (**find a better way to phrase this lmao)
