# Event Engine System

The Event Engine System provides dynamic and engaging gameplay through environmental challenges and opportunities. It implements a comprehensive event system that includes triggered events, random events, and disaster events, all coordinated through a sophisticated scheduling system.

## Overview

The Event Engine System consists of three main event types:

1. **Triggered Events**: Occur when specific conditions are met
2. **Random Events**: Occur randomly with probability-based mechanics
3. **Disaster Events**: Large-scale events with area-of-effect mechanics

All events are managed through a unified `EventEngine` that provides scheduling, execution, and coordination.

## Architecture

### Core Components

- **`EventEngine`**: Main coordinator that integrates all event systems
- **`EventScheduler`**: Manages event scheduling and execution order
- **`TriggeredEventEngine`**: Handles condition-based events
- **`RandomEventEngine`**: Handles probability-based events
- **`DisasterEventEngine`**: Handles large-scale disaster events
- **`event_data.py`**: Base data structures and event types

### Data Structures

#### `Event`
Base class for all events:
```python
@dataclass
class Event:
    event_id: str
    name: str
    description: str
    event_type: EventType
    probability: float = 1.0
    cooldown_weeks: int = 0
    max_occurrences: Optional[int] = None
    last_occurrence_week: int = -1
    occurrence_count: int = 0
    is_active: bool = True
```

#### `EventResult`
Represents the outcome of event execution:
```python
@dataclass
class EventResult:
    event_id: str
    event_type: EventType
    success: bool
    message: str
    affected_animals: List[str] = field(default_factory=list)
    casualties: int = 0
    effects_applied: int = 0
    resources_changed: int = 0
    terrain_modified: bool = False
    duration: Optional[float] = None
    timestamp: Optional[datetime] = None
```

#### `EventCondition`
Defines conditions for triggered events:
```python
@dataclass
class EventCondition:
    name: str
    description: str
    check_function: Callable[[Simulation], bool]
    parameters: Dict[str, Any] = field(default_factory=dict)
```

## Event Types

### Triggered Events

Events that occur when specific conditions are met in the simulation.

#### Population Events
- **Overpopulation Crisis**: Triggers when too many animals are in a small area
- **Population Decline**: Triggers when population drops below threshold
- **Population Boom**: Triggers when population grows rapidly

#### Resource Events
- **Resource Depletion**: Triggers when resources become scarce
- **Resource Abundance**: Triggers when resources are plentiful
- **Resource Competition**: Triggers when animals compete for limited resources

#### Health Events
- **Disease Outbreak**: Triggers when many animals have low health
- **Health Crisis**: Triggers when overall population health is poor
- **Recovery Period**: Triggers after major health events

### Random Events

Events that occur randomly with specific probabilities.

#### Beneficial Events
- **Resource Discovery**: Adds new resources to the world
- **Healing Springs**: Restores health to random animals
- **Abundant Harvest**: Increases resource abundance

#### Neutral Events
- **Migration**: Moves animals to new locations
- **Weather Change**: Affects animal energy and behavior

#### Minor Negative Events
- **Pest Infestation**: Reduces plant resources
- **Territorial Dispute**: Increases animal stress and aggression

### Disaster Events

Large-scale events with area-of-effect mechanics.

#### Natural Disasters
- **Earthquake**: Damages terrain and affects animals in radius
- **Flood**: Transforms terrain and displaces animals
- **Drought**: Reduces water resources across large areas
- **Wildfire**: Destroys resources and damages animals

#### Environmental Disasters
- **Pollution**: Contaminates resources and affects animal health
- **Climate Change**: Alters terrain types and resource availability
- **Habitat Destruction**: Removes resources and forces migration

#### Biological Disasters
- **Plague**: Spreads disease among animals
- **Predator Invasion**: Introduces new threats
- **Parasite Outbreak**: Weakens animals over time

## Event Scheduling

### Weekly Schedule Generation

The `EventScheduler` generates weekly schedules based on:

1. **Week Number**: Early weeks have fewer events
2. **Population Size**: Adjusts event probabilities based on population
3. **Event Cooldowns**: Prevents events from occurring too frequently
4. **Maximum Events**: Limits events per week to prevent overwhelming

### Schedule Progression
- **Week 1**: Minimal events (1 triggered, 1 random, 0 disasters)
- **Weeks 2-3**: Limited events (2 triggered, 1 random, 0-1 disasters)
- **Week 4+**: Normal scheduling (3 triggered, 2 random, 1 disaster)

### Probability Adjustments
- **Low Population (≤3)**: Disaster probability reduced to 30%
- **High Population (>15)**: Disaster probability increased to 150%
- **Late Weeks (>10)**: Disaster probability increased by 20%

## Usage

### Basic Usage
```python
from event_engine import EventEngine

# Initialize with simulation and logger
event_engine = EventEngine(simulation, logger)

# Execute weekly events
result = event_engine.execute_weekly_events(week=5)

# Check results
print(f"Events executed: {result['events_executed']}")
print(f"Casualties: {result['casualties']}")
print(f"Resources affected: {result['resources_affected']}")
```

