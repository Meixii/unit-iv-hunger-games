import { Separator } from "@/components/ui/separator";

export default function DataStructurePage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Conceptual Data Structure</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section outlines the high-level relationships between the core data objects of the simulation, serving as a blueprint for class structure.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Simulation</h3>
            <p>The main controller class that orchestrates the entire simulation.</p>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span className="font-mono">current_week</span>
                  <span className="text-muted-foreground">Integer</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">event_queue</span>
                  <span className="text-muted-foreground">List of Event Objects</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">world</span>
                  <span className="text-muted-foreground">World Object</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">population</span>
                  <span className="text-muted-foreground">List of Animal Objects</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">graveyard</span>
                  <span className="text-muted-foreground">List of Animal Objects</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">World</h3>
            <p>Represents the game world and its grid-based structure.</p>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span className="font-mono">grid</span>
                  <span className="text-muted-foreground">2D Array of Tile Objects</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">dimensions</span>
                  <span className="text-muted-foreground">Tuple, e.g., (25, 25)</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Tile</h3>
            <p>Individual grid cell representing a location in the world.</p>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span className="font-mono">coordinates</span>
                  <span className="text-muted-foreground">Tuple, e.g., (x, y)</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">terrain_type</span>
                  <span className="text-muted-foreground">String, e.g., 'Plains', 'Forest'</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">resource</span>
                  <span className="text-muted-foreground">Resource Object or None</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">occupant</span>
                  <span className="text-muted-foreground">Animal Object or None</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Animal</h3>
            <p>The core entity representing a living creature in the simulation.</p>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span className="font-mono">id</span>
                  <span className="text-muted-foreground">Unique Identifier</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">category</span>
                  <span className="text-muted-foreground">String, e.g., 'Carnivore'</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">mlp_network</span>
                  <span className="text-muted-foreground">MLP Object</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">traits</span>
                  <span className="text-muted-foreground">Dictionary of Integers, e.g., {'{STR: 7, AGI: 5, ...}'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">status</span>
                  <span className="text-muted-foreground">Dictionary of Floats/Integers, e.g., {'{Health: 150, Hunger: 80, ...}'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">passive</span>
                  <span className="text-muted-foreground">String, e.g., 'Ambush Predator'</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">active_effects</span>
                  <span className="text-muted-foreground">List of Effect Objects</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">location</span>
                  <span className="text-muted-foreground">Tuple, e.g., (x, y)</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">fitness_score_components</span>
                  <span className="text-muted-foreground">Dictionary, e.g., {'{Time: 120, Kills: 1, ...}'}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Effect</h3>
            <p>Temporary modifiers that affect animal traits or status.</p>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span className="font-mono">name</span>
                  <span className="text-muted-foreground">String, e.g., 'Poisoned'</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">duration</span>
                  <span className="text-muted-foreground">Integer</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">modifiers</span>
                  <span className="text-muted-foreground">Dictionary, e.g., {'{AGI: -2}'}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Resource</h3>
            <p>Consumable items that animals can interact with.</p>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span className="font-mono">type</span>
                  <span className="text-muted-foreground">String, e.g., 'Plant', 'Prey', 'Water'</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">quantity</span>
                  <span className="text-muted-foreground">Integer, e.g., amount of Hunger/Thirst restored</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-mono">uses_left</span>
                  <span className="text-muted-foreground">Integer</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Class Relationships</h3>
            <div className="border rounded-lg p-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="font-semibold">Simulation</span>
                  <span className="text-muted-foreground">contains</span>
                  <span className="font-mono">World, List&lt;Animal&gt;</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">World</span>
                  <span className="text-muted-foreground">contains</span>
                  <span className="font-mono">2D Array&lt;Tile&gt;</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">Tile</span>
                  <span className="text-muted-foreground">may contain</span>
                  <span className="font-mono">Animal, Resource</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">Animal</span>
                  <span className="text-muted-foreground">has</span>
                  <span className="font-mono">MLP, List&lt;Effect&gt;</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
