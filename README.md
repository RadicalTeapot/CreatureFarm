# Creature Farm

## Ideas:
- Player is the hive mind controlling creature
- When starting adventure, creature are created from pool of available genetic material
- While adventuring, creature assimilates enemies to store their genetic material
- If not killed, creature comes back and sacrifices itself to release all stored genetic material in the material pool
- If killed, material is lost (low chance of partial/total recovery by another creature sent to the same adventure)
- Enemy assimilation as well as environment adaptation leads to new genetic abilities when creature is turned back to genetic material

- All text, center panel describes action/creature/....


# TODO
- __Finish load/save code and make a start menu__
- Add options to give creatures potions/food/items before going to adventures to be used in adventure (at cost of inventory space)
- Add min level caps to activities and implement gaining exp when activity is done
- Add fail chance for activities driven by difference between creature level and activity complexity
- Log xp gain, success/fail at end of activities to creature log
- Change way game is drawn (generate a static image for the panel borders and create a Panel.refresh method which redraws only the current tab texture. In Game.draw, draw first the panels textures and then the border overlay)
- Change healing system from food to turn based. More hp take longer to heal. Make food grant bonuses (permanent (mutagen...) or temporary)
- Add some items to increase inventory size of creatures

- Implement an activity log to describe creature activity evolution
- Implement stat effects from food (e.g. +5 strength, -0.2 evasion, ...)
- Reimplement tabs in UI
- Display available adventures/recipe first then rest greyed out based (availability is determined by creature skills and/or inventory contents)
- Improve fight system

# Playtest
