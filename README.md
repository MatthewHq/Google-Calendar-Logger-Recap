# Google-Calendar-Logger


"Quick and Dirty" development speed, no refinement planned from the start.


Creates calendar events representing a logged activity once setup with iPhone shortcuts and Windows OpenSSH in combination with a few batch files and task scheduler.

[![click](https://github.com/MatthewHoque/Google-Calendar-Mover/blob/main/readMeSources/googlecalendarmover.png?raw=true)](https://youtu.be/rCv-Rt_5bC4?t=552)

## Potential Rework Plans / Ideas / Needs
 
 Scenarios
    Visual definitions: 
        X - cached time
        [ - start time
        ] - end time
        K - Input
        N - Now

 1. Completed / Changed activity but did not log at prior time end

    X===[K1====N]
 2. About to log completed activity but last cached time is too early

    [X===K1]======N
 3. Definite complete range?

    [K1===K2]====X===N


 Speed
  - Smart assumption arg dynamic
    - Make default assumptions allowing for optionally less arguments

 
 Control
 - Define new start point
 - Determining event end point 
 - Offline support?



