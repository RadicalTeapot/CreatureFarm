# Mutations

The json file contains the dictionary representing mutation data for the game. Each mutation is indexed by a unique string used as an id for this mutation, use dot to separate concepts (e.g _movement.crawl_). Add flags are optional unless specified.


- `name` *The display name for the mutation (__mandatory__)*
- `required`
    - `knowledge` *The amount of knowledge about this mutation to be able to use it (defaults to 0.0)*
    - `mutations` *A list of mutations that must be present on the creature to be able to use this mutation (defaults to an empty list)*
    - `size` *The minimum size a creature must be to use this mutations (defaults to 0.0)*
- `exclude` *A list of mutation ids to exclude, partial matches can be used (e.g mutation would exclude movement.crawl and movement.quadruped mutations) (defaults to an empty list)*
- `size` *The mutation size itself, added to the creature base size (__mandatory__)*

- `effects` *(__mandatory__)*
    #### Mandatory Flags
    Those flags have to be present for the effect to be valid
    - `target` *Specify the target of the effect*
        - `self` *Affect itself*
        - `allies` *Affect all allies (doesn't include itself)*
        - `allies_self` *Affect all allies (include itself)*
        - `enemies` *Affect all enemies*
        - `all` *Affect all*
    - `activation` *When to activate the effect*
        - `always` *Passive effect, always active*
        - `start_turn` *At the begining of the target's turn*
        - `end_turn` *At the end of the target's turn*
        - `attacked` *When taget is attacked*
        - `killed` *When target killed*
    - `chance` *The chance of the effect to be activated (between 0.0 and 1.0)*

    #### One of the following
    One and only one of those flags have to be present for the effect to be valid
    - `stats` *Change target(s) stats (positive or negative values)*
    - `extra_turn` *Grant an extra turn to the target(s)*
    - `attack` *The target(s) attack*
    - `heal` *The target(s) get healed (between 0.0 and 1.0 of total health)*
    - `block` *The target(s) block the incoming attack (between 0.0 and 1.0 of total damages)*
- `biomass_cost` *The cost of this mutation added to the creature cost (__mandatory__)*
- `description` *Small mutation description displayed as tooltip (__mandatory__)*
