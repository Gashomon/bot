## CONTROL REQUIREMENTS

Guide on making flow

---

**Logic & Concept (Deliver)**
> 1. Bot waits 
> 2. User send data (currently via bot)
> 3. Bot receives full order details
> 3. bot travels 
> 3. bot asks confirmation to user
> 4. user confirms & loads
> 5. bot checks weight. proceeds
> 6. bot confirms, then goes home

**UI function Requirements**
main ui
> **constructor**
> - `mainclass(modules nav2, server, ui)`

> **objects**
> - module          -> module functions: consists of lock, load, sound
> - server          -> server class: app to bot comm
> - nav2            -> navigation class: robot navigator
> - ui              -> ui class: consists of all ui
> - Transac         -> defined class
> - destinations    -> dictionary

> - situation   -> enum class
> - currentpass -> string

> **functions**
> - void `lockon()`                 -> depends `setlock(lockstate)`
> - void `lockoff()`                -> depends `setlock(lockstate)`
> - bool `checkdoor()`              -> depends `getdoorstate()`
> - void `playfor(situation)`       -> depends `playonce(audio)` and `playloop(audio, trigger)`
> - bool `checkload(limit)`         -> depends `getLoad()`
> - Transac `getcmd()`              -> depends `waitforcmd()`
> - void `run(transac)`             
> - void `deliver(transac)`         -> depends `createPoseStamped(x, y, rot)` and `waittillsuccess(fnc())`
> - void `main()`     
