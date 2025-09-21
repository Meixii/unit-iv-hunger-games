import { Separator } from "@/components/ui/separator";

export default function FitnessFunctionPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Fitness Function & Generational Goals</h1>
        <p className="text-lg text-muted-foreground">
          This section defines the precise formula for calculating an animal&apos;s fitness and the high-level objectives for each evolutionary generation.
        </p>
      </div>
      
      <div className="space-y-8">

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Fitness Function Rationale</h3>
            <p>
              The goal of the fitness function is to provide a single, quantitative measure of an animal&apos;s success. This value guides the Evolutionary Algorithm by rewarding beneficial strategies and behaviors.
            </p>
            
            <div className="bg-muted p-6 rounded-lg">
              <h4 className="font-semibold mb-2">Formula:</h4>
              <code className="text-sm">
                Fitness Score = (Time Survived * W_Time) + (Resources Gathered * W_Resource) + (Kills * W_Kills) + (Distance Traveled * W_Distance) + (Events Survived * W_Events)
              </code>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Fitness Components</h4>
              <div className="grid gap-4">
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-blue-600">Time Survived</h5>
                  <p className="text-sm text-muted-foreground">
                    The most crucial component. It directly rewards the primary objective of survival. An animal that learns to effectively manage its needs and avoid danger will live longer and thus have a higher base fitness.
                  </p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-green-600">Resources Gathered</h5>
                  <p className="text-sm text-muted-foreground">
                    This incentivizes the MLP to learn proactive behaviors. It&apos;s not enough to simply hide; an animal must actively seek out food and water to replenish its status, and this term rewards that efficiency.
                  </p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-red-600">Kills</h5>
                  <p className="text-sm text-muted-foreground">
                    This component is essential for making the Carnivore category viable. It provides a significant fitness boost for successful predatory behavior, encouraging the evolution of effective hunting strategies.
                  </p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-purple-600">Distance Traveled</h5>
                  <p className="text-sm text-muted-foreground">
                    This provides a minor incentive for exploration. It is designed to prevent passive strategies (e.g., an animal finding one resource patch and never leaving) from becoming dominant, encouraging the MLP to learn to navigate the wider world.
                  </p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-orange-600">Events Survived</h5>
                  <p className="text-sm text-muted-foreground">
                    This rewards adaptability. By providing a fitness bonus for successfully navigating Triggered Events, we encourage the evolution of more flexible and &quot;intelligent&quot; MLPs that can handle unexpected situations.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <Separator />

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Generational Goals</h3>
            <p>These are the high-level objectives we aim to observe as the simulation progresses through multiple generations.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Primary Goal</h4>
              <div className="border rounded-lg p-4 bg-blue-50 dark:bg-blue-950">
                <p className="font-semibold text-blue-800 dark:text-blue-200">Increase Average Fitness</p>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  The main indicator of successful learning is a clear upward trend in the average fitness score of the population from one generation to the next.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Secondary Goals</h4>
              <div className="grid gap-4">
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold">Observe Adaptation</h5>
                  <p className="text-sm text-muted-foreground">
                    We expect to see the population&apos;s average traits shift in response to environmental pressures. For instance, in a world with frequent &quot;Harsh Winter&quot; disasters, animals with higher Endurance should have higher fitness scores, leading to a gradual increase in the average Endurance of the population over generations.
                  </p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold">Promote Specialization</h5>
                  <p className="text-sm text-muted-foreground">
                    Each animal category should develop distinct, successful strategies. Carnivores should evolve MLPs that are adept at hunting. Herbivores should evolve MLPs that excel at locating plants and evading threats. Omnivores should evolve flexible MLPs that can switch between scavenging, grazing, and opportunistic hunting.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
