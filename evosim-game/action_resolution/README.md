# Action Resolution System

The Action Resolution System implements the core turn-based mechanics for EvoSim, providing a fair and deterministic way to process all animal actions during each simulation turn. This system ensures that animals acting earlier in the turn don't have an unfair advantage over those acting later.

## Overview

The Action Resolution System follows a 4-phase approach as specified in Section IV.B of the EvoSim design:

1. **Decision Phase**: Collect actions from all animals
2. **Status & Environmental Phase**: Apply passive effects
3. **Action Execution Phase**: Execute actions by priority
4. **Cleanup Phase**: Apply new effects and remove expired ones

## Architecture

### Core Components

- **`ActionResolver`**: Main orchestrator that coordinates all phases
- **`DecisionEngine`**: Handles Phase 1 - collecting animal decisions
- **`StatusEngine`**: Handles Phase 2 - applying passive effects
- **`ExecutionEngine`**: Handles Phase 3 - executing actions with conflict resolution
- **`CleanupEngine`**: Handles Phase 4 - managing effects and cleanup
- **`action_data.py`**: Data structures for actions and priorities

### Data Structures

#### `AnimalAction`
Represents a planned action by an animal during the decision phase:
```python
@dataclass
class AnimalAction:
    animal_id: str
    animal: Animal
    action_type: ActionType
    target_location: Optional[Tuple[int, int]] = None
    target_animal: Optional[Animal] = None
    energy_cost: float = 0.0
    success: bool = False
    result_message: str = ""
```

#### `ActionPriority`
Defines execution priority levels:
- `STATIONARY = 1`: Rest, Eat, Drink, Attack
- `MOVEMENT = 2`: All movement actions

## Phase Details

### Phase 1: Decision Phase
**Purpose**: Collect actions from all living animals

**Process**:
- Each animal's decision system (MLP or rule-based) outputs a chosen action
- Actions are stored without execution
- Supports both MLP-based and fallback rule-based decisions
- Handles decision failures gracefully with default rest action

**Key Features**:
- MLP preference with rule-based fallback
- Resource-aware decision making
- Diet-based food selection (herbivore/carnivore/omnivore)
- Energy cost calculation

### Phase 2: Status & Environmental Phase
**Purpose**: Apply passive changes to all animals simultaneously

**Process**:
- Hunger and thirst depletion (3 and 2 points per turn respectively)
- Health loss from debuffs (poisoned, injured effects)
- Passive energy regeneration (2 points if healthy, 1 if unhealthy)
- Death condition checking and animal removal

**Key Features**:
- Simultaneous application prevents order-dependent effects
- Death from health, starvation, or dehydration
- Fitness tracking (time survived)

### Phase 3: Action Execution Phase
**Purpose**: Execute actions in priority order with conflict resolution

**Execution Order**:
1. **Stationary Actions** (Priority 1): Rest, Eat, Drink, Attack
2. **Movement Actions** (Priority 2): All movement with conflict resolution

**Conflict Resolution**:
- Movement conflicts resolved by agility (highest wins)
- Resource conflicts handled per action type
- Animal encounters during movement

**Key Features**:
- Energy requirement validation
- Terrain-based movement restrictions (mountains impassable)
- Combat mechanics with strength vs agility
- Resource consumption and depletion
- Fitness tracking (distance, resources, kills)

### Phase 4: Cleanup Phase
**Purpose**: Apply new effects and remove expired ones

**Process**:
- Decrease effect durations
- Remove expired effects
- Add new effects based on conditions:
  - Well-Fed: When hunger ≥ 90
  - Exhausted: When energy ≤ 20

## Usage

### Basic Usage
```python
from action_resolution import ActionResolver

# Initialize with simulation and logger
resolver = ActionResolver(simulation, logger)

# Execute complete action resolution for a week
result = resolver.execute_action_resolution_system(week=5)

# Check results
print(f"Actions processed: {result['actions_processed']}")
print(f"Casualties: {result['casualties']}")
print(f"Conflicts resolved: {result['conflicts_resolved']}")
```

### Result Structure
```python
{
    'phase': 'action_resolution',
    'week': 5,
    'success': True,
    'message': 'Action resolution completed successfully. 2 casualties.',
    'phases_completed': 4,
    'actions_processed': 12,
    'casualties': 2,
    'affected_animals': ['animal_001', 'animal_003'],
    'conflicts_resolved': 1,
    'duration': timedelta(seconds=0.045),
    'phase_results': {
        'decision': {'actions_collected': 12},
        'status_environmental': {...},
        'action_execution': {...},
        'cleanup': {...}
    }
}
```

## Action Types

### Movement Actions
- `MOVE_NORTH`, `MOVE_EAST`, `MOVE_SOUTH`, `MOVE_WEST`
- Energy cost: 5.0
- Subject to terrain restrictions and conflict resolution

### Stationary Actions
- `REST`: Restore energy (20) and health (5), no energy cost
- `EAT`: Consume food resources, restore hunger, energy cost: 2.0
- `DRINK`: Consume water resources, restore thirst, energy cost: 2.0
- `ATTACK`: Combat with other animals, energy cost: 10.0

## Decision Making

### MLP-Based Decisions
When an animal has an MLP network:
1. Build input vector from sensory data
2. Forward pass through MLP
3. Select action with highest probability
4. Calculate target location for movement actions

### Rule-Based Fallback
When no MLP is available:
1. Check critical survival needs (health ≤ 20 → rest)
2. Check hunger (≤ 30 → find and eat food)
3. Check thirst (≤ 30 → find and drink water)
4. Check energy (≤ 40 → rest)
5. Default to random movement

## Conflict Resolution

### Movement Conflicts
When multiple animals try to move to the same location:
1. Calculate agility for each animal
2. Highest agility wins
3. Winner executes movement
4. Losers fail with "Lost movement conflict" message

### Animal Encounters
When an animal moves into an occupied tile:
- Currently blocks movement to prevent complexity
- Can be extended for full combat mechanics

## Error Handling

The system includes comprehensive error handling:
- Decision failures default to rest action
- Action execution failures are logged and tracked
- Invalid locations and insufficient energy are handled gracefully
- Dead animals are filtered out before action execution

## Performance Considerations

- Actions are collected once per turn to avoid redundant decision making
- Conflict resolution is O(n) for each target location
- Effect processing is batched for efficiency
- Statistics are tracked for monitoring and debugging

## Integration

The Action Resolution System integrates with:
- **Simulation Controller**: Called once per week
- **Sensory System**: For MLP input vector generation
- **Fitness System**: For tracking animal performance metrics
- **World Generator**: For terrain and resource validation
- **Evolution System**: For MLP network access

## Configuration

The system can be configured through the simulation parameters:
- Energy costs for different actions
- Hunger/thirst depletion rates
- Health regeneration rates
- Conflict resolution mechanics
- Effect durations and conditions

## Testing

The system includes comprehensive test coverage for:
- All action types and their execution
- Conflict resolution scenarios
- Error handling and edge cases
- Integration with other systems
- Performance under various loads

## Future Enhancements

Potential improvements include:
- More sophisticated combat mechanics
- Advanced conflict resolution strategies
- Dynamic action costs based on terrain
- Multi-turn action planning
- Cooperative actions between animals
