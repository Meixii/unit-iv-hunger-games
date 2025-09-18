import { Separator } from "@/components/ui/separator";

export default function DevelopmentTasksPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Development Task List</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            A structured plan to guide the coding and implementation of the project in logical phases, with cross-references to the relevant design sections.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 1: Foundational Classes & Core Mechanics</h3>
            
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 1.1: Setup Constants File</h4>
                <p className="text-sm text-muted-foreground mb-2">Centralize all numeric and categorical constants in a single file.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Create constants.py containing all static variables for balancing</li>
                    <li>• Use clear names and include docstrings/comments sourced from the design doc</li>
                  </ul>
                  <p className="text-sm font-medium mt-2">Acceptance Criteria:</p>
                  <p className="text-sm text-muted-foreground">All magic numbers in test scripts/classes reference this file; covered constants match Section IX.</p>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 1.2: Build Core Data Classes</h4>
                <p className="text-sm text-muted-foreground mb-2">Implement data containers for animals, world, resources, tiles, and effects.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Write constructors for Animal, World, Tile, Resource, Effect</li>
                    <li>• Add attribute type hints, docstrings, and ensure initial attributes match the class map</li>
                  </ul>
                  <p className="text-sm font-medium mt-2">Dependencies:</p>
                  <p className="text-sm text-muted-foreground">Task 1.1</p>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 1.3: World & Map Generation</h4>
                <p className="text-sm text-muted-foreground mb-2">Code logic to generate the initial 2D game world, terrains, and resource placement.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Create world grid; assign terrain types using defined probability distributions</li>
                    <li>• Position initial resources as per biomes</li>
                    <li>• Validate no duplicate animal/resource spawn locations</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 1.4: Animal Creation & Customization</h4>
                <p className="text-sm text-muted-foreground mb-2">Finalize creation logic for diversified animals.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Assign category, randomize trait distribution (primary/standard ranges), instantiate passives</li>
                    <li>• Implement application of the 5 initial training points to traits</li>
                    <li>• Compute max health/energy using design formulas</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 1.5: Foundational Unit Tests</h4>
                <p className="text-sm text-muted-foreground mb-2">Ensure reliability of new core code.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Write basic tests for all constructors, attribute assignments, and boundary cases</li>
                  </ul>
                  <p className="text-sm font-medium mt-2">Acceptance Criteria:</p>
                  <p className="text-sm text-muted-foreground">Minimum 80% code coverage for foundational classes.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 2: Simulation Engine & Event Handling</h3>
            
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 2.1: Main Simulation Controller</h4>
                <p className="text-sm text-muted-foreground mb-2">Create a Simulation class as the root orchestrator.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Handles World, animal population, event queue, and overall control flow</li>
                  </ul>
                  <p className="text-sm font-medium mt-2">Dependencies:</p>
                  <p className="text-sm text-muted-foreground">Phase 1 complete</p>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 2.2: Game Loop Implementation</h4>
                <p className="text-sm text-muted-foreground mb-2">Develop run_generation() for week-based generational simulation.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Track week progression, manage event order, call action resolution, detect win/loss</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 2.3: Action Resolution System</h4>
                <p className="text-sm text-muted-foreground mb-2">Implement phases for animal action turns (decision, status, execution, cleanup).</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Build phase handlers (decision, status/environment, execution, cleanup)</li>
                    <li>• Implement tie-break and fairness logic for simultaneity</li>
                    <li>• Break into four handlers as in Section IV.B</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 2.4: Event & Disaster Engine</h4>
                <p className="text-sm text-muted-foreground mb-2">Write logic for triggered, random, and disaster events.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Create function per event; build dice-roll and effect logic</li>
                    <li>• Ensure events reference and affect animal/environment state properly</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 2.5: Simulation Engine Testing</h4>
                <p className="text-sm text-muted-foreground mb-2">Test and validate the complete simulation cycle and its components.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Write and run integration tests for population survival, event triggers, and edge states</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 3: Artificial Intelligence & Evolution</h3>
            
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 3.1: MLP ("Brain") Implementation</h4>
                <p className="text-sm text-muted-foreground mb-2">Develop the neural decision system.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Define input/output node count</li>
                    <li>• Implement initialization and forward pass</li>
                    <li>• Shape design, initialization function, forward function, helper functions</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 3.2: Sensory Input System</h4>
                <p className="text-sm text-muted-foreground mb-2">Translate animal and environment status to neural input.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Gather and normalize animal's internal stats, scan localized grid</li>
                    <li>• Flatten to 41-node vector</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 3.3: Fitness Function Implementation</h4>
                <p className="text-sm text-muted-foreground mb-2">Quantify evolutionary fitness for each animal.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Implement the formula; measure all components (time, kills, resources, distance, events)</li>
                    <li>• Ensure it triggers on annulment (death/sim-end)</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 3.4: Evolutionary Algorithm</h4>
                <p className="text-sm text-muted-foreground mb-2">Develop next-gen creation logic with selection, crossover, mutation.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Implement elitism and tournament selection</li>
                    <li>• Write crossover (1-point, per design) and mutation routines</li>
                    <li>• Unit-test offspring gene propagation</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 3.5: AI/Evolution Testing and Data Logging</h4>
                <p className="text-sm text-muted-foreground mb-2">Validate and debug animal decision logic, MLP evolution.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Simulate multiple generations; output scores/traits for trend visualization</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 4: UI, Visualization & Reports</h3>
            
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 4.1: Training CLI Interface</h4>
                <p className="text-sm text-muted-foreground mb-2">Interactive text interface for animal selection and trait assignment.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Build prompts, validate selections, apply trait bonuses</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 4.2: Simulation Visualization/Renderer</h4>
                <p className="text-sm text-muted-foreground mb-2">Provide real-time game-world visualization.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Print grid with symbols for each terrain/resource/animal; display population/round count</li>
                    <li>• Consider color/ASCII enhancement</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 4.3: Generational Reporting & Analysis</h4>
                <p className="text-sm text-muted-foreground mb-2">Summarize and analyze run/performance after each simulation.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Output fitness, max/avg scores, and top traits; save report/log if needed</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Task 4.4: Documentation & Code Comments</h4>
                <p className="text-sm text-muted-foreground mb-2">Maintain docstrings, comments, and update documentation for each new module.</p>
                <div className="space-y-2">
                  <p className="text-sm font-medium">Action Items:</p>
                  <ul className="text-sm text-muted-foreground ml-4 space-y-1">
                    <li>• Complete Markdown sections or Jupyter notes after each milestone</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase Overlaps & Parallelization</h3>
            <div className="border rounded-lg p-4">
              <p className="text-sm text-muted-foreground">
                Tasks in each phase build on each other but UI/prototyping tasks (4.1–4.3) can begin after Phase 2 stable baseline is available.
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Encourage periodic reviews and changelogs after each phase for easier debugging and progress tracking.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
