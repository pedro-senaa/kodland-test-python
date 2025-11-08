# What is this

This is a project for Kodland's test for tutors. In this project, I wrote a sample game, where the main ship can walk around with mouse clicks, shoot cannon balls with spacebar, and enemys will spawn every few seconds, trying to get to the player's ship.

## How to run this project
Firstly, I'll consider you already have python installed, as well as already have this project cloned somewhere. You also might want to set up a virtual environment for the dependecies.

- In your terminal with the project folder open, run `pip install -r requirements.txt` for installing all dependecies with correct versions for this project
Do notice only **pgzero** is used, but it requires **numpy** and **pygames**

- Still in your terminal and in the same folder, run `pgzrun main.py`. This will start the game. 

- Play!

## What does this have
There are several files here. Apart from the `READ.md` and other files, here's a summary of this project.

### main.py file
In here is the main code with classes, functionalities and everything else
### /images directory
All the images used in the game (required for **pgzero**)
### /music directory
All music used in the game (required for **pgzero**)
### /sounds directory
All other sounds used in the game (required for **pgzero**)

images and sounds are from [kenney](https://kenney.nl/assets) and music is from [pixabay](https://pixabay.com)



## Next steps!
Even though this is a test for a tutoring job, I'll keep working on this!

- Add new types of enemys
- Add new weapons
- Create auto-shooter system (initial idea was a [vampire survivors](https://store.steampowered.com/app/1794680/Vampire_Survivors)-like gameplay loop)