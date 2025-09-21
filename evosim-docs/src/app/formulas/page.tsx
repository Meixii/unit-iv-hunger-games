import { Separator } from "@/components/ui/separator";

export default function FormulasPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Formulas & Computations Summary</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section compiles all core formulas and checks from across the document into a single, easy-to-reference location.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Animal Stat Calculations</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Max Health</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">BASE_HEALTH + (animal.END * HEALTH_PER_ENDURANCE)</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Where BASE_HEALTH = 100, HEALTH_PER_ENDURANCE = 10</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Max Energy</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">BASE_ENERGY + (animal.END * ENERGY_PER_ENDURANCE)</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Where BASE_ENERGY = 100, ENERGY_PER_ENDURANCE = 5</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Action & Combat Calculations</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Movement Energy Cost</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">(MOVEMENT_BASE_COST * TERRAIN_MOVEMENT_MODIFIERS[terrain]) - (animal.AGI * MOVEMENT_AGILITY_MULTIPLIER)</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Where MOVEMENT_BASE_COST = 10, MOVEMENT_AGILITY_MULTIPLIER = 0.5</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Combat Damage</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">(attacker.STR * STRENGTH_DAMAGE_MULTIPLIER) - defender.AGI</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Where STRENGTH_DAMAGE_MULTIPLIER = 2</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Evasion Chance</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">defender.AGI * AGILITY_EVASION_MULTIPLIER</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Result is a percentage. AGILITY_EVASION_MULTIPLIER = 5</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Time Complexity</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">O(1)</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Single Action complexity</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Passive Ability Modifiers</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Ambush Predator Damage</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">Combat Damage * AMBUSH_PREDATOR_MULTIPLIER</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Where AMBUSH_PREDATOR_MULTIPLIER = 1.5</p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Efficient Grazer Gain</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">PLANT_FOOD_GAIN * EFFICIENT_GRAZER_MULTIPLIER</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Where EFFICIENT_GRAZER_MULTIPLIER = 1.25</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Event & Check Calculations</h3>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Success Check (General Formula)</h4>
                <div className="bg-muted p-3 rounded mt-2">
                  <code className="text-sm">roll(d10) + animal.Trait &gt;= DC</code>
                </div>
                <p className="text-sm text-muted-foreground mt-2">General formula for all trait-based checks</p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="border rounded-lg p-4">
                  <h4 className="font-semibold">Rockslide Escape Check</h4>
                  <div className="bg-muted p-3 rounded mt-2">
                    <code className="text-sm">roll(d10) + animal.AGI &gt;= 14</code>
                  </div>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h4 className="font-semibold">Rockslide Hide Check</h4>
                  <div className="bg-muted p-3 rounded mt-2">
                    <code className="text-sm">roll(d10) + animal.END &gt;= 12</code>
                  </div>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h4 className="font-semibold">Curious Object Check</h4>
                  <div className="bg-muted p-3 rounded mt-2">
                    <code className="text-sm">roll(d10) + animal.INT &gt;= 13</code>
                  </div>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h4 className="font-semibold">Contamination Save Check</h4>
                  <div className="bg-muted p-3 rounded mt-2">
                    <code className="text-sm">roll(d10) + animal.END &gt;= 10</code>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Fitness Score Calculation</h3>
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold">Complete Formula</h4>
              <div className="bg-muted p-4 rounded mt-2">
                  <code className="text-sm">
                    Fitness Score = (Time Survived * W[&apos;Time&apos;]) + (Resources Gathered / 40 * W[&apos;Resource&apos;]) + (Kills * W[&apos;Kill&apos;]) + (Distance * W[&apos;Distance&apos;]) + (Events Survived * W[&apos;Event&apos;])
                  </code>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p><strong>Weights (W):</strong></p>
                  <ul className="ml-4 space-y-1">
                    <li>• Time: 1</li>
                    <li>• Resource: 5</li>
                    <li>• Kill: 50</li>
                  </ul>
                </div>
                <div>
                  <p><strong>Weights (W):</strong></p>
                  <ul className="ml-4 space-y-1">
                    <li>• Distance: 0.2</li>
                    <li>• Event: 10</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
