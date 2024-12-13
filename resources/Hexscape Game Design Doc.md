# HEXscape

## Story/Manifesto

- The player is not given very much to work off of, and must discover why they are tasked with this mission.
- Some lines in the dialogue include:
  - "Where am I?"
  - "What is this?"
  - "What am I doing here?"
  - "I guess all I can do is keep moving..."
  - (*After some momentum is gained, perhaps after restarting from level 1.) "I know I can find a way."
- Emphasis on memory, sounds, attention to details. It's impossible to win just by button mashing.
- The big picture is to gain confidence, and persevere through failure/the unknown. The player will have to embrace it even, as the cornerstone of their progress and growth.
- The player will come to understand that they can't go back on decisions they've made in the past. Although it's nearly impossible to know if they're headed the right way or not, they must keep moving. Keep trying.

## Aesthetics

- Every asset is either hand draw via Aesprite or a primative shape managed via Pyglet.
- The HUD includes:
  - Move counter in the top right corner.
  - Current level in the top left corner.
  - Collected waypoints along the left edge of the screen.
  - Pause button in the bottom right corner.

## Visual FX

- Isometric perspective achieved by a custom projection matrix configuration via Pyglet module `graphics`.
- Parallax effect to center the view on the player.
- Add some 'bumping' animation for running into a wall.
- Ball glows stronger and stronger the closer you are to exiting the level.

## Audio FX

- Add excitement to the music as the player progresses/gains more confidence, such as reaching a certain level or collecting a certain color waypoint. Each color sounds a unique way.
  - needs a good kick drum line
  - snare
  - hihat
  - guitar

## Gameplay Mechanics/Implementation Details

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
