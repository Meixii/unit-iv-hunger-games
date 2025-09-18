import { Separator } from "@/components/ui/separator";

export default function Home() {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Evolve or Perish</h1>
        <p className="text-xl text-muted-foreground">
          An Animal Survival Simulation Using an Evolutionary Algorithm to Train a Multi-Layer Perceptron
        </p>
        <div className="flex gap-4 text-sm text-muted-foreground">
          <span><strong>Date:</strong> June 2026</span>
          <span><strong>Version:</strong> 1.0.0</span>
        </div>
      </div>
      
      <div className="space-y-6">

        <div className="bg-muted p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">Research Paper</h2>
          <p className="text-sm text-muted-foreground mb-2">Presented to the Faculty of The College of Liberal Arts and Sciences</p>
          <p className="text-sm text-muted-foreground mb-2">Congress Campus, Caloocan City</p>
          <p className="text-sm text-muted-foreground mb-4">In Partial Fulfillment of the Requirements for the Degree Bachelor of Science in Computer Science</p>
          
          <div className="space-y-2">
            <p className="font-semibold">Authors:</p>
            <div className="grid md:grid-cols-2 gap-2 text-sm">
              <div>• Ma. Catherine H. Bae</div>
              <div>• Emann Pabua</div>
              <div>• Irheil Mae S. Antang</div>
              <div>• Jhon Keneth Ryan B. Namias</div>
              <div>• Jin Harold A. Failana</div>
              <div>• Kevin A. Llanes</div>
              <div>• Ronan Renz T. Valencia</div>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Project Objectives</h2>
          
          <div className="border rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">General Objective</h3>
            <p className="text-muted-foreground">
              To design and develop a competitive survival simulation where a Multi-Layer Perceptron, trained by an evolutionary algorithm, learns to effectively control an animal's behavior. The project aims to demonstrate how evolutionary processes can optimize a neural network's decision-making capabilities for survival within a dynamic, resource-limited, and hazardous environment.
            </p>
          </div>

          <div className="border rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">Specific Objectives</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• To classify animals into three categories (herbivore, carnivore, omnivore) with unique survival skills and behaviors</li>
              <li>• To create a training system that uses evolutionary algorithms where animals can improve their behaviors by facing different survival events and scenarios across generations</li>
              <li>• To design and implement a multi-layered event system featuring: AI-driven Movement Events, player-interactive Quick Events, simulation-wide Random Events, and hazardous Disasters that occur on a structured weekly cycle</li>
              <li>• To develop a competitive survival simulation where AI-driven animals, managed by a Multi-Layer Perceptron trained through evolutionary algorithms, experience survival across multiple generations within a dynamic environment</li>
              <li>• To enable the MLP to make decisions for basic actions (moving, hunting, drinking, fleeing) based on the animal's core Status inputs (Health, Hunger, Thirst, Energy, Instinct)</li>
              <li>• To simulate users with different kinds of events, including hunting, migration, and resource collection</li>
              <li>• To create an environment with diverse terrains, such as jungle, lake, and plains</li>
              <li>• To create a system that displays animal skills based on specific statuses such as health, hunger, thirst, energy, and instinct</li>
            </ul>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Project Scope</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">1. Multi-Layer Perceptron Architecture</h3>
              <p className="text-sm text-muted-foreground">Implementation of neural networks with input layers (environmental sensors), multiple hidden layers (behavioral processing), and output layers (action selection) specifically designed for animal behavior control.</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">2. Evolutionary Training System</h3>
              <p className="text-sm text-muted-foreground">Development of genetic algorithms that adjust MLP weights and biases using competitive selection, optimization, and mutation strategies to progressively improve animal behaviors.</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">3. Competitive Hunger Games Environment</h3>
              <p className="text-sm text-muted-foreground">Creation of a survival simulation featuring resource management, environmental hazards, and inter-animal competition where trained MLPs control animal decision-making.</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">4. Random Environmental Event System</h3>
              <p className="text-sm text-muted-foreground">Dynamic environmental challenges including meteors (area damage), storms (visibility reduction), resource depletion events, and terrain changes that test animal adaptability and survival instincts.</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">5. Grid Map Navigation</h3>
              <p className="text-sm text-muted-foreground">Dynamic grid-based map environment where animals navigate across cells, enabling structured movement, interaction, and spatial awareness within the simulation.</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">6. Grid-Based Random Spawning System</h3>
              <p className="text-sm text-muted-foreground">Implementation of a map divided into grids with a neighbor-aware spawning system, ensuring balanced and randomized placement of animals, resources, and hazards while maintaining strategic spatial interactions.</p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Project Limitations</h2>
          <div className="space-y-3 text-sm text-muted-foreground">
            <div className="border rounded p-4">
              <h3 className="font-semibold text-orange-600 mb-2">MLP Architecture Constraints</h3>
              <p>The neural network complexity will be limited to 2-3 hidden layers to maintain computational feasibility during 10-20 minute classroom sessions while demonstrating multi-layer learning capabilities.</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-semibold text-orange-600 mb-2">Session Duration Limitations</h3>
              <p>Game sessions will be constrained to 10-20 minutes to fit classroom schedules, limiting the number of evolutionary generations and behavioral complexity that can be demonstrated.</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-semibold text-orange-600 mb-2">Simplified Environmental Model</h3>
              <p>The battle royale environment will use a 2D grid-based representation with text-based gameplay and static chibi images rather than complex 3D graphics or real-time animations.</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-semibold text-orange-600 mb-2">Population Balance Constraints</h3>
              <p>Animal populations will be artificially balanced (ratios dependent on class size) rather than naturally emerging ecosystem dynamics to ensure fair gameplay within time limits.</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-semibold text-orange-600 mb-2">Behavioral Complexity Boundaries</h3>
              <p>Animal behaviors, while driven by a neural network, will be primarily reactive to immediate Status needs (e.g., low hunger triggers food-seeking) and sensory information within a limited range, rather than complex, long-term strategic planning.</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-semibold text-orange-600 mb-2">Player Interaction</h3>
              <p>Direct player control is intentionally limited to the initial 'Training' phase and timed 'Quick Events.' The core gameplay loop, including movement and resource gathering, is fully autonomous and governed by the animal's evolved MLP, reinforcing the project's focus on evolutionary algorithms.</p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Quick Start</h2>
          <div className="bg-muted p-4 rounded-lg">
            <p className="text-sm">
              Explore the documentation using the sidebar navigation to learn about core concepts, 
              game mechanics, technical implementation details, and development phases.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}