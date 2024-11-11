## GUI REQUIREMENTS

Guide on making ui

---

**Logic & Concept**
> 1. Use PySide6.
> 2. Create seperate `ui.forms` and `ui.pys` of the seperate windows
> 3. __Ensure proper labelling.__
> 3. Import all as classes into one `ui_functions.py`.
> 3. All individual windows are loaded into one single window, using a `StackedWidget`.
> 4. create all functions in the py file. also create a main function for testing.
> 5. The main class must make instances of other expected modules.
> 6. other functions may be created to achieve the desired output. as long as the public functions are similar

**UI function Requirements**
main ui
> - `class(sound, lock, nav2, server, load)`
> - 
>
---

## SPECIFICS

Specific ui details may be confirmed later on the development phase...

---

**Password Window**
> ClassName: _unimportant yet_\
> Objects:
> - 0_bt        -> button
> - 1_bt        -> button
> - 2_bt        -> button
> - 3_bt        -> button
> - 4_bt        -> button
> - 5_bt        -> button
> - 6_bt        -> button
> - 7_bt        -> button
> - 8_bt        -> button
> - 9_bt        -> button
> - del_bt      -> button
> - confirm_bt  -> button
> - clr_bt      -> button
> - input_tf    -> textfield
> - resp_lb     -> label

**Status Window**
> Objects:
> - bigstat_lb  -> label
> - smlstat_lb  -> label

**Choice Window**
> Objects:
> - qst_lb      -> label
> - note_lb     -> label
> - ys_bt       -> button
> - no_bt       -> button