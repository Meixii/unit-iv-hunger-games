import { Separator } from "@/components/ui/separator";

export default function EventsDisastersPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Events and Disasters</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            This section covers the random environmental challenges that will test the animals&apos; adaptability, such as storms, meteors, and resource depletion.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Movement Event</h3>
            <p><strong>Frequency:</strong> 2 per week</p>
            <p>This is the core AI-driven action phase.</p>
            <ul className="space-y-2 ml-4">
              <li><strong>Mechanic:</strong> The MLP for each animal makes a decision based on its current Status and environmental inputs.</li>
              <li><strong>Potential Actions:</strong> Move towards detected food/water, hunt a nearby animal, flee from a threat, or do nothing to conserve energy.</li>
            </ul>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Triggered Events</h3>
            <p><strong>Frequency:</strong> 3 per week</p>
            <p>Automated, situational scenarios. A random event is chosen from the list below when triggered.</p>
            
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Animal Encounter</h4>
                <p className="text-sm text-muted-foreground">Two animals move onto the same tile. The MLP for each decides &quot;Fight&quot; or &quot;Flee&quot;.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Resource Scarcity</h4>
                <p className="text-sm text-muted-foreground">An animal arrives at a resource tile with one use left. The MLP decides whether to take the small reward or move on.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Sudden Threat (e.g., Rockslide)</h4>
                <p className="text-sm text-muted-foreground">A localized threat appears. The MLP decides to attempt an escape (Agility check) or hide (Endurance check).</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold">Curious Object</h4>
                <p className="text-sm text-muted-foreground">An unusual object is discovered. The MLP decides to investigate (Intelligence check for a buff) or ignore it.</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Random Events</h3>
            <p><strong>Frequency:</strong> 1 per week</p>
            <p>Simulation-wide occurrences. A random event is chosen from the list below at the start of the week.</p>
            
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-green-600">Migration</h4>
                <p className="text-sm text-muted-foreground">A random map quadrant becomes a &quot;Lush Zone&quot; for the week.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-blue-600">Resource Bloom</h4>
                <p className="text-sm text-muted-foreground">A specific resource type spawns at double the rate across the map.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-yellow-600">Drought</h4>
                <p className="text-sm text-muted-foreground">Half of all water source tiles become inactive for the week.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-purple-600">Predator&apos; Frenzy / Grazing Season</h4>
                <p className="text-sm text-muted-foreground">A global +1 STR buff for Carnivores or +1 AGI for Herbivores for one week.</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Disasters</h3>
            <p><strong>Frequency:</strong> 1 per week</p>
            <p>Large-scale, negative events. A random disaster is chosen from the list below.</p>
            
            <div className="grid gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-red-600">Wildfire</h4>
                <p className="text-sm text-muted-foreground">Affects all &apos;Forest&apos; terrain cells.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-orange-600">Contamination</h4>
                <p className="text-sm text-muted-foreground">A random water source becomes permanently contaminated.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-blue-600">Flood</h4>
                <p className="text-sm text-muted-foreground">Affects all tiles adjacent to water sources.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-gray-600">Earthquake</h4>
                <p className="text-sm text-muted-foreground">Changes some &apos;Plains&apos; tiles to &apos;Difficult Terrain&apos; and may cause the Injured debuff.</p>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-cyan-600">Harsh Winter</h4>
                <p className="text-sm text-muted-foreground">Lasts for a full week. Doubles Hunger/Thirst depletion and gives a -1 Agility penalty.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
