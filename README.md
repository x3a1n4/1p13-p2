# 1p13 p2
This is our code for 1p13 Project 2. In this project, a QArm (from quanser) must pick up our designed containers and drop them off at their corresponding autoclave positions.

The provided "Common" folder must be in same-level folder as repository

# Instructions
Left potentiometer must start at a position greater than threashold, by default 50%

The arm will pick up the container and return to home. Control movement incrementally with right potentiometer
To end rotation phase, move left potentiometer below threshold. If arm is facing autoclave, it will move on to placement phase.

Once arm enters placement phase, movement is controlled with left potentiometer. Move the potentiometer between 50% and 100% for position 1, move to 100% for position 2 (position 1 is in autoclave, position 2 is on top of autoclave). The arm will place the container accordingly.
