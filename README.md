# Creature Farm

## Ideas:
- All text, center panel describes action/creature/....
- Player has no direct control over creature, can just give orders
- Creature must hunt for food
- Stay dead when killed during adventure
- Sleep to restore HP
- Can prepare meals for temp stat increase and healing to be used before or during adventures (e.g creature heals itself when reaching 0 hp while adventure)
- Earns XP, stat levels
- Can make mutagen to mutate and unlock new ablities
- During hunts, can capture new creatures to expand stable
- Choose which creature to send hunt
- Player has to manage stable
- Can mate creatures for mutated offsprings
- Higher level creatures, creatures get needs for special buildings/meals
- Let player hatch eggs and make it look like opening a loot box
- The game is turn based, each creature can do at most one action a day (adventure(last more than one day), research, cook, ...). If not adventuring, they rest for one point at the end of the day.


# TODO
- __Add min level caps to activities and implement gaining exp when activity is done__
- Add fail chance for activities driven by difference between creature level and activity complexity
- Log xp gain, success/fail at end of activities to creature log

- Implement an activity log to describe creature activity evolution
- Implement weapons and armor
- Implement stat effects from food/armor/weapon (e.g. +5 strength, -0.2 evasion, ...)
- Change creatures stats to fit a skill based system (e.g. cooking, crafting, strength, marksmanship, sword wielding...)
- Reimplement tabs in UI (when a panel has multiple tabs, show arrows at the bottom right of it letting the user switch tabs)
- Display available adventures/recipe first then rest greyed out based (availability is determined by creature skills and/or inventory contents)
- Improve fight system
- Switch ids to string and use . notation (e.g. : item.weapon.sword, recipe.cooked_meat, ...)

# Playtest