### Configuration
```python
# Configure event system
event_engine.configure(
    enabled=True,
    triggered_events_enabled=True,
    random_events_enabled=True,
    disaster_events_enabled=True,
    max_events_per_week=5,
    disaster_probability_modifier=1.0
)
```

### Custom Events
```python
# Add custom triggered event
custom_event = TriggeredEvent(
    event_id="custom_event",
    name="Custom Event",
    description="A custom event",
    conditions=[custom_condition]
)
event_engine.add_custom_event(custom_event)
```

## Event Execution Flow

1. **Schedule Generation**: Create weekly event schedule
2. **Triggered Events**: Check conditions and execute triggered events
3. **Random Events**: Roll probabilities and execute random events
4. **Disaster Events**: Apply probability modifiers and execute disasters
5. **Result Aggregation**: Collect and summarize all event results
6. **History Storage**: Store results for statistics and analysis

## Event Mechanics

### Triggered Event Mechanics
- Conditions are checked each week
- Events can require all conditions or any condition
- Cooldown periods prevent spam
- Maximum occurrence limits prevent over-execution

### Random Event Mechanics
- Base probabilities are modified by simulation state
- Population size affects event likelihood
- Week number influences event frequency
- Events are shuffled for random execution order

### Disaster Event Mechanics
- Area-of-effect calculations using distance formulas
- Severity levels affect damage multipliers
- Epicenters are randomly chosen if not specified
- Terrain and resource modifications

## Result Tracking

### Event Results
Each event execution produces an `EventResult` containing:
- Success/failure status
- Descriptive message
- Affected animals list
- Casualty count
- Effects applied count
- Resources changed count
- Terrain modification flag

### Statistics
The system tracks comprehensive statistics:
- Total events executed
- Success rates by event type
- Total casualties caused
- Total resources affected
- Event frequency analysis

## Integration

The Event Engine integrates with:
- **Simulation Controller**: Called once per week
- **Action Resolution System**: Events can affect animal actions
- **World Generator**: Events can modify terrain and resources
- **Fitness System**: Events can impact animal performance
- **Logging System**: Comprehensive event logging

## Error Handling

The system includes robust error handling:
- Event execution failures are caught and logged
- Invalid conditions default to false
- Malformed events are skipped gracefully
- Scheduler errors are reported in results

## Performance Considerations

- Events are filtered by cooldown and occurrence limits
- Probability calculations are cached when possible
- Area-of-effect calculations are optimized
- Event history is limited to prevent memory issues

## Configuration Options

### Global Configuration
- `enabled`: Enable/disable entire event system
- `max_events_per_week`: Maximum events per week
- `disaster_probability_modifier`: Global disaster probability multiplier
- `event_intensity_modifier`: Global event intensity multiplier

### Per-Type Configuration
- `triggered_events_enabled`: Enable/disable triggered events
- `random_events_enabled`: Enable/disable random events
- `disaster_events_enabled`: Enable/disable disaster events

### Event-Specific Configuration
- `probability`: Base occurrence probability
- `cooldown_weeks`: Minimum weeks between occurrences
- `max_occurrences`: Maximum times event can occur
- `severity`: Disaster severity level
- `area_of_effect`: Disaster radius

## Testing

The system includes comprehensive test coverage for:
- All event types and their execution
- Condition checking and validation
- Probability calculations and modifiers
- Area-of-effect mechanics
- Error handling and edge cases
- Integration with other systems

## Future Enhancements

Potential improvements include:
- More sophisticated condition systems
- Chain events (events that trigger other events)
- Seasonal event patterns
- Player-triggered events
- Event balancing based on simulation state
- Machine learning for dynamic event generation
- Event visualization and reporting tools

## Event Examples

### Example Triggered Event
```python
# Overpopulation event
overpopulation_condition = EventCondition(
    name="overpopulation",
    description="Too many animals in a small area",
    check_function=check_overpopulation,
    parameters={"threshold": 15, "area_size": 25}
)

overpopulation_event = OverpopulationEvent(
    event_id="overpopulation",
    name="Overpopulation Crisis",
    description="Too many animals competing for limited resources",
    conditions=[overpopulation_condition],
    cooldown_weeks=2
)
```

### Example Random Event
```python
# Resource discovery event
resource_discovery = ResourceDiscoveryEvent(
    event_id="resource_discovery",
    name="Resource Discovery",
    description="New resources are discovered in the world",
    base_probability=0.15,
    cooldown_weeks=3
)
```

### Example Disaster Event
```python
# Earthquake disaster
earthquake = EarthquakeEvent(
    event_id="earthquake",
    name="Earthquake",
    description="A powerful earthquake shakes the ground",
    severity="major",
    area_of_effect=4,
    base_probability=0.05,
    cooldown_weeks=8
)
```
