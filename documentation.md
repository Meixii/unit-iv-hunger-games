# EvoSim Project

**Project:** Evolve or Perish: AI-Driven Animal Survival in a Neural Network Battle Royale  
**Date:** September 19, 2025  
**Objective:** To outline the core mechanics, calculations, parameters, map design, and events for the simulation.
**Link:** [Google Docs](https://docs.google.com/document/d/1qrMfD3UcS5KcEVAf6wdcfgbe8y7ELfNu2IIqW7OwYTg/edit?tab=t.0#heading=h.10am4qwgcy2r)

## Section I: Terminologies

*A dictionary of key concepts used throughout the project.*

- **Crossover:** A process in the Evolutionary Algorithm where the MLP weights of two parent animals are combined to create the MLP for a new offspring.
- **Disaster:** A large-scale, negative event that affects a large area of the map or the entire simulation for a period of time (e.g., Wildfire, Harsh Winter).
- **Effect (Buff/Debuff):** A temporary modifier applied to an animal that alters its Traits or Status for a limited duration (e.g., 'Poisoned', 'Well-Fed').
- **Elitism:** A selection strategy in the Evolutionary Algorithm where a small percentage of the most successful animals (the "elites") from one generation are carried over to the next generation unchanged.
- **Evolutionary Algorithm (EA):** The training method used to optimize the MLP. It mimics natural selection by creating a population of animals, evaluating their performance via a Fitness Function, and "breeding" the most successful ones to create the next generation.
- **Fitness Function:** The specific formula used to calculate an animal's success score at the end of a simulation round. This score determines its likelihood of passing its traits to the next generation.
- **Generation:** A complete cycle of the simulation. A population of animals lives, dies, and the most successful ones are used to create a new, potentially improved population for the next generation.
- **Movement Event:** The core, AI-driven phase of the simulation where each animal's MLP makes a decision and performs an action, such as moving, eating, or resting.
- **Multi-Layer Perceptron (MLP):** A type of artificial neural network that acts as the "brain" for each animal, making decisions based on inputs (like Hunger, Thirst, nearby threats) to produce outputs (like moving, eating, fighting).
- **Mutation:** A process in the Evolutionary Algorithm where small, random changes are applied to an offspring's MLP weights to introduce new genetic diversity into the population.
- **Neuroevolution:** The process of using an evolutionary algorithm to train a neural network, which is the core concept of this project.
- **Passive:** An innate, category-specific ability that is always active for an animal (e.g., a Carnivore's Ambush Predator ability).
- **Random Event:** A simulation-wide event that affects all animals and the environment for one week (e.g., Drought, Resource Bloom).
- **Selection:** The process within the Evolutionary Algorithm of choosing which animals from a generation will become parents for the next, based on their fitness scores.
- **Status:** A dynamic, moment-to-moment variable reflecting an animal's well-being (e.g., Health, Hunger, Energy). These are the primary inputs for the MLP.
- **Trait:** A core, semi-permanent genetic attribute of an animal (e.g., Strength, Agility). These are the values the EA will tune over generations.
- **Triggered Event:** An automated, situational scenario that occurs when specific conditions are met, presenting a unique challenge or opportunity for an animal's MLP to solve (e.g., Animal Encounter, Sudden Threat).
## Section II: MLP & Evolutionary Algorithm Design

*This section will detail the technical architecture of the neural network and the mechanics of the genetic algorithm.*

### A. Multi-Layer Perceptron (MLP) Architecture

The MLP serves as the decision-making core for each animal. Its weights and biases are the "genes" that will be evolved.

#### 1. Input Layer
The sensory information provided to the MLP. It's a flattened vector of normalized values (0.0 to 1.0) representing:

- **Internal Status (5 nodes):** Health %, Hunger %, Thirst %, Energy %, and Instinct (0 for Calm, 1 for Alert).
- **Sensory Grid (Perception-based):** A 3x3 grid of tiles centered on the animal. For each of the 9 tiles, the following data is included:
  - Is it a threat? (e.g., Fire, Flood) (1 node)
  - Is there a food source? (1 node)
  - Is there a water source? (1 node)
  - Is there another animal? (1 node)

**Total Input Nodes:** 5 (Internal) + 9 tiles * 4 data points/tile = 41 nodes.

#### 2. Hidden Layers
The processing layers of the network. To adhere to project limitations while providing sufficient complexity, the architecture will be:

- **Hidden Layer 1:** 16 neurons with a ReLU activation function.
- **Hidden Layer 2:** 12 neurons with a ReLU activation function.

#### 3. Output Layer
The layer that determines the animal's action. The neuron with the highest activation value is the chosen action for the turn.

**Output Actions (8 nodes):**
- Move North
- Move East
- Move South
- Move West
- Rest (Conserve/Regain Energy)
- Eat (If food is on the current tile)
- Drink (If adjacent to a water tile)
- Attack (If another animal is on the current tile)

**Activation Function:** Softmax, to ensure a clear "choice" among the possible actions.

### B. Evolutionary Algorithm (EA) Mechanics

This is the process for training the population of MLPs across generations.

#### 1. Initialization
For Generation 0, a population of animals is created. Each animal is assigned an MLP with its weights and biases initialized to small, random values.

#### 2. Evaluation
The entire simulation is run for a fixed number of "weeks." As each animal perishes or when the simulation ends, its performance is calculated using the Fitness Function.

#### 3. Selection
The top-performing animals are selected to become "parents" for the next generation.

- **Elitism:** The top 10% of the population (based on fitness score) are automatically carried over to the next generation unchanged.
- **Tournament Selection:** To fill the remaining 90% of the new population, pairs of "parents" are chosen. A small group of animals (e.g., 5) is randomly selected from the previous generation, and the one with the highest fitness score in that group wins the "tournament" and is chosen as a parent.

#### 4. Crossover (Reproduction)
For each new offspring, two parents selected via the tournament are combined.

**Method:** The weights of both parent MLPs are flattened into single arrays. A random crossover point is chosen. The offspring inherits all weights before the crossover point from Parent A and all weights after the point from Parent B.

#### 5. Mutation
To introduce new genetic diversity, the offspring's MLP weights are slightly and randomly altered.

**Method:** For each weight in the offspring's network, there is a small mutation chance (e.g., 2%). If mutation occurs, a small random value (from a Gaussian distribution) is added to the existing weight.
## Section III: Fitness Function & Generational Goals

*This section defines the precise formula for calculating an animal's fitness and the high-level objectives for each evolutionary generation.*

### A. Fitness Function Rationale

The goal of the fitness function is to provide a single, quantitative measure of an animal's success. This value guides the Evolutionary Algorithm by rewarding beneficial strategies and behaviors. The formula is:

```
Fitness Score = (Time Survived * W_Time) + (Resources Gathered * W_Resource) + (Kills * W_Kills) + (Distance Traveled * W_Distance) + (Events Survived * W_Events)
```

- **Time Survived:** The most crucial component. It directly rewards the primary objective of survival. An animal that learns to effectively manage its needs and avoid danger will live longer and thus have a higher base fitness.
- **Resources Gathered:** This incentivizes the MLP to learn proactive behaviors. It's not enough to simply hide; an animal must actively seek out food and water to replenish its status, and this term rewards that efficiency.
- **Kills:** This component is essential for making the Carnivore category viable. It provides a significant fitness boost for successful predatory behavior, encouraging the evolution of effective hunting strategies.
- **Distance Traveled:** This provides a minor incentive for exploration. It is designed to prevent passive strategies (e.g., an animal finding one resource patch and never leaving) from becoming dominant, encouraging the MLP to learn to navigate the wider world.
- **Events Survived:** This rewards adaptability. By providing a fitness bonus for successfully navigating Triggered Events, we encourage the evolution of more flexible and "intelligent" MLPs that can handle unexpected situations.

### B. Generational Goals

These are the high-level objectives we aim to observe as the simulation progresses through multiple generations.

#### Primary Goal
**Increase Average Fitness.** The main indicator of successful learning is a clear upward trend in the average fitness score of the population from one generation to the next.

#### Secondary Goals
- **Observe Adaptation:** We expect to see the population's average traits shift in response to environmental pressures. For instance, in a world with frequent "Harsh Winter" disasters, animals with higher Endurance should have higher fitness scores, leading to a gradual increase in the average Endurance of the population over generations.
- **Promote Specialization:** Each animal category should develop distinct, successful strategies. Carnivores should evolve MLPs that are adept at hunting. Herbivores should evolve MLPs that excel at locating plants and evading threats. Omnivores should evolve flexible MLPs that can switch between scavenging, grazing, and opportunistic hunting.
## Section IV: Core Mechanics

*This section details the fundamental systems of the simulation, such as the simulation loop, action resolution, and resource/combat mechanics.*

### A. Simulation Flow

This defines the high-level sequence of the entire simulation from start to finish.

#### 1. Preparation Stage
The one-time setup at the very beginning of a simulation run.

- **Character Selection & Initial Training:** Players choose an animal category and answer 5 questions to receive a +1 bonus to specific traits. This is the only point of direct player intervention.
- **World & Population Generation:** The grid map, terrain, resources, and the initial population of animals (Generation 0) are created based on the parameters in Sections VII and IX.

#### 2. Generational Loop
The simulation proceeds in generations. Each generation consists of a full "Hunger Games" style survival scenario. The loop is as follows:

1. Run the Weekly Cycle until a single animal survives or a maximum number of weeks is reached.
2. Calculate the final Fitness Score for every animal that participated.
3. Perform the Evolutionary Algorithm steps (Selection, Crossover, Mutation) to create the population for the next generation.
4. Reset the world and spawn the new population.
5. Repeat.

#### 3. Weekly Cycle
Within a generation, time progresses in weeks. Each week consists of a series of events.

- **Week 1 (Fixed Order):** Movement, Triggered Event, Random Event, Disaster, Triggered Event, Movement, Triggered Event.
- **Subsequent Weeks:** The order and frequency of events are randomized to ensure unpredictability.

### B. Turn & Action Resolution (Within a Movement Event)

To ensure fairness, each Movement Event is resolved in distinct phases, preventing animals that act earlier from having an unfair advantage.

#### 1. Decision Phase
Every living animal's MLP is fed its current sensory inputs. Each MLP processes this information and outputs a chosen action (e.g., "Move North," "Eat"). All decisions are stored without being executed yet.

#### 2. Status & Environmental Phase
Before actions are taken, passive changes are applied to all animals simultaneously.

- Hunger and Thirst depletion.
- Health loss from debuffs like 'Poisoned'.
- Passive Energy regeneration.

#### 3. Action Execution Phase
The stored actions are executed in a specific order of priority:

- **Priority 1 (Stationary Actions):** 'Rest', 'Eat', 'Drink', 'Attack'. These are resolved first.
- **Priority 2 (Movement Actions):** All 'Move' actions are resolved. If two animals attempt to move into the same empty tile, the one with the higher Agility succeeds, while the other's move fails (consuming no energy). If an animal moves onto a tile occupied by another, an 'Animal Encounter' is triggered.

#### 4. Cleanup Phase
Any new effects are applied (e.g., 'Well-Fed' after eating), and expired effects are removed.

### C. Resource Dynamics

- **Spawning:** Resources are placed on the map during World Generation. When a resource is fully consumed, it has a small chance to respawn in a valid location after a set number of weeks, preventing the map from becoming permanently barren.
- **Consumption:** Resources have a set number of "uses." For example, a Plant resource might have 2 uses, restoring 40 Hunger each time before it disappears.

### D. Combat Mechanics

#### Initiation
Combat is initiated when an 'Animal Encounter' is triggered. The MLPs of both animals then make a choice based on their sensory input: 'Attack' or one of the 'Move' actions (to flee).

#### Resolution
- If both animals choose 'Attack', they engage in combat. Damage is exchanged simultaneously based on the formula in Section V. Combat continues in subsequent turns until one is defeated or chooses to flee.
- If one animal chooses 'Attack' and the other chooses 'Flee', the attacker gets one free attack (the defender's AGI is not subtracted for this first strike). The fleeing animal then attempts to move to an adjacent tile.
- If both choose 'Flee', they both move away in their chosen directions.
## Section V: Parameters and Variables

*This section will list and define the key attributes for animals, the environment, and the simulation itself, like health points, sensor ranges, and resource density.*

**Brainstorming (2025-09-18)**

### Animal Categories
The foundational archetypes for our creatures.

- Herbivore
- Carnivore
- Omnivore

### Traits
Core genetic attributes that define an animal's capabilities (Scale: 1-10). These will be the values the evolutionary algorithm tunes.

- **Strength (STR):** Influences combat damage.
- **Agility (AGI):** Affects movement speed, evasion, and energy efficiency.
- **Intelligence (INT):** Could influence learning rate or effectiveness in Triggered Events.
- **Endurance (END):** Determines base Health and Energy pools.
- **Perception (PER):** Affects the range at which an animal can detect resources or other animals.

### Primary Traits & Bonuses
To ensure each animal is unique while maintaining a category advantage, traits are randomized within specific ranges upon creation.

- **Standard Trait Range:** A random integer between 4 and 6 (inclusive).
- **Primary Trait Range:** A random integer between 7 and 9 (inclusive).

#### Trait Distribution Logic
- **A Carnivore's primary trait is Strength.** Its STR will be randomized between 7-9, while all its other traits (AGI, INT, END, PER) will be individually randomized between 4-6.
- **A Herbivore's primary trait is Agility.** Its AGI will be randomized between 7-9, while its other traits will be individually randomized between 4-6.
- **An Omnivore's primary trait is Endurance.** Its END will be randomized between 7-9, while its other traits will be individually randomized between 4-6.

### Status
Dynamic variables reflecting an animal's current well-being. These are critical inputs for the MLP.

- **Health:** Animal's life force. If it reaches 0, the animal perishes. Calculated as 100 + (Endurance * 10). Does not regenerate passively.
- **Hunger:** Scale of 0-100. Decreases with every turn. At 0, the animal begins to starve and loses health.
- **Thirst:** Scale of 0-100. Decreases with every turn, typically faster than hunger. At 0, the animal becomes dehydrated and loses health at a severe rate.
- **Energy:** Consumed by actions. Replenished by resting or passively at a slow rate. Calculated as 100 + (Endurance * 5). Reaching 0 causes Exhaustion.
- **Instinct (Danger Level):** A state (e.g., Calm or Alert). Becomes "Alert" when health is low, a predator is nearby, or during a disaster. This state is a direct input to the MLP to influence its decision-making priorities (e.g., flee vs. eat).

### Passives & Effects
Modifiers that influence Traits or Status.

#### Passives
Innate, category-specific abilities that are always active.

- **Carnivore - Ambush Predator:** The first attack against another animal in an encounter deals bonus damage. This incentivizes hunting over prolonged fights.
- **Herbivore - Efficient Grazer:** Gains 25% more Hunger and Energy from any plant-based food source. This allows them to spend less time eating and more time moving or hiding.
- **Omnivore - Iron Stomach:** Has a high resistance to negative effects from food or water sources (e.g., "Sick" or "Poisoned"). This makes them excellent scavengers and adaptable survivors.

#### Effects (Buffs/Debuffs)
Temporary modifiers from the environment or interactions. These have a duration (e.g., number of turns).

##### Good Effects (Buffs)
- **Well-Fed:** Temporary +1 STR, +1 END. (Trigger: Hunger > 90%)
- **Hydrated:** Temporary +1 AGI, faster passive energy regeneration. (Trigger: Thirst > 90%)
- **Rested:** Significant boost to energy regeneration for 3 turns. (Trigger: Taking the 'Rest' action)
- **Adrenaline Rush:** +2 STR, +2 AGI for 2 turns, but energy drains faster. (Trigger: Quick Event or low health)

##### Bad Effects (Debuffs)
- **Injured:** -2 AGI until healed. (Trigger: Taking significant damage)
- **Poisoned:** Lose a fixed amount of health per turn for 5 turns. (Trigger: Eating a poisonous plant, disaster)
- **Exhausted:** Energy regeneration is halved. (Trigger: Energy drops to 0)
- **Sick:** -1 to all traits. (Trigger: Drinking from contaminated water)
## Section VI: Map and Objectives

*This section details the design of the grid-based map, including terrains, resource distribution, and the ultimate win/loss conditions for the animals.*

### Map Structure
The world is a pre-designed, grid-based environment. The coordinate system allows for precise tracking of all entities.

### Terrain Types & Effects
Each grid cell has a terrain type that directly impacts gameplay.

- **Plains:** The standard terrain.
  - *Effect:* No bonus or penalty. Movement cost is normal. Standard resource density.
- **Forest:** Dense woodland.
  - *Effect:* Increased movement cost (x1.5). Provides a "Hidden" status, preventing detection from animals more than 2 tiles away. High density of plant-based food.
- **Jungle:** A more extreme and dangerous forest.
  - *Effect:* High movement cost (x2.0). High chance of encountering poisonous plants. Very high density of rare, high-value plants.
- **Water (River/Lake):** A source of hydration.
  - *Effect:* Cannot be moved onto, but animals on adjacent tiles can drink. Acts as a natural barrier.
- **Swamp:** Fetid marshland.
  - *Effect:* Increased movement cost (x1.8). Each turn spent in a swamp tile has a 10% chance to inflict the Sick debuff. Contains unique scavenging opportunities for Omnivores.
- **Mountains:** Impassable rock.
  - *Effect:* Acts as a permanent wall, blocking movement and line of sight.

### Resource Distribution
Resources are strategically placed based on terrain.

#### Food
- **Plants (Herbivore/Omnivore):** Spawn with high frequency in Forests and Plains. Rare, high-nutrient plants spawn only in Jungles.
- **Prey (Carnivore):** Small AI creatures spawn and move randomly within Plains tiles.
- **Carcasses (Omnivore/Carnivore):** Have a chance to appear after an animal is defeated or during certain events. More common in Swamps.

#### Water
Spawns in clusters to form Lakes and lines to form Rivers.

### Objectives & Win Conditions
The ultimate goal is to produce the most "fit" animal for the next generation.

#### Primary Objective (Winning a Round)
Be the last animal standing.

#### Secondary Objective (Driving Evolution)
Achieve the highest possible Fitness Score. This score, calculated at the moment of an animal's death (or the end of the simulation), determines its evolutionary success.

#### Fitness Score Calculation
```
Fitness Score = (Time Survived * W_Time) + (Resources Gathered * W_Resource) + (Kills * W_Kills) + (Distance Traveled * W_Distance) + (Events Survived * W_Events)
```

#### Weights (W)
These values are critical for balancing what the algorithm prioritizes.

- **W_Time:** Rewards longevity and endurance.
- **W_Resource:** Rewards efficient resource management.
- **W_Kills:** Heavily rewards aggressive, successful carnivore behavior.
- **W_Distance:** Lightly rewards exploration to discourage overly passive strategies.
- **W_Events:** Rewards adaptable decision-making in special circumstances.
## Section VII: Preparations, Events and Disasters

*This section will cover the random environmental challenges that will test the animals' adaptability, such as storms, meteors, and resource depletion.*

**Brainstorming (2025-09-18)**

### Preparations Stage
The initial setup phase before the simulation begins.

1. **Animal Selection:** Players choose one of the three categories (Herbivore, Carnivore, Omnivore).
2. **Initial Training:** Players answer 5 questions. The chosen trait in each question receives a permanent +1 bonus. (This is the only point of direct player intervention.)
3. **World & Population Generation:** After training, the world is procedurally generated.
   - **Map Generation:** A grid is created. Each tile is assigned a terrain type based on a percentage distribution (e.g., using a simple randomizer or a more advanced algorithm like Perlin noise for clustering).
   - **Resource Spawning:** Food and Water sources are placed on the map according to terrain rules (e.g., Water tiles cluster to form lakes, Food tiles spawn in Plains/Forest but not Mountains).
   - **Animal Spawning:** Each animal is placed on a random, valid 'Plains' tile, ensuring no two animals start on the same or adjacent tiles.

### Movement Event
**Frequency:** 2 per week

This is the core AI-driven action phase.

- **Mechanic:** The MLP for each animal makes a decision based on its current Status and environmental inputs.
- **Potential Actions:** Move towards detected food/water, hunt a nearby animal, flee from a threat, or do nothing to conserve energy.

### Triggered Events
**Frequency:** 3 per week

Automated, situational scenarios. A random event is chosen from the list below when triggered.

#### List of Triggered Events
- **Animal Encounter:** Two animals move onto the same tile. The MLP for each decides "Fight" or "Flee".
- **Resource Scarcity:** An animal arrives at a resource tile with one use left. The MLP decides whether to take the small reward or move on.
- **Sudden Threat (e.g., Rockslide):** A localized threat appears. The MLP decides to attempt an escape (Agility check) or hide (Endurance check).
- **Curious Object:** An unusual object is discovered. The MLP decides to investigate (Intelligence check for a buff) or ignore it.

### Random Events
**Frequency:** 1 per week

Simulation-wide occurrences. A random event is chosen from the list below at the start of the week.

#### List of Random Events
- **Migration:** A random map quadrant becomes a "Lush Zone" for the week.
- **Resource Bloom:** A specific resource type spawns at double the rate across the map.
- **Drought:** Half of all water source tiles become inactive for the week.
- **Predator's Frenzy / Grazing Season:** A global +1 STR buff for Carnivores or +1 AGI for Herbivores for one week.

### Disasters
**Frequency:** 1 per week

Large-scale, negative events. A random disaster is chosen from the list below.

#### List of Disasters
- **Wildfire:** Affects all 'Forest' terrain cells.
- **Contamination:** A random water source becomes permanently contaminated.
- **Flood:** Affects all tiles adjacent to water sources.
- **Earthquake:** Changes some 'Plains' tiles to 'Difficult Terrain' and may cause the Injured debuff.
- **Harsh Winter:** Lasts for a full week. Doubles Hunger/Thirst depletion and gives a -1 Agility penalty.
## Section VIII: Quantitative Mechanics & Balancing

*This section centralizes all numerical values for easy tuning and reference.*

### World Generation Parameters
- **Grid Size:** 25x25 tiles.

#### Terrain Distribution
- Plains: 60%
- Forest: 25%
- Water: 10%
- Mountains (Impassable): 5%

#### Resource Density
- **Food Source Chance (per valid tile):** 15%
- **Water Source Chance (per valid tile):** 5% (Note: Water often clusters)

### Animal Parameters
- **Standard Trait Range:** Random integer between 4-6.
- **Primary Trait Range:** Random integer between 7-9.
- **Initial Training Bonus:** +1 to a chosen trait per question (5 total bonus points).

### Status Dynamics (per MovementEvent)
- **Hunger Depletion:** -5
- **Thirst Depletion:** -8
- **Passive Energy Regen:** +10
- **Starvation Damage (Hunger = 0):** -5 Health per turn.
- **Dehydration Damage (Thirst = 0):** -10 Health per turn.

### Passive & Effect Modifiers
- **Carnivore - Ambush Predator:** First attack damage multiplied by 1.5.
- **Herbivore - Efficient Grazer:** All food gains multiplied by 1.25.
- **Omnivore - Iron Stomach:** 50% chance to ignore Sick or Poisoned debuffs from resources.

#### Buffs (Default Duration: 3 turns)
- **Well-Fed:** +1 STR, +1 END
- **Hydrated:** +1 AGI
- **Adrenaline Rush:** +2 STR, +2 AGI, Action energy costs * 1.5. (Duration: 2 turns)

#### Debuffs (Default Duration: 5 turns)
- **Injured:** -2 AGI
- **Poisoned:** -5 Health per turn
- **Exhausted:** Passive energy regeneration is halved.
- **Sick:** -1 to all traits.

### Event & Disaster Mechanics
- **Triggered Event - Resource Scarcity Gain:** +10 Hunger/Thirst.
- **Disaster - Harsh Winter:** Hunger/Thirst depletion x2. All animals get -1 Agility for the week.

### Fitness Score Weights
- **Time Survived (per turn):** 1
- **Resources Gathered (per 40 units):** 5
- **Kills:** 50
- **Distance Traveled (per tile):** 0.2
- **Events Survived:** 10
## Section IX: Code Implementation Constants

*This section provides a direct translation of the parameters in Section VIII into a format suitable for a configuration or constants file in Python. This centralizes all "magic numbers" for easy tweaking during development.*

```python
# World Generation
GRID_WIDTH = 25
GRID_HEIGHT = 25
TERRAIN_DISTRIBUTION = {'Plains': 0.60, 'Forest': 0.25, 'Water': 0.10, 'Mountains': 0.05}
FOOD_SPAWN_CHANCE = 0.15
WATER_SPAWN_CHANCE = 0.05
TERRAIN_MOVEMENT_MODIFIERS = {'Plains': 1.0, 'Forest': 1.5, 'Jungle': 2.0, 'Swamp': 1.8}
SWAMP_SICKNESS_CHANCE = 0.10

# Animal Parameters
STANDARD_TRAIT_MIN = 4
STANDARD_TRAIT_MAX = 6
PRIMARY_TRAIT_MIN = 7
PRIMARY_TRAIT_MAX = 9
BASE_HEALTH = 100
HEALTH_PER_ENDURANCE = 10
BASE_ENERGY = 100
ENERGY_PER_ENDURANCE = 5
INITIAL_TRAINING_POINTS = 5

# Status Dynamics
HUNGER_DEPLETION_RATE = 5
THIRST_DEPLETION_RATE = 8
PASSIVE_ENERGY_REGEN = 10
STARVATION_DAMAGE = 5
DEHYDRATION_DAMAGE = 10

# Action Costs & Gains
MOVEMENT_BASE_COST = 10
MOVEMENT_AGILITY_MULTIPLIER = 0.5
REST_ENERGY_GAIN = 40
PLANT_FOOD_GAIN = 40
PREY_FOOD_GAIN = 50
DRINKING_THIRST_GAIN = 40

# Combat
STRENGTH_DAMAGE_MULTIPLIER = 2
AGILITY_EVASION_MULTIPLIER = 5

# Passives & Effects
AMBUSH_PREDATOR_MULTIPLIER = 1.5
EFFICIENT_GRAZER_MULTIPLIER = 1.25
IRON_STOMACH_RESISTANCE_CHANCE = 0.50
DEFAULT_BUFF_DURATION = 3
DEFAULT_DEBUFF_DURATION = 5
POISON_DAMAGE_PER_TURN = 5

# Events & Disasters
RESOURCE_SCARCITY_GAIN = 10
ROCKSLIDE_ESCAPE_DC = 14
ROCKSLIDE_HIDE_DC = 12
ROCKSLIDE_DAMAGE = 15
CURIOUS_OBJECT_DC = 13
MIGRATION_ENERGY_BONUS = 15
RESOURCE_BLOOM_MULTIPLIER = 1.5
DROUGHT_WATER_REDUCTION = 0.50
WILDFIRE_DAMAGE = 20
CONTAMINATION_SAVE_DC = 10
FLOOD_DAMAGE = 15
EARTHQUAKE_INJURY_CHANCE = 0.25
WINTER_DEPLETION_MULTIPLIER = 2

# Fitness Score Weights
FITNESS_WEIGHTS = {'Time': 1, 'Resource': 5, 'Kill': 50, 'Distance': 0.2, 'Event': 10}
```



## Section X: Formulas & Computations Summary

*This section compiles all core formulas and checks from across the document into a single, easy-to-reference location.*

### A. Animal Stat Calculations
- **Max Health:** `BASE_HEALTH + (animal.END * HEALTH_PER_ENDURANCE)`
- **Max Energy:** `BASE_ENERGY + (animal.END * ENERGY_PER_ENDURANCE)`

### B. Action & Combat Calculations
- **Movement Energy Cost:** `(MOVEMENT_BASE_COST * TERRAIN_MOVEMENT_MODIFIERS[terrain]) - (animal.AGI * MOVEMENT_AGILITY_MULTIPLIER)`
- **Combat Damage:** `(attacker.STR * STRENGTH_DAMAGE_MULTIPLIER) - defender.AGI`
- **Evasion Chance:** `defender.AGI * AGILITY_EVASION_MULTIPLIER` (Result is a percentage)
- **Time Complexity (Single Action):** O(1)

### C. Passive Ability Modifiers
- **Ambush Predator Damage:** `Combat Damage * AMBUSH_PREDATOR_MULTIPLIER`
- **Efficient Grazer Gain:** `PLANT_FOOD_GAIN * EFFICIENT_GRAZER_MULTIPLIER`

### D. Event & Check Calculations
- **Success Check (General Formula):** `roll(d10) + animal.Trait >= DC`
- **Rockslide Escape Check:** `roll(d10) + animal.AGI >= ROCKSLIDE_ESCAPE_DC (14)`
- **Rockslide Hide Check:** `roll(d10) + animal.END >= ROCKSLIDE_HIDE_DC (12)`
- **Curious Object Check:** `roll(d10) + animal.INT >= CURIOUS_OBJECT_DC (13)`
- **Contamination Save Check:** `roll(d10) + animal.END >= CONTAMINATION_SAVE_DC (10)`

### E. Fitness Score Calculation
```
Fitness Score: (Time Survived * W['Time']) + (Resources Gathered / 40 * W['Resource']) + (Kills * W['Kill']) + (Distance * W['Distance']) + (Events Survived * W['Event'])
```
## Section XI: Conceptual Data Structure

*This section outlines the high-level relationships between the core data objects of the simulation, serving as a blueprint for class structure.*

### Simulation
- `current_week` (Integer)
- `event_queue` (List of Event Objects)
- `world` (World Object)
- `population` (List of Animal Objects)
- `graveyard` (List of Animal Objects)

### World
- `grid` (2D Array of Tile Objects)
- `dimensions` (Tuple, e.g., (25, 25))

### Tile
- `coordinates` (Tuple, e.g., (x, y))
- `terrain_type` (String, e.g., 'Plains', 'Forest')
- `resource` (Resource Object or None)
- `occupant` (Animal Object or None)

### Animal
- `id` (Unique Identifier)
- `category` (String, e.g., 'Carnivore')
- `mlp_network` (MLP Object)
- `traits` (Dictionary of Integers, e.g., {'STR': 7, 'AGI': 5, ...})
- `status` (Dictionary of Floats/Integers, e.g., {'Health': 150, 'Hunger': 80, ...})
- `passive` (String, e.g., 'Ambush Predator')
- `active_effects` (List of Effect Objects)
- `location` (Tuple, e.g., (x, y))
- `fitness_score_components` (Dictionary, e.g., {'Time': 120, 'Kills': 1, ...})

### Effect
- `name` (String, e.g., 'Poisoned')
- `duration` (Integer)
- `modifiers` (Dictionary, e.g., {'AGI': -2})

### Resource
- `type` (String, e.g., 'Plant', 'Prey', 'Water')
- `quantity` (Integer, e.g., amount of Hunger/Thirst restored)
- `uses_left` (Integer)
## Section XII: Development Task List

*A structured plan to guide the coding and implementation of the project in logical phases, with cross-references to the relevant design sections.*

### Phase 1: Foundational Classes & Core Mechanics

#### Task 1.1: Setup Constants File
**Description:** Centralize all numeric and categorical constants in a single file.

**Action Items:**
- Create constants.py containing all static variables for balancing (e.g., grid size, trait ranges, event parameters).
- Use clear names and include docstrings/comments sourced from the design doc.

**Acceptance Criteria:** All magic numbers in test scripts/classes reference this file; covered constants match Section IX.

**Reference:** Section IX: Code Implementation Constants.

#### Task 1.2: Build Core Data Classes
**Description:** Implement data containers for animals, world, resources, tiles, and effects.

**Action Items:**
- Write constructors for Animal, World, Tile, Resource, Effect.
- Add attribute type hints, docstrings, and ensure initial attributes match the class map.

**Dependencies:** Task 1.1.

**Acceptance Criteria:** Classes instantiated in isolation pass attribute inspection.

**Reference:** Section XI: Conceptual Data Structure; See also Section V, VI for attributes.

#### Task 1.3: World & Map Generation
**Description:** Code logic to generate the initial 2D game world, terrains, and resource placement.

**Action Items:**
- Create world grid; assign terrain types using defined probability distributions.
- Position initial resources as per biomes.
- Validate no duplicate animal/resource spawn locations.

**Acceptance Criteria:** A grid prints with correct terrain/resource counts; unit tests cover edge cases (e.g., map borders, all-mountain tiles).

**Reference:** Section VI: Map and Objectives, Section VIII (World Generation Parameters).

#### Task 1.4: Animal Creation & Customization
**Description:** Finalize creation logic for diversified animals.

**Action Items:**
- Assign category, randomize trait distribution (primary/standard ranges), instantiate passives.
- Implement application of the 5 initial training points to traits.
- Compute max health/energy using design formulas.

**Dependencies:** Tasks 1.2, 1.3.

**Acceptance Criteria:** Script spawns a sample population with distinct, valid stats for each category.

**Reference:** Section V (Trait Distribution Logic), Section X.A (Formulas).

#### Task 1.5: Foundational Unit Tests
**Description:** Ensure reliability of new core code.

**Action Items:**
- Write basic tests for all constructors, attribute assignments, and boundary cases.

**Acceptance Criteria:** Minimum 80% code coverage for foundational classes.

**Reference:** Section XI: Data Structure.

### Phase 2: Simulation Engine & Event Handling

#### Task 2.1: Main Simulation Controller
**Description:** Create a Simulation class as the root orchestrator.

**Action Items:**
- Handles World, animal population, event queue, and overall control flow.

**Dependencies:** Phase 1 complete.

**Acceptance Criteria:** Simulation object can initialize a world and population without errors.

**Reference:** Section XI: Conceptual Data Structure.

#### Task 2.2: Game Loop Implementation
**Description:** Develop run_generation() for week-based generational simulation.

**Action Items:**
- Track week progression, manage event order, call action resolution, detect win/loss.

**Dependencies:** Task 2.1.

**Acceptance Criteria:** Simulation cycles through a generation; logs state transitions.

**Reference:** Section IV.A: Simulation Flow.

#### Task 2.3: Action Resolution System
**Description:** Implement phases for animal action turns (decision, status, execution, cleanup).

**Action Items:**
- Build phase handlers (decision, status/environment, execution, cleanup).
- Implement tie-break and fairness logic for simultaneity.
- **Subtasks:** Break into four handlers as in Section IV.B.

**Dependencies:** Tasks 2.2, 3.2 (for MLP integration).

**Acceptance Criteria:** Animals act in turn; phase logs confirm state changes; tested for deadlocks.

**Reference:** Section IV.B: Turn & Action Resolution.

#### Task 2.4: Event & Disaster Engine
**Description:** Write logic for triggered, random, and disaster events.

**Action Items:**
- Create function per event; build dice-roll and effect logic.
- Ensure events reference and affect animal/environment state properly.

**Dependencies:** Tasks 2.1–2.3.

**Acceptance Criteria:** Events fire with correct triggers and apply consequences; disaster/events unit tested.

**Reference:** Section VII: Event Lists, Section X.D: Event Formulas.

#### Task 2.5: Simulation Engine Testing
**Description:** Test and validate the complete simulation cycle and its components.

**Action Items:** Write and run integration tests for population survival, event triggers, and edge states.

**Acceptance Criteria:** End-to-end "dry run" passes; no critical errors during a test simulation.

**Reference:** Section X: Formulas.

### Phase 3: Artificial Intelligence & Evolution

#### Task 3.1: MLP ("Brain") Implementation
**Description:** Develop the neural decision system.

**Action Items:**
- Define input/output node count.
- Implement initialization and forward pass.
- **Subtasks:** Shape design, initialization function, forward function, helper functions.

**Reference:** Section II.A: MLP Architecture.

#### Task 3.2: Sensory Input System
**Description:** Translate animal and environment status to neural input.

**Action Items:**
- Gather and normalize animal's internal stats, scan localized grid.
- Flatten to 41-node vector.

**Dependencies:** Task 3.1.

**Acceptance Criteria:** Sensory function returns valid, bounded input for any grid position.

**Reference:** Section II.A (Input Layer), Section V: Status Variables.

#### Task 3.3: Fitness Function Implementation
**Description:** Quantify evolutionary fitness for each animal.

**Action Items:**
- Implement the formula; measure all components (time, kills, resources, distance, events).
- Ensure it triggers on annulment (death/sim-end).

**Dependencies:** Tasks 2.2, 2.3.

**Acceptance Criteria:** Fitness score reported correctly for example runs.

**Reference:** Section III.A: Fitness Function Rationale, Section X.E: Formula.

#### Task 3.4: Evolutionary Algorithm
**Description:** Develop next-gen creation logic with selection, crossover, mutation.

**Action Items:**
- Implement elitism and tournament selection.
- Write crossover (1-point, per design) and mutation routines.
- Unit-test offspring gene propagation.

**Dependencies:** Task 3.3.

**Acceptance Criteria:** Population evolves to next generation; gene transfer validated.

**Reference:** Section II.B: Evolutionary Algorithm Mechanics.

#### Task 3.5: AI/Evolution Testing and Data Logging
**Description:** Validate and debug animal decision logic, MLP evolution.

**Action Items:** Simulate multiple generations; output scores/traits for trend visualization.

**Reference:** Section III.B: Generational Goals.

### Phase 4: UI, Visualization & Reports

#### Task 4.1: Training CLI Interface
**Description:** Interactive text interface for animal selection and trait assignment.

**Action Items:** Build prompts, validate selections, apply trait bonuses.

**Reference:** Section VII: Preparations Stage.

#### Task 4.2: Simulation Visualization/Renderer (Grid GUI)
**Description:** Provide a real-time grid-based GUI renderer (desktop) for the world.

**Action Items:** Implement a grid view showing terrain/resources/animals with colors/icons; add controls for Next Week/Next Step, Auto-run, and Speed; integrate with `SimulationController`.

**Reference:** Section VI: Map and Objectives.

#### Task 4.3: Generational Reporting & Analysis
**Description:** Summarize and analyze run/performance after each simulation.

**Action Items:** Output fitness, max/avg scores, and top traits; save report/log if needed.

**Reference:** Section III.B: Generational Goals; Section X: Formulas.

#### Task 4.4: Documentation & Code Comments
**Description:** Maintain docstrings, comments, and update documentation for each new module.

**Action Items:** Complete Markdown sections or Jupyter notes after each milestone.

**Reference:** All sections.

### Phase Overlaps & Parallelization
Tasks in each phase build on each other but UI/prototyping tasks (4.1–4.3) can begin after Phase 2 stable baseline is available. The Grid GUI (4.2) can be prototyped in parallel once action resolution and events are stable.

Encourage periodic reviews and changelogs after each phase for easier debugging and progress tracking.

### Quick Navigation Reference
- **Section II:** Neural architecture and learning logic
- **Section III:** Fitness and evolutionary goals
- **Section IV:** Simulation/game engine cycle
- **Section V:** Animal/trait specifics
- **Section VI:** Map/biome and resource design
- **Section IX:** All constants for implementation
- **Section XI:** Full class/data blueprints
