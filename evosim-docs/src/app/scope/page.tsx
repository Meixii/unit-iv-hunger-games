import { Separator } from "@/components/ui/separator";

export default function ScopePage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Project Scope</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            The project scope defines the boundaries and extent of the EvoSim project, outlining the key technical components and systems that will be implemented.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Core Technical Components</h3>
            <div className="grid gap-6">
              <div className="border rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm">1</div>
                  <div className="flex-1">
                    <h4 className="text-xl font-semibold mb-3">Multi-Layer Perceptron Architecture</h4>
                    <p className="text-muted-foreground mb-4">
                      Implementation of neural networks with input layers (environmental sensors), multiple hidden layers (behavioral processing), and output layers (action selection) specifically designed for animal behavior control.
                    </p>
                    <div className="bg-muted p-3 rounded">
                      <h5 className="font-semibold mb-2">Key Features:</h5>
                      <ul className="text-sm space-y-1">
                        <li>• Environmental sensor input processing</li>
                        <li>• Multi-layer behavioral decision making</li>
                        <li>• Action selection output mechanisms</li>
                        <li>• Real-time neural network processing</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold text-sm">2</div>
                  <div className="flex-1">
                    <h4 className="text-xl font-semibold mb-3">Evolutionary Training System</h4>
                    <p className="text-muted-foreground mb-4">
                      Development of genetic algorithms that adjust MLP weights and biases using competitive selection, optimization, and mutation strategies to progressively improve animal behaviors.
                    </p>
                    <div className="bg-muted p-3 rounded">
                      <h5 className="font-semibold mb-2">Key Features:</h5>
                      <ul className="text-sm space-y-1">
                        <li>• Genetic algorithm implementation</li>
                        <li>• Weight and bias optimization</li>
                        <li>• Competitive selection mechanisms</li>
                        <li>• Mutation and crossover strategies</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="w-8 h-8 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-sm">3</div>
                  <div className="flex-1">
                    <h4 className="text-xl font-semibold mb-3">Competitive Hunger Games Environment</h4>
                    <p className="text-muted-foreground mb-4">
                      Creation of a survival simulation featuring resource management, environmental hazards, and inter-animal competition where trained MLPs control animal decision-making.
                    </p>
                    <div className="bg-muted p-3 rounded">
                      <h5 className="font-semibold mb-2">Key Features:</h5>
                      <ul className="text-sm space-y-1">
                        <li>• Resource management systems</li>
                        <li>• Environmental hazard simulation</li>
                        <li>• Inter-animal competition mechanics</li>
                        <li>• MLP-controlled decision making</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold text-sm">4</div>
                  <div className="flex-1">
                    <h4 className="text-xl font-semibold mb-3">Random Environmental Event System</h4>
                    <p className="text-muted-foreground mb-4">
                      Dynamic environmental challenges including meteors (area damage), storms (visibility reduction), resource depletion events, and terrain changes that test animal adaptability and survival instincts.
                    </p>
                    <div className="bg-muted p-3 rounded">
                      <h5 className="font-semibold mb-2">Key Features:</h5>
                      <ul className="text-sm space-y-1">
                        <li>• Dynamic environmental challenges</li>
                        <li>• Area damage events (meteors)</li>
                        <li>• Visibility reduction (storms)</li>
                        <li>• Resource depletion scenarios</li>
                        <li>• Terrain change events</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="w-8 h-8 bg-orange-600 text-white rounded-full flex items-center justify-center font-bold text-sm">5</div>
                  <div className="flex-1">
                    <h4 className="text-xl font-semibold mb-3">Grid Map Navigation</h4>
                    <p className="text-muted-foreground mb-4">
                      Dynamic grid-based map environment where animals navigate across cells, enabling structured movement, interaction, and spatial awareness within the simulation.
                    </p>
                    <div className="bg-muted p-3 rounded">
                      <h5 className="font-semibold mb-2">Key Features:</h5>
                      <ul className="text-sm space-y-1">
                        <li>• Grid-based map system</li>
                        <li>• Structured movement mechanics</li>
                        <li>• Spatial interaction capabilities</li>
                        <li>• Dynamic navigation algorithms</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="w-8 h-8 bg-cyan-600 text-white rounded-full flex items-center justify-center font-bold text-sm">6</div>
                  <div className="flex-1">
                    <h4 className="text-xl font-semibold mb-3">Grid-Based Random Spawning System</h4>
                    <p className="text-muted-foreground mb-4">
                      Implementation of a map divided into grids with a neighbor-aware spawning system, ensuring balanced and randomized placement of animals, resources, and hazards while maintaining strategic spatial interactions.
                    </p>
                    <div className="bg-muted p-3 rounded">
                      <h5 className="font-semibold mb-2">Key Features:</h5>
                      <ul className="text-sm space-y-1">
                        <li>• Neighbor-aware spawning algorithms</li>
                        <li>• Balanced resource placement</li>
                        <li>• Randomized hazard distribution</li>
                        <li>• Strategic spatial interaction maintenance</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Implementation Scope</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Included in Scope</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Complete MLP neural network implementation</li>
                  <li>• Full evolutionary algorithm system</li>
                  <li>• Grid-based world generation</li>
                  <li>• Event and disaster systems</li>
                  <li>• Animal behavior simulation</li>
                  <li>• Resource management mechanics</li>
                  <li>• Competitive survival gameplay</li>
                </ul>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Out of Scope</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• 3D graphics or complex animations</li>
                  <li>• Real-time multiplayer networking</li>
                  <li>• Advanced AI pathfinding</li>
                  <li>• Complex physics simulation</li>
                  <li>• Database integration</li>
                  <li>• Mobile platform support</li>
                  <li>• Cloud-based processing</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
