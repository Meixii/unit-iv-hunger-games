import { Separator } from "@/components/ui/separator";

export default function ParametersPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Parameters and Variables</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section lists and defines the key attributes for animals, the environment, and the simulation itself, like health points, sensor ranges, and resource density.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Animal Categories</h3>
            <p>The foundational archetypes for our creatures.</p>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="border rounded-lg p-4 text-center">
                <h4 className="font-semibold text-green-600">Herbivore</h4>
                <p className="text-sm text-muted-foreground">Plant-based diet</p>
              </div>
              <div className="border rounded-lg p-4 text-center">
                <h4 className="font-semibold text-red-600">Carnivore</h4>
                <p className="text-sm text-muted-foreground">Meat-based diet</p>
              </div>
              <div className="border rounded-lg p-4 text-center">
                <h4 className="font-semibold text-blue-600">Omnivore</h4>
                <p className="text-sm text-muted-foreground">Mixed diet</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Traits</h3>
            <p>Core genetic attributes that define an animal's capabilities (Scale: 1-10). These will be the values the evolutionary algorithm tunes.</p>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Strength (STR)</h4>
                <p className="text-sm text-muted-foreground">Influences combat damage.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Agility (AGI)</h4>
                <p className="text-sm text-muted-foreground">Affects movement speed, evasion, and energy efficiency.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Intelligence (INT)</h4>
                <p className="text-sm text-muted-foreground">Could influence learning rate or effectiveness in Triggered Events.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Endurance (END)</h4>
                <p className="text-sm text-muted-foreground">Determines base Health and Energy pools.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Perception (PER)</h4>
                <p className="text-sm text-muted-foreground">Affects the range at which an animal can detect resources or other animals.</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Status</h3>
            <p>Dynamic variables reflecting an animal's current well-being. These are critical inputs for the MLP.</p>
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Health</h4>
                <p className="text-sm text-muted-foreground">Animal's life force. If it reaches 0, the animal perishes. Calculated as 100 + (Endurance * 10). Does not regenerate passively.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Hunger</h4>
                <p className="text-sm text-muted-foreground">Scale of 0-100. Decreases with every turn. At 0, the animal begins to starve and loses health.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Thirst</h4>
                <p className="text-sm text-muted-foreground">Scale of 0-100. Decreases with every turn, typically faster than hunger. At 0, the animal becomes dehydrated and loses health at a severe rate.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Energy</h4>
                <p className="text-sm text-muted-foreground">Consumed by actions. Replenished by resting or passively at a slow rate. Calculated as 100 + (Endurance * 5). Reaching 0 causes Exhaustion.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Instinct (Danger Level)</h4>
                <p className="text-sm text-muted-foreground">A state (e.g., Calm or Alert). Becomes "Alert" when health is low, a predator is nearby, or during a disaster. This state is a direct input to the MLP to influence its decision-making priorities (e.g., flee vs. eat).</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Passives & Effects</h3>
            <p>Modifiers that influence Traits or Status.</p>
            
            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Passives</h4>
              <p>Innate, category-specific abilities that are always active.</p>
              <div className="grid gap-4">
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-red-600">Carnivore - Ambush Predator</h5>
                  <p className="text-sm text-muted-foreground">The first attack against another animal in an encounter deals bonus damage. This incentivizes hunting over prolonged fights.</p>
                </div>
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-green-600">Herbivore - Efficient Grazer</h5>
                  <p className="text-sm text-muted-foreground">Gains 25% more Hunger and Energy from any plant-based food source. This allows them to spend less time eating and more time moving or hiding.</p>
                </div>
                <div className="border rounded-lg p-4">
                  <h5 className="font-semibold text-blue-600">Omnivore - Iron Stomach</h5>
                  <p className="text-sm text-muted-foreground">Has a high resistance to negative effects from food or water sources (e.g., "Sick" or "Poisoned"). This makes them excellent scavengers and adaptable survivors.</p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xl font-semibold">Effects (Buffs/Debuffs)</h4>
              <p>Temporary modifiers from the environment or interactions. These have a duration (e.g., number of turns).</p>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <h5 className="font-semibold text-green-600">Good Effects (Buffs)</h5>
                  <div className="space-y-2">
                    <div className="border rounded p-3">
                      <p className="font-medium">Well-Fed</p>
                      <p className="text-xs text-muted-foreground">Temporary +1 STR, +1 END. (Trigger: Hunger &gt; 90%)</p>
                    </div>
                    <div className="border rounded p-3">
                      <p className="font-medium">Hydrated</p>
                      <p className="text-xs text-muted-foreground">Temporary +1 AGI, faster passive energy regeneration. (Trigger: Thirst &gt; 90%)</p>
                    </div>
                    <div className="border rounded p-3">
                      <p className="font-medium">Rested</p>
                      <p className="text-xs text-muted-foreground">Significant boost to energy regeneration for 3 turns. (Trigger: Taking the 'Rest' action)</p>
                    </div>
                    <div className="border rounded p-3">
                      <p className="font-medium">Adrenaline Rush</p>
                      <p className="text-xs text-muted-foreground">+2 STR, +2 AGI for 2 turns, but energy drains faster. (Trigger: Quick Event or low health)</p>
                    </div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h5 className="font-semibold text-red-600">Bad Effects (Debuffs)</h5>
                  <div className="space-y-2">
                    <div className="border rounded p-3">
                      <p className="font-medium">Injured</p>
                      <p className="text-xs text-muted-foreground">-2 AGI until healed. (Trigger: Taking significant damage)</p>
                    </div>
                    <div className="border rounded p-3">
                      <p className="font-medium">Poisoned</p>
                      <p className="text-xs text-muted-foreground">Lose a fixed amount of health per turn for 5 turns. (Trigger: Eating a poisonous plant, disaster)</p>
                    </div>
                    <div className="border rounded p-3">
                      <p className="font-medium">Exhausted</p>
                      <p className="text-xs text-muted-foreground">Energy regeneration is halved. (Trigger: Energy drops to 0)</p>
                    </div>
                    <div className="border rounded p-3">
                      <p className="font-medium">Sick</p>
                      <p className="text-xs text-muted-foreground">-1 to all traits. (Trigger: Drinking from contaminated water)</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
