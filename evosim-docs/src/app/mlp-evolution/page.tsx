import { Separator } from "@/components/ui/separator";

export default function MLPEvolutionPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">MLP & Evolutionary Algorithm Design</h1>
        <p className="text-lg text-muted-foreground">
          This section details the technical architecture of the neural network and the mechanics of the genetic algorithm.
        </p>
      </div>
      
      <div className="space-y-8">

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Multi-Layer Perceptron (MLP) Architecture</h3>
            <p>
              The MLP serves as the decision-making core for each animal. Its weights and biases are the &quot;genes&quot; that will be evolved.
            </p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">1. Input Layer</h4>
              <p>The sensory information provided to the MLP. It&apos;s a flattened vector of normalized values (0.0 to 1.0) representing:</p>
              <ul className="space-y-2 ml-4">
                <li><strong>Internal Status (5 nodes):</strong> Health %, Hunger %, Thirst %, Energy %, and Instinct (0 for Calm, 1 for Alert).</li>
                <li><strong>Sensory Grid (Perception-based):</strong> A 3x3 grid of tiles centered on the animal. For each of the 9 tiles, the following data is included:
                  <ul className="ml-4 mt-2 space-y-1">
                    <li>• Is it a threat? (e.g., Fire, Flood) (1 node)</li>
                    <li>• Is there a food source? (1 node)</li>
                    <li>• Is there a water source? (1 node)</li>
                    <li>• Is there another animal? (1 node)</li>
                  </ul>
                </li>
              </ul>
              <div className="bg-muted p-4 rounded-lg">
                <p className="font-semibold">Total Input Nodes: 5 (Internal) + 9 tiles * 4 data points/tile = 41 nodes.</p>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">2. Hidden Layers</h4>
              <p>The processing layers of the network. To adhere to project limitations while providing sufficient complexity, the architecture will be:</p>
              <ul className="space-y-2 ml-4">
                <li><strong>Hidden Layer 1:</strong> 16 neurons with a ReLU activation function.</li>
                <li><strong>Hidden Layer 2:</strong> 12 neurons with a ReLU activation function.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">3. Output Layer</h4>
              <p>The layer that determines the animal&apos;s action. The neuron with the highest activation value is the chosen action for the turn.</p>
              
              <div className="space-y-2">
                <p><strong>Output Actions (8 nodes):</strong></p>
                <ul className="grid grid-cols-2 gap-2 ml-4">
                  <li>• Move North</li>
                  <li>• Move East</li>
                  <li>• Move South</li>
                  <li>• Move West</li>
                  <li>• Rest (Conserve/Regain Energy)</li>
                  <li>• Eat (If food is on the current tile)</li>
                  <li>• Drink (If adjacent to a water tile)</li>
                  <li>• Attack (If another animal is on the current tile)</li>
                </ul>
              </div>
              
              <div className="bg-muted p-4 rounded-lg">
                <p><strong>Activation Function:</strong> Softmax, to ensure a clear &quot;choice&quot; among the possible actions.</p>
              </div>
            </div>
          </div>

          <Separator />

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Evolutionary Algorithm (EA) Mechanics</h3>
            <p>This is the process for training the population of MLPs across generations.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">1. Initialization</h4>
              <p>For Generation 0, a population of animals is created. Each animal is assigned an MLP with its weights and biases initialized to small, random values.</p>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">2. Evaluation</h4>
              <p>The entire simulation is run for a fixed number of &quot;weeks.&quot; As each animal perishes or when the simulation ends, its performance is calculated using the Fitness Function.</p>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">3. Selection</h4>
              <p>The top-performing animals are selected to become &quot;parents&quot; for the next generation.</p>
              <ul className="space-y-2 ml-4">
                <li><strong>Elitism:</strong> The top 10% of the population (based on fitness score) are automatically carried over to the next generation unchanged.</li>
                <li><strong>Tournament Selection:</strong> To fill the remaining 90% of the new population, pairs of &quot;parents&quot; are chosen. A small group of animals (e.g., 5) is randomly selected from the previous generation, and the one with the highest fitness score in that group wins the &quot;tournament&quot; and is chosen as a parent.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">4. Crossover (Reproduction)</h4>
              <p>For each new offspring, two parents selected via the tournament are combined.</p>
              <p><strong>Method:</strong> The weights of both parent MLPs are flattened into single arrays. A random crossover point is chosen. The offspring inherits all weights before the crossover point from Parent A and all weights after the point from Parent B.</p>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">5. Mutation</h4>
              <p>To introduce new genetic diversity, the offspring&apos;s MLP weights are slightly and randomly altered.</p>
              <p><strong>Method:</strong> For each weight in the offspring&apos;s network, there is a small mutation chance (e.g., 2%). If mutation occurs, a small random value (from a Gaussian distribution) is added to the existing weight.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
