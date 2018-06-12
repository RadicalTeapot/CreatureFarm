# Creature Farm

## Ideas:
- Player is the hive mind controlling creature
- When starting adventure, creature are created from pool of available genetic material
- While adventuring, creature assimilates enemies to store their genetic material
- If not killed, creature comes back and sacrifices itself to release all stored genetic material in the material pool
- If killed, material is lost (low chance of partial/total recovery by another creature sent to the same adventure)
- Enemy assimilation as well as environment adaptation leads to new genetic abilities when creature is turned back to genetic material
- Knowledge is only gathered when biomass is gathered (creature should return automatically when biomass container is full)
- Creature size (and cost) is determined by number of mutations applied, the bigger the creature the more expansive the mutations (have a global multiplier for applied mutation costs)
- Some applied mutation parts can be shared between mutations (e.g venomous bite shares venom glands with venomous claws)
- Have a mutation designer that can put together knowledges to form new mutations
- All text, center panel describes action/creature/....


# TODO
- __Finish load/save code__
- __Attach the logger to Game__
- Refactor screens to more tightly follow the MVC pattern (split ui and logic in two separate classes)
- Add some mutation to increase biomass container size of creatures
- Change way game is drawn (generate a static image for the panel borders and create a Panel.refresh method which redraws only the current tab texture. In Game.draw, draw first the panels textures and then the border overlay)

- Reimplement tabs in UI
- Display available adventures/mutation first then rest greyed out based (availability is determined by creature skills and/or inventory contents)
- Improve fight system

# Playtest
