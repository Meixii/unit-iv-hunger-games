import { Separator } from "@/components/ui/separator";

export default function LimitationsPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Project Limitations</h2>
      </div>
      <Separator />
      
      <div className="space-y-8">
        <div className="space-y-4">
          <p className="text-lg text-muted-foreground">
            The project operates within specific constraints and limitations that define the scope and boundaries of the implementation. These limitations are designed to ensure feasibility within the academic context and classroom environment.
          </p>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Technical Limitations</h3>
            <div className="space-y-4">
              <div className="border rounded-lg p-6">
                <h4 className="text-xl font-semibold text-orange-600 mb-3">MLP Architecture Constraints</h4>
                <p className="text-muted-foreground mb-4">
                  The neural network complexity will be limited to 2-3 hidden layers to maintain computational feasibility during 10-20 minute classroom sessions while demonstrating multi-layer learning capabilities.
                </p>
                <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded">
                  <h5 className="font-semibold mb-2">Impact:</h5>
                  <ul className="text-sm space-y-1">
                    <li>• Simplified neural network architecture</li>
                    <li>• Limited complexity in decision-making processes</li>
                    <li>• Focus on core learning principles rather than advanced AI</li>
                    <li>• Faster training and execution times</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <h4 className="text-xl font-semibold text-orange-600 mb-3">Session Duration Limitations</h4>
                <p className="text-muted-foreground mb-4">
                  Game sessions will be constrained to 10-20 minutes to fit classroom schedules, limiting the number of evolutionary generations and behavioral complexity that can be demonstrated.
                </p>
                <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded">
                  <h5 className="font-semibold mb-2">Impact:</h5>
                  <ul className="text-sm space-y-1">
                    <li>• Limited number of evolutionary generations</li>
                    <li>• Reduced behavioral complexity demonstration</li>
                    <li>• Focus on immediate survival strategies</li>
                    <li>• Quick demonstration of core concepts</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <h4 className="text-xl font-semibold text-orange-600 mb-3">Simplified Environmental Model</h4>
                <p className="text-muted-foreground mb-4">
                  The battle royale environment will use a 2D grid-based representation with text-based gameplay and static chibi images rather than complex 3D graphics or real-time animations.
                </p>
                <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded">
                  <h5 className="font-semibold mb-2">Impact:</h5>
                  <ul className="text-sm space-y-1">
                    <li>• 2D grid-based world representation</li>
                    <li>• Text-based gameplay interface</li>
                    <li>• Static visual elements (chibi images)</li>
                    <li>• No complex 3D graphics or animations</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Design Limitations</h3>
            <div className="space-y-4">
              <div className="border rounded-lg p-6">
                <h4 className="text-xl font-semibold text-orange-600 mb-3">Population Balance Constraints</h4>
                <p className="text-muted-foreground mb-4">
                  Animal populations will be artificially balanced (ratios dependent on class size) rather than naturally emerging ecosystem dynamics to ensure fair gameplay within time limits.
                </p>
                <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded">
                  <h5 className="font-semibold mb-2">Impact:</h5>
                  <ul className="text-sm space-y-1">
                    <li>• Artificial population ratios (e.g., 20:5:5)</li>
                    <li>• No natural ecosystem dynamics</li>
                    <li>• Fair gameplay within time constraints</li>
                    <li>• Predictable population distribution</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <h4 className="text-xl font-semibold text-orange-600 mb-3">Behavioral Complexity Boundaries</h4>
                <p className="text-muted-foreground mb-4">
                  Animal behaviors, while driven by a neural network, will be primarily reactive to immediate Status needs (e.g., low hunger triggers food-seeking) and sensory information within a limited range, rather than complex, long-term strategic planning.
                </p>
                <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded">
                  <h5 className="font-semibold mb-2">Impact:</h5>
                  <ul className="text-sm space-y-1">
                    <li>• Reactive rather than strategic behavior</li>
                    <li>• Immediate status-based decision making</li>
                    <li>• Limited sensory range</li>
                    <li>• No long-term planning capabilities</li>
                  </ul>
                </div>
              </div>

              <div className="border rounded-lg p-6">
                <h4 className="text-xl font-semibold text-orange-600 mb-3">Player Interaction</h4>
                <p className="text-muted-foreground mb-4">
                  Direct player control is intentionally limited to the initial &apos;Training&apos; phase and timed &apos;Quick Events.&apos; The core gameplay loop, including movement and resource gathering, is fully autonomous and governed by the animal&apos;s evolved MLP, reinforcing the project&apos;s focus on evolutionary algorithms.
                </p>
                <div className="bg-orange-50 dark:bg-orange-950 p-4 rounded">
                  <h5 className="font-semibold mb-2">Impact:</h5>
                  <ul className="text-sm space-y-1">
                    <li>• Limited player control during gameplay</li>
                    <li>• Focus on autonomous AI behavior</li>
                    <li>• Emphasis on evolutionary algorithm learning</li>
                    <li>• Reduced human intervention in core mechanics</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Academic Context Limitations</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Classroom Environment</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• 10-20 minute session duration</li>
                  <li>• Limited computational resources</li>
                  <li>• Educational demonstration focus</li>
                  <li>• Multiple student participation</li>
                </ul>
              </div>
              
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-2">Research Scope</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Undergraduate level complexity</li>
                  <li>• Proof-of-concept implementation</li>
                  <li>• Educational value over commercial viability</li>
                  <li>• Limited external dependencies</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-2xl font-semibold">Mitigation Strategies</h3>
            <div className="bg-muted p-6 rounded-lg">
              <p className="text-muted-foreground mb-4">
                Despite these limitations, the project is designed to effectively demonstrate core concepts while working within the defined constraints:
              </p>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold mb-2">Technical Mitigations</h4>
                  <ul className="text-sm space-y-1">
                    <li>• Optimized algorithms for quick execution</li>
                    <li>• Efficient data structures</li>
                    <li>• Streamlined user interface</li>
                    <li>• Pre-computed scenarios for demonstrations</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Educational Mitigations</h4>
                  <ul className="text-sm space-y-1">
                    <li>• Clear visual feedback systems</li>
                    <li>• Step-by-step process explanations</li>
                    <li>• Real-time progress indicators</li>
                    <li>• Comprehensive documentation</li>
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
