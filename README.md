# Drone Backyard Flyer 

![video](./movie.gif)


## Objective 

- Command the drone to autonomously fly a 10 meter box at a 3 meter altitude in Unity envrionment

## Approach

- This uses [UdaciDrone API](https://udacity.github.io/udacidrone/) to control the drone
- Set next target location to move to, and after confirming the location is close to the target location (the gap of x, y, z is smaller than accepted distance), set the next target location

## Result

- The drone could fly a 10 meter box 
- See the video above (full video is movie.mp4 in this repository)

## How to run
- Download the Simulator [from this repository](https://github.com/udacity/FCND-Simulator-Releases/releases).
- Set up Conda envrionment seeing [this repository](https://github.com/udacity/FCND-Term1-Starter-Kit) and activate it ('source activate fcnd')
- Run following `python backyard_flyer.py` 

