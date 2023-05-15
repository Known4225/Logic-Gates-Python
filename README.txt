Welcome to Logic Gates™

download files and run 

python3 logicgates.py

You can add -f and a filename to load in a file

Create logic circuits by summoning components with keybinds and click and drag mechanics to wire and rearrange components.
This project has support for 8 types of unique components with all the infinite possibilities of functional completeness

The full list of keybinds:
1, e, p - POWER component (input/output)
2, w, n - NOT gate
3, a - AND gate
4, q, o - OR gate
5 - XOR gate
6 - NOR gate
7 - NAND gate
8 - BUFFER gate
x - delete component
click + drag - move components or screen
space + click + drag - create wire
s + click + drag - select
s + click - add component to selection
c - copy/paste selected
scroll wheel (or up and down arrows) - zoom
up and down arrows - zoom
space + scroll wheel - rotate component (coarse)
sideways arrows - rotate component (fine)
space + sideways arrows - rotate selected (fine)
k - export
l - import (it's L and not i)
h - toggle sidebar

All the data for a Logic Gates™ setup is in just 5 lists, some of which store redundant information. File sizes are around 60 bytes per component.

NOT POWER POWER 0 0 90 -80 50 90 80 -50 90 0 0 1 0 0 0 1 0 0 1 2 0 1 0 0 1 1 0 1 3 1 2 1 0

ToDo: 
Undo/Redo commands (very difficult, might require compact encoding)
Configurable keybinds - possibly just in code
User interface/Sidebar - might be unecessary
Custom gate creator
Multiplexer component
Triple (or more) input gates (currently incompatible with implementation, would require large reworks)

Update 26.01.23:
Added linux support
New keybinds for scrolling (linux support, but I ended up getting the scroll wheel to work on linux anyway)
Tps variable (change your fps and tps)
A fix for linux keyRelease events (buffer key system)
scrollSpeed and rotateSpeed variables
new streamlined key sensing (not applied universally, since the shift key was not having issues)

Issue:
Buffers don't work too well with high tps, but lowering the tps causes lag
Fix: just use the JS version
