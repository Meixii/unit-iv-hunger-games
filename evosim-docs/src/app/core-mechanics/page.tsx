import { Separator } from "@/components/ui/separator";

export default function CoreMechanicsPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h1 id="core-mechanics" className="text-4xl font-bold tracking-tight">Core Mechanics</h1>
        <p className="text-lg text-muted-foreground">
          This section details the fundamental systems of the simulation, such as the simulation loop, action resolution, and resource/combat mechanics.
        </p>
      </div>
      
      <div className="space-y-8">

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 id="simulation-flow" className="text-2xl font-semibold">Simulation Flow</h3>
            <p>This defines the high-level sequence of the entire simulation from start to finish.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">1. Preparation Stage</h4>
              <p>The one-time setup at the very beginning of a simulation run.</p>
              <ul className="space-y-2 ml-4">
                <li><strong>Character Selection & Initial Training:</strong> Players choose an animal category and answer 5 questions to receive a +1 bonus to specific traits. This is the only point of direct player intervention.</li>
                <li><strong>World & Population Generation:</strong> The grid map, terrain, resources, and the initial population of animals (Generation 0) are created based on the parameters in Sections VII and IX.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">2. Generational Loop</h4>
              <p>The simulation proceeds in generations. Each generation consists of a full &quot;Hunger Games&quot; style survival scenario. The loop is as follows:</p>
              <ol className="space-y-2 ml-4 list-decimal">
                <li>Run the Weekly Cycle until a single animal survives or a maximum number of weeks is reached.</li>
                <li>Calculate the final Fitness Score for every animal that participated.</li>
                <li>Perform the Evolutionary Algorithm steps (Selection, Crossover, Mutation) to create the population for the next generation.</li>
                <li>Reset the world and spawn the new population.</li>
                <li>Repeat.</li>
              </ol>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">3. Weekly Cycle</h4>
              <p>Within a generation, time progresses in weeks. Each week consists of a series of events.</p>
              <ul className="space-y-2 ml-4">
                <li><strong>Week 1 (Fixed Order):</strong> Movement, Triggered Event, Random Event, Disaster, Triggered Event, Movement, Triggered Event.</li>
                <li><strong>Subsequent Weeks:</strong> The order and frequency of events are randomized to ensure unpredictability.</li>
              </ul>
            </div>
          </div>

          <Separator />

          <div className="space-y-4">
            <h3 id="turn-action-resolution" className="text-2xl font-semibold">Turn & Action Resolution</h3>
            <p>To ensure fairness, each Movement Event is resolved in distinct phases, preventing animals that act earlier from having an unfair advantage.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">1. Decision Phase</h4>
              <p>Every living animal&apos;s MLP is fed its current sensory inputs. Each MLP processes this information and outputs a chosen action (e.g., &quot;Move North,&quot; &quot;Eat&quot;). All decisions are stored without being executed yet.</p>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">2. Status & Environmental Phase</h4>
              <p>Before actions are taken, passive changes are applied to all animals simultaneously.</p>
              <ul className="space-y-1 ml-4">
                <li>• Hunger and Thirst depletion.</li>
                <li>• Health loss from debuffs like &apos;Poisoned&apos;.</li>
                <li>• Passive Energy regeneration.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">3. Action Execution Phase</h4>
              <p>The stored actions are executed in a specific order of priority:</p>
              <ul className="space-y-2 ml-4">
                <li><strong>Priority 1 (Stationary Actions):</strong> &apos;Rest&apos;, &apos;Eat&apos;, &apos;Drink&apos;, &apos;Attack&apos;. These are resolved first.</li>
                <li><strong>Priority 2 (Movement Actions):</strong> All &apos;Move&apos; actions are resolved. If two animals attempt to move into the same empty tile, the one with the higher Agility succeeds, while the other&apos;s move fails (consuming no energy). If an animal moves onto a tile occupied by another, an &apos;Animal Encounter&apos; is triggered.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">4. Cleanup Phase</h4>
              <p>Any new effects are applied (e.g., &apos;Well-Fed&apos; after eating), and expired effects are removed.</p>
            </div>
          </div>

          <Separator />

          <div className="space-y-4">
            <h3 id="resource-dynamics" className="text-2xl font-semibold">Resource Dynamics</h3>
            <ul className="space-y-2 ml-4">
              <li><strong>Spawning:</strong> Resources are placed on the map during World Generation. When a resource is fully consumed, it has a small chance to respawn in a valid location after a set number of weeks, preventing the map from becoming permanently barren.</li>
              <li><strong>Consumption:</strong> Resources have a set number of &quot;uses.&quot; For example, a Plant resource might have 2 uses, restoring 40 Hunger each time before it disappears.</li>
            </ul>
          </div>

          <Separator />

          <div className="space-y-4">
            <h3 id="combat-mechanics" className="text-2xl font-semibold">Combat Mechanics</h3>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Initiation</h4>
              <p>Combat is initiated when an &apos;Animal Encounter&apos; is triggered. The MLPs of both animals then make a choice based on their sensory input: &apos;Attack&apos; or one of the &apos;Move&apos; actions (to flee).</p>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Resolution</h4>
              <ul className="space-y-2 ml-4">
                <li>If both animals choose &apos;Attack&apos;, they engage in combat. Damage is exchanged simultaneously based on the formula in Section V. Combat continues in subsequent turns until one is defeated or chooses to flee.</li>
                <li>If one animal chooses &apos;Attack&apos; and the other chooses &apos;Flee&apos;, the attacker gets one free attack (the defender&apos;s AGI is not subtracted for this first strike). The fleeing animal then attempts to move to an adjacent tile.</li>
                <li>If both choose &apos;Flee&apos;, they both move away in their chosen directions.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
