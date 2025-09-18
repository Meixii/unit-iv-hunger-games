import { Separator } from "@/components/ui/separator";

export default function MapObjectivesPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Map and Objectives</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section details the design of the grid-based map, including terrains, resource distribution, and the ultimate win/loss conditions for the animals.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Map Structure</h3>
            <p>The world is a pre-designed, grid-based environment. The coordinate system allows for precise tracking of all entities.</p>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Terrain Types & Effects</h3>
            <p>Each grid cell has a terrain type that directly impacts gameplay.</p>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-green-600">Plains</h4>
                <p className="text-sm text-muted-foreground">The standard terrain. No bonus or penalty. Movement cost is normal. Standard resource density.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-green-800">Forest</h4>
                <p className="text-sm text-muted-foreground">Dense woodland. Increased movement cost (x1.5). Provides a "Hidden" status, preventing detection from animals more than 2 tiles away. High density of plant-based food.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-green-900">Jungle</h4>
                <p className="text-sm text-muted-foreground">A more extreme and dangerous forest. High movement cost (x2.0). High chance of encountering poisonous plants. Very high density of rare, high-value plants.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-blue-600">Water (River/Lake)</h4>
                <p className="text-sm text-muted-foreground">A source of hydration. Cannot be moved onto, but animals on adjacent tiles can drink. Acts as a natural barrier.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-yellow-600">Swamp</h4>
                <p className="text-sm text-muted-foreground">Fetid marshland. Increased movement cost (x1.8). Each turn spent in a swamp tile has a 10% chance to inflict the Sick debuff. Contains unique scavenging opportunities for Omnivores.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-gray-600">Mountains</h4>
                <p className="text-sm text-muted-foreground">Impassable rock. Acts as a permanent wall, blocking movement and line of sight.</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Resource Distribution</h3>
            <p>Resources are strategically placed based on terrain.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Food</h4>
              <ul className="space-y-2 ml-4">
                <li><strong>Plants (Herbivore/Omnivore):</strong> Spawn with high frequency in Forests and Plains. Rare, high-nutrient plants spawn only in Jungles.</li>
                <li><strong>Prey (Carnivore):</strong> Small AI creatures spawn and move randomly within Plains tiles.</li>
                <li><strong>Carcasses (Omnivore/Carnivore):</strong> Have a chance to appear after an animal is defeated or during certain events. More common in Swamps.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Water</h4>
              <p>Spawns in clusters to form Lakes and lines to form Rivers.</p>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Objectives & Win Conditions</h3>
            <p>The ultimate goal is to produce the most "fit" animal for the next generation.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Primary Objective (Winning a Round)</h4>
              <div className="border rounded-lg p-4 bg-blue-50 dark:bg-blue-950">
                <p className="font-semibold">Be the last animal standing.</p>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Secondary Objective (Driving Evolution)</h4>
              <div className="border rounded-lg p-4">
                <p className="font-semibold">Achieve the highest possible Fitness Score.</p>
                <p className="text-sm text-muted-foreground">This score, calculated at the moment of an animal's death (or the end of the simulation), determines its evolutionary success.</p>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Fitness Score Calculation</h4>
              <div className="bg-muted p-4 rounded-lg">
                <code className="text-sm">
                  Fitness Score = (Time Survived * W_Time) + (Resources Gathered * W_Resource) + (Kills * W_Kills) + (Distance Traveled * W_Distance) + (Events Survived * W_Events)
                </code>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Weights (W)</h4>
              <p>These values are critical for balancing what the algorithm prioritizes.</p>
              <div className="grid gap-2">
                <div className="flex justify-between p-2 border rounded">
                  <span><strong>W_Time:</strong></span>
                  <span>Rewards longevity and endurance.</span>
                </div>
                <div className="flex justify-between p-2 border rounded">
                  <span><strong>W_Resource:</strong></span>
                  <span>Rewards efficient resource management.</span>
                </div>
                <div className="flex justify-between p-2 border rounded">
                  <span><strong>W_Kills:</strong></span>
                  <span>Heavily rewards aggressive, successful carnivore behavior.</span>
                </div>
                <div className="flex justify-between p-2 border rounded">
                  <span><strong>W_Distance:</strong></span>
                  <span>Lightly rewards exploration to discourage overly passive strategies.</span>
                </div>
                <div className="flex justify-between p-2 border rounded">
                  <span><strong>W_Events:</strong></span>
                  <span>Rewards adaptable decision-making in special circumstances.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
