import { Separator } from "@/components/ui/separator";

export default function PhasesPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Implementation Phases</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            A high-level overview of the four main implementation phases for the EvoSim project.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 1: Foundational Classes & Core Mechanics</h3>
            <div className="border rounded-lg p-6 bg-blue-50 dark:bg-blue-950">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">1</div>
                  <h4 className="text-xl font-semibold">Foundation Phase</h4>
                </div>
                <p className="text-sm text-muted-foreground">
                  Establish the core data structures and basic game mechanics. This phase focuses on creating the fundamental building blocks of the simulation.
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="font-semibold mb-2">Key Deliverables:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• Constants file with all parameters</li>
                      <li>• Core data classes (Animal, World, Tile, etc.)</li>
                      <li>• World generation system</li>
                      <li>• Animal creation and customization</li>
                      <li>• Unit tests for foundational code</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold mb-2">Success Criteria:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• All classes instantiate correctly</li>
                      <li>• World generates with proper terrain distribution</li>
                      <li>• Animals spawn with valid stats</li>
                      <li>• 80%+ code coverage on tests</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 2: Simulation Engine & Event Handling</h3>
            <div className="border rounded-lg p-6 bg-green-50 dark:bg-green-950">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">2</div>
                  <h4 className="text-xl font-semibold">Simulation Phase</h4>
                </div>
                <p className="text-sm text-muted-foreground">
                  Build the core simulation loop and event system. This phase creates the "heart" of the simulation where all the action happens.
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="font-semibold mb-2">Key Deliverables:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• Main simulation controller</li>
                      <li>• Game loop with week-based progression</li>
                      <li>• Action resolution system</li>
                      <li>• Event and disaster engine</li>
                      <li>• Integration testing suite</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold mb-2">Success Criteria:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• Complete simulation cycles run without errors</li>
                      <li>• Events trigger correctly</li>
                      <li>• Action resolution is fair and consistent</li>
                      <li>• End-to-end tests pass</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 3: Artificial Intelligence & Evolution</h3>
            <div className="border rounded-lg p-6 bg-purple-50 dark:bg-purple-950">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">3</div>
                  <h4 className="text-xl font-semibold">AI & Evolution Phase</h4>
                </div>
                <p className="text-sm text-muted-foreground">
                  Implement the neural networks and evolutionary algorithms. This phase brings the "intelligence" to the simulation.
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="font-semibold mb-2">Key Deliverables:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• MLP neural network implementation</li>
                      <li>• Sensory input system</li>
                      <li>• Fitness function calculation</li>
                      <li>• Evolutionary algorithm (selection, crossover, mutation)</li>
                      <li>• AI testing and data logging</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold mb-2">Success Criteria:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• Animals make intelligent decisions</li>
                      <li>• Evolution produces better survival strategies</li>
                      <li>• Fitness scores increase over generations</li>
                      <li>• Data shows clear evolutionary trends</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase 4: UI, Visualization & Reports</h3>
            <div className="border rounded-lg p-6 bg-orange-50 dark:bg-orange-950">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-orange-600 text-white rounded-full flex items-center justify-center font-bold">4</div>
                  <h4 className="text-xl font-semibold">User Interface Phase</h4>
                </div>
                <p className="text-sm text-muted-foreground">
                  Create user interfaces and visualization tools. This phase includes a desktop Grid GUI for real-time simulation visualization in addition to the CLI.
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="font-semibold mb-2">Key Deliverables:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• Training CLI interface</li>
                      <li>• Real-time simulation visualization</li>
                      <li>• Generational reporting and analysis</li>
                      <li>• Documentation and code comments</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold mb-2">Success Criteria:</h5>
                    <ul className="text-sm space-y-1">
                      <li>• Users can easily interact with the system</li>
                      <li>• Visualizations are clear and informative</li>
                      <li>• Reports provide meaningful insights</li>
                      <li>• Code is well-documented</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Phase Dependencies & Timeline</h3>
            <div className="border rounded-lg p-6">
              <div className="space-y-4">
                <h4 className="font-semibold">Sequential Dependencies</h4>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm">Phase 1</span>
                    <span className="text-muted-foreground">→</span>
                    <span className="font-mono text-sm">Phase 2</span>
                    <span className="text-muted-foreground">→</span>
                    <span className="font-mono text-sm">Phase 3</span>
                  </div>
                  <p className="text-sm text-muted-foreground">Core phases must be completed sequentially as each builds on the previous.</p>
                </div>
                
                <h4 className="font-semibold">Parallel Opportunities</h4>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm">Phase 2</span>
                    <span className="text-muted-foreground">+</span>
                    <span className="font-mono text-sm">Phase 4 (UI tasks)</span>
                  </div>
                  <p className="text-sm text-muted-foreground">UI and visualization tasks can begin once Phase 2 provides a stable baseline.</p>
                </div>

                <h4 className="font-semibold">Recommended Timeline</h4>
                <div className="grid md:grid-cols-4 gap-4 text-sm">
                  <div className="text-center">
                    <div className="font-semibold">Phase 1</div>
                    <div className="text-muted-foreground">2-3 weeks</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold">Phase 2</div>
                    <div className="text-muted-foreground">3-4 weeks</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold">Phase 3</div>
                    <div className="text-muted-foreground">4-5 weeks</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold">Phase 4</div>
                    <div className="text-muted-foreground">2-3 weeks</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Quality Assurance</h3>
            <div className="border rounded-lg p-6">
              <div className="space-y-4">
                <h4 className="font-semibold">Testing Strategy</h4>
                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <h5 className="font-semibold text-green-600">Unit Tests</h5>
                    <p className="text-sm text-muted-foreground">Individual component testing with 80%+ coverage</p>
                  </div>
                  <div>
                    <h5 className="font-semibold text-blue-600">Integration Tests</h5>
                    <p className="text-sm text-muted-foreground">End-to-end simulation testing</p>
                  </div>
                  <div>
                    <h5 className="font-semibold text-purple-600">Performance Tests</h5>
                    <p className="text-sm text-muted-foreground">Evolution speed and memory usage validation</p>
                  </div>
                </div>
                
                <h4 className="font-semibold">Review Process</h4>
                <ul className="text-sm space-y-1 ml-4">
                  <li>• Code reviews after each major task</li>
                  <li>• Weekly progress reviews</li>
                  <li>• Phase completion demonstrations</li>
                  <li>• Documentation updates with each milestone</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
