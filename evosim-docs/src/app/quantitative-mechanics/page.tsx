import { Separator } from "@/components/ui/separator";

export default function QuantitativeMechanicsPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Quantitative Mechanics & Balancing</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section centralizes all numerical values for easy tuning and reference.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">World Generation Parameters</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Grid Size</h4>
                <p className="text-2xl font-mono">25x25 tiles</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Terrain Distribution</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Plains:</span>
                    <span className="font-mono">60%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Forest:</span>
                    <span className="font-mono">25%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Water:</span>
                    <span className="font-mono">10%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Mountains:</span>
                    <span className="font-mono">5%</span>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Resource Density</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Food Source Chance:</span>
                    <span className="font-mono">15%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Water Source Chance:</span>
                    <span className="font-mono">5%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Animal Parameters</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Trait Ranges</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Standard Trait Range:</span>
                    <span className="font-mono">4-6</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Primary Trait Range:</span>
                    <span className="font-mono">7-9</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Initial Training Bonus:</span>
                    <span className="font-mono">+1 per question (5 total)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Status Dynamics (per Movement Event)</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Depletion Rates</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Hunger Depletion:</span>
                    <span className="font-mono text-red-600">-5</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Thirst Depletion:</span>
                    <span className="font-mono text-red-600">-8</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Passive Energy Regen:</span>
                    <span className="font-mono text-green-600">+10</span>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Damage Values</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Starvation Damage:</span>
                    <span className="font-mono text-red-600">-5 Health/turn</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Dehydration Damage:</span>
                    <span className="font-mono text-red-600">-10 Health/turn</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Passive & Effect Modifiers</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Passive Abilities</h4>
                <div className="grid gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Ambush Predator (Carnivore):</span>
                    <span className="font-mono">1.5x first attack damage</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Efficient Grazer (Herbivore):</span>
                    <span className="font-mono">1.25x food gains</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Iron Stomach (Omnivore):</span>
                    <span className="font-mono">50% debuff resistance</span>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Effect Durations</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="flex justify-between">
                    <span>Buffs (Default):</span>
                    <span className="font-mono">3 turns</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Debuffs (Default):</span>
                    <span className="font-mono">5 turns</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Fitness Score Weights</h3>
            <div className="border rounded-lg p-4">
              <div className="grid gap-2">
                <div className="flex justify-between">
                  <span>Time Survived (per turn):</span>
                  <span className="font-mono">1</span>
                </div>
                <div className="flex justify-between">
                  <span>Resources Gathered (per 40 units):</span>
                  <span className="font-mono">5</span>
                </div>
                <div className="flex justify-between">
                  <span>Kills:</span>
                  <span className="font-mono text-red-600">50</span>
                </div>
                <div className="flex justify-between">
                  <span>Distance Traveled (per tile):</span>
                  <span className="font-mono">0.2</span>
                </div>
                <div className="flex justify-between">
                  <span>Events Survived:</span>
                  <span className="font-mono">10</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
