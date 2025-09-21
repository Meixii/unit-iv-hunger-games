import { Separator } from "@/components/ui/separator";

export default function ObjectivesPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Project Objectives</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            The project aims to demonstrate how evolutionary processes can optimize a neural network&apos;s decision-making capabilities for survival within a dynamic, resource-limited, and hazardous environment.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">General Objective</h3>
            <div className="border rounded-lg p-6 bg-blue-50 dark:bg-blue-950">
              <p className="text-muted-foreground">
                To design and develop a competitive survival simulation where a Multi-Layer Perceptron, trained by an evolutionary algorithm, learns to effectively control an animal&apos;s behavior. The project aims to demonstrate how evolutionary processes can optimize a neural network&apos;s decision-making capabilities for survival within a dynamic, resource-limited, and hazardous environment.
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Specific Objectives</h3>
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Animal Classification System</h4>
                <p className="text-sm text-muted-foreground">To classify animals into three categories (herbivore, carnivore, omnivore) with unique survival skills and behaviors</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Evolutionary Training System</h4>
                <p className="text-sm text-muted-foreground">To create a training system that uses evolutionary algorithms where animals can improve their behaviors by facing different survival events and scenarios across generations</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Multi-Layered Event System</h4>
                <p className="text-sm text-muted-foreground">To design and implement a multi-layered event system featuring: AI-driven Movement Events, player-interactive Quick Events, simulation-wide Random Events, and hazardous Disasters that occur on a structured weekly cycle</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Competitive Survival Simulation</h4>
                <p className="text-sm text-muted-foreground">To develop a competitive survival simulation where AI-driven animals, managed by a Multi-Layer Perceptron trained through evolutionary algorithms, experience survival across multiple generations within a dynamic environment</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">MLP Decision Making</h4>
                <p className="text-sm text-muted-foreground">To enable the MLP to make decisions for basic actions (moving, hunting, drinking, fleeing) based on the animal&apos;s core Status inputs (Health, Hunger, Thirst, Energy, Instinct)</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Event Simulation</h4>
                <p className="text-sm text-muted-foreground">To simulate users with different kinds of events, including hunting, migration, and resource collection</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Diverse Environment</h4>
                <p className="text-sm text-muted-foreground">To create an environment with diverse terrains, such as jungle, lake, and plains</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Status-Based Skills System</h4>
                <p className="text-sm text-muted-foreground">To create a system that displays animal skills based on specific statuses such as health, hunger, thirst, energy, and instinct</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Expected Outcomes</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-green-600 mb-2">Technical Achievement</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Successful implementation of MLP architecture</li>
                  <li>• Effective evolutionary algorithm training</li>
                  <li>• Dynamic event system functionality</li>
                  <li>• Grid-based navigation system</li>
                </ul>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-blue-600 mb-2">Educational Value</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Demonstration of evolutionary algorithms</li>
                  <li>• Neural network behavior learning</li>
                  <li>• Competitive simulation mechanics</li>
                  <li>• Real-time decision making processes</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
