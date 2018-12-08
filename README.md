# FlowState
This is the repository for the Flow State FPV drone racing simulator 


## Simulator Philosophy

This simulator is a true FPV Drone Racing simulator. The goal is to make it look and feel as similar to a standard racing drone as possible. As such, the goal is *not* to make the most HD/GoPro-esque visuals. Instead the focus is on simulating what pilots see through the goggles, static and all! Here are some of the founding principles of this sim for contributors' consideration. 
- Flight feel is #1 priority
  - This means lowest (realistic) possible input latency
  - Option for typical FPV aspect ratio, and resolutions
- Use as a practice tool
  - Lap times should be similar for most pilots/setups/tracks
  - Editable maps with commonly used track elements
- Visual disturbances similar to those found at an FPV racing event
  - realistic video static/interference
- Competitive
  - The sim does not provide significant advantages to those with high end gaming rigs
  - The "sim quads" could be flown "against" real quads, and yield a fair competition
- Field friendly
  - Should be usable with or without internet connection
  - Should function well on adequately powerful laptops


## Contributing

This project uses UPBGE as its game engine. If you would like to contribute, please follow these steps...
1. run ```git clone https://github.com/skyfpv/FlowState.git```, or download from GitHub webpage
2. Install UPBGE from https://github.com/UPBGE/blender
3. In order for you radio to work in the internal player, place a copy of gamecontrollerdb.txt in ```YOUR_UPBGE_FOLDER/2.79/datafiles/gamecontroller```
4. Open game.blend
