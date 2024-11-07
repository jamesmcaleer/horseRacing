# Horse Racing 🐎
A digital horse racing simulator to continue my grandfather's holiday tradition

<img width="1675" alt="horseracescreenshot" src="https://github.com/user-attachments/assets/00fbb110-128c-4174-ac0e-dc7b88b994f4">

## Controls

When the game starts, you will be in a menu with the generated horses

To **start** the race, press **space**
To **generate** new horses, press **n**

When the race starts, you will see the horses moving

To **restart** the race, press **space**
To **return** to the menu, press **r**


## Installation

To play **Horse Racing Simulator**, follow these installation steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/jamesmcaleer/horseRacing.git
    ```

2. Install pygame
   ```bash
   pip install pygame
   ```

4. Run the project with main.py file



## Odds Simulation

The **ChanceHandler** creates a set of 8 odds (ex: 2:1, 9:1)

8 random speed graphs are generated and sorted

Based on the odds, each horse has a certain percent chance to be given the fastest available speed graph

This way, even a horse with the lowest odds has a chance to win the race

When a horse is picked, the speed graph becomes _unavailable_, the process repeats using the _next_ fastest speed graph and picks another horse

Once this process is complete, the program has 8 _horse skeletons_ but there are no graphics, numbers, or colors attached

## Attaching Assets

The **ActionHandler** is used to generate empties (full horses with no skeletons)

These horses are given a number 1-8, a random fur color, and a random clothing color

These assets are fetched from the assets folder and places on top of eachother

_apply_speeds_ is ran to combine our previously made _skeletons_ with the _empties_

## Graphics

To give the effect that the horses are moving and that a camera is also moving and following these horses, many calculations need to be made in **GraphicsHandler**

The background image containing trees and other background objects is cycled using _move_background_

The horses (along with their extra assets) are moved in tandem with their speed graphs but an offset is applied so that they stay relative to the camera

The finish line's final position is calculated and only displayed when a certain amount of time has passed and it will line up with the first place horse around the middle of the screen

The race is stopped when the first place horse crosses the finish line, a podium is created for the top 3 horses with their names, images, odds, and final times.





