# Hexscape Game Design Document

## 1. __Story/Manifesto__

### Concept

- The player begins in an unknown place and must uncover their purpose through exploration.
- Core narrative themes:
  - __Discovery__: "Where am I?", "What is this?"
  - __Perseverance__: "I know I can find a way."
- The player must embrace failure and the unknown to progress.
- Irreversible decisions drive gameplay tension and realism.

### Goals

- Encourage attention to memory, sound, and details.
- Build confidence through incremental progress.

---

## 2. __Aesthetics and Presentation__

### Visual Design

- __Assets__: Hand-drawn in Aseprite or created as primitives via Pyglet.
- __HUD__:

| Left          | Center        | Right
|---------------|---------------|--------------
| Current Level |               | Move Counter
| Waypoints     | Player        | Controls
| Ability Descriptions |        | Pause Button

### Visual Effects

- __Isometric perspective__: Custom projection matrix in Pyglet.
- __Parallax__: Centers the view on the player.
- __Animations__:
  - "Bumping" animation when running into walls.
  - Glowing around the player intensifies near the exit.

---

## 3. __Audio FX__

### Sound Design

- Dynamic music evolves as the player progresses:
  - __Milestones__: Reaching a level or collecting waypoints triggers new layers.
  - Instruments: Kick drum, snare, hi-hat, guitar.
- Each waypoint color has a unique sound signature.

---

## 4. __Gameplay Mechanics__

### Map and Procedural Maze Generation

#### Requirements

- Maze parameters:
  - Irregular shapes.
  - Loops and rooms.
  - Clear goal and exit.

### Waypoints

#### Functions by Color

| __Color__   | Ability Description | Spawn Rarity
|-------------|---------------------|-------------
| __RED__     | Break walls (limited uses). | 0.2
| __ORANGE__  | Illuminate path to nearest waypoint (temporary). | 0.7
| __YELLOW__  | Highlight nearby tiles and walls (temporary). | 0.9
| __GREEN__   | Reveal all waypoints on the map (temporary). | 1.0
| __PURPLE__  | Teleport within a level-based range of an undiscovered waypoint. | 0.2
| __BLUE__    | Extend moves to maximum distance. | 0.1

---

## 5. __Progress Tracker__

| Feature                        | Status        | Priority    | Notes
|--------------------------------|---------------|-------------|------------------------------------
| Story narrative/dialogue       | Drafted       | Medium      | Test emotional tone.
| HUD design                     | In Progress   | High        | Finalize layout and placement.
| Procedural maze generation     | In Progress   | High        | Debug irregular shapes, loops, sparseness, and multiple goals.  
| Waypoint implementation        | Not Started   | High        | Start with RED and ORANGE.
| Isometric perspective          | Planned       | Low         | Test for visual bugs.
| Sound design (waypoints)       | Not Started   | Medium      | Prototype sound effects.
| Music layering system          | Planned       | Medium      | Compose basic drum and guitar loop
| Wall "bump" animation          | Not Started   | Low         | Explore simple easing animations.
