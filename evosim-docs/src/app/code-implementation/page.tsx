import { Separator } from "@/components/ui/separator";

export default function CodeImplementationPage() {
  const codeConstants = `# World Generation
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
FITNESS_WEIGHTS = {'Time': 1, 'Resource': 5, 'Kill': 50, 'Distance': 0.2, 'Event': 10}`;

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Code Implementation Constants</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section provides a direct translation of the parameters in Section VIII into a format suitable for a configuration or constants file in Python. This centralizes all "magic numbers" for easy tweaking during development.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Python Constants File</h3>
            <p>
              All numerical values and parameters are centralized in a single constants file for easy maintenance and balancing.
            </p>
            
            <div className="bg-muted rounded-lg p-4">
              <pre className="text-sm overflow-x-auto">
                <code>{codeConstants}</code>
              </pre>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Usage Guidelines</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">World Generation</h4>
                <p className="text-sm text-muted-foreground">
                  Constants for grid size, terrain distribution, and resource spawning probabilities.
                </p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Animal Parameters</h4>
                <p className="text-sm text-muted-foreground">
                  Trait ranges, health/energy calculations, and initial training bonuses.
                </p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Status Dynamics</h4>
                <p className="text-sm text-muted-foreground">
                  Depletion rates, regeneration values, and damage calculations.
                </p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Combat & Effects</h4>
                <p className="text-sm text-muted-foreground">
                  Damage multipliers, evasion calculations, and effect durations.
                </p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Events & Disasters</h4>
                <p className="text-sm text-muted-foreground">
                  Event parameters, difficulty checks, and environmental effects.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Implementation Notes</h3>
            <ul className="space-y-2 ml-4">
              <li>• All magic numbers should reference this constants file</li>
              <li>• Use clear, descriptive names for all variables</li>
              <li>• Include docstrings and comments for complex calculations</li>
              <li>• Group related constants together for better organization</li>
              <li>• Consider using enums for categorical values</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
