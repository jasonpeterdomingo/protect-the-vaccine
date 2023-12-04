# protect-the-vaccine
## Author
Jason Domingo: jayprdom@udel.edu

## Description
*Protect the Vaccine* is a game where the scientist has to protect the vaccine from zombies.

## About
*Protect the Vaccine* is a game where the scientist has to protect the vaccine from the zombies 
spawning from all 4 sides of the screen. The zombie's goal is to either chase the player or the vaccine, whichever is 
closer. If any of the zombies touch the scientist or the vaccine, the vaccine will be contaminated, thus, 
ending the game. The scientist will shoot their laser to kill the zombies. Also, the player cannot walk over the 
vaccine and has to surround it to protect it. There is a random chance the zombie will drop a power-up when killed. 
The apple increases the scientist's speed while the star increases the size of their lasers. Every 10 seconds, the 
zombies will scale in difficulty: faster, stronger, and larger quantity. When the timer runs out, the player wins.


## Preview
#### YOUTUBE LINK: https://youtu.be/8QwdTDLnzOU?si=CnmlRFcF9T2dJum0


## Instructions
- <b>Moving:</b> The scientist can move up, down, left, and right by pressing "w", "s", "a", "d" respectively.
- <b>Shooting:</b> Press the space bar. The laser will shoot in the last direction the user inputs.
- <b>Diagonal Shooting</b> Press "q", "e", "z", and "x" to shoot up-left, up-right, down-left, and down-right


## Acknowledgements
- https://designer-edu.github.io/designer/students/docs.html
- https://designer-edu.github.io/designer/examples/examples.html
- https://docs.python.org/3/library/math.html
- https://www.w3schools.com/python/ref_string_format.asp


## Tasks
### Phase 1
#### YOUTUBE LINK: https://youtu.be/2cLohY3uw3Y
- [x] <b>Create Game</b>: Create the square grid where the game takes place
- [x] <b>Scientist Exists</b>: There is a scientist on screen
- [x] <b>Scientist Moves</b>: move up, down, left, and right when the user presses 'W', 'S', 'A', and 'D' respectively
- [x] <b>Laser</b>: When the user hits the space bar, a laser comes out. Laser disappears when it hits offscreen
- [x] <b>Limit Screen</b>: Scientist cannot walk offscreen
- [x] <b>Zombie Appears</b>: There is a zombie that spawn randomly from all 4 sides of the screen

### Phase 2
#### YOUTUBE LINK: https://youtu.be/mvnHIdMObQ4?si=t1Txsrf769af3cIK
- [x] <b>Laser Direction</b>: Laser shoots the direction the scientist faces
- [x] <b>Zombie Disappears</b>: The zombies disappear when they are hit by the laser
- [x] <b>Laser Disappears</b>: Laser disappears when it hits a zombie
- [x] <b>Create Vaccine</b>: Create the vaccine in the middle of the screen
- [x] Make it so that the scientist cannot walk over the vaccine
- [x] <b>Zombie Moves</b>: The zombies follow the vaccine (need to modify to follow whichever is closer)
- [x] <b>Game Pauses</b>: If the zombie touches the scientist or the vaccine, the game pauses

### Phase 3
- [x] <b>Zombie Follows</b>: The zombies follow the scientist or the vaccine (whichever is closer)
- [x] <b>Shoot Lasers Diagonally</b>: bullets can be shot diagonally when pressing certain keys
- [x] <b>Item Drop</b>: Create a random chance the zombies will drop a special item (make the player faster, bigger lasers)
- [x] <b>Timer</b>: Add the timer
- [x] <b>Timer runs out</b>: When timer runs out, a "You Won" screen appears
- [x] <b>Score Increase</b>: Add a score that increases every 10 seconds
- [x] <b>Game Over Screen</b>: Add the "Game Over" screen when you die/vaccine gets touched
- [x] <b>Display Stats on Screen</b>: Display the score and time left
- [x] <b>Scale</b>: As timer runs out, increase difficulty (faster zombies, need to be hit multiple times)