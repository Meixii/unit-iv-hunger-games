
export default function TerminologiesPage() {
  const terminologies = [
    {
      term: "Crossover",
      definition: "A process in the Evolutionary Algorithm where the MLP weights of two parent animals are combined to create the MLP for a new offspring."
    },
    {
      term: "Disaster",
      definition: "A large-scale, negative event that affects a large area of the map or the entire simulation for a period of time (e.g., Wildfire, Harsh Winter)."
    },
    {
      term: "Effect (Buff/Debuff)",
      definition: "A temporary modifier applied to an animal that alters its Traits or Status for a limited duration (e.g., 'Poisoned', 'Well-Fed')."
    },
    {
      term: "Elitism",
      definition: "A selection strategy in the Evolutionary Algorithm where a small percentage of the most successful animals (the \"elites\") from one generation are carried over to the next generation unchanged."
    },
    {
      term: "Evolutionary Algorithm (EA)",
      definition: "The training method used to optimize the MLP. It mimics natural selection by creating a population of animals, evaluating their performance via a Fitness Function, and \"breeding\" the most successful ones to create the next generation."
    },
    {
      term: "Fitness Function",
      definition: "The specific formula used to calculate an animal's success score at the end of a simulation round. This score determines its likelihood of passing its traits to the next generation."
    },
    {
      term: "Generation",
      definition: "A complete cycle of the simulation. A population of animals lives, dies, and the most successful ones are used to create a new, potentially improved population for the next generation."
    },
    {
      term: "Movement Event",
      definition: "The core, AI-driven phase of the simulation where each animal's MLP makes a decision and performs an action, such as moving, eating, or resting."
    },
    {
      term: "Multi-Layer Perceptron (MLP)",
      definition: "A type of artificial neural network that acts as the \"brain\" for each animal, making decisions based on inputs (like Hunger, Thirst, nearby threats) to produce outputs (like moving, eating, fighting)."
    },
    {
      term: "Mutation",
      definition: "A process in the Evolutionary Algorithm where small, random changes are applied to an offspring's MLP weights to introduce new genetic diversity into the population."
    },
    {
      term: "Neuroevolution",
      definition: "The process of using an evolutionary algorithm to train a neural network, which is the core concept of this project."
    },
    {
      term: "Passive",
      definition: "An innate, category-specific ability that is always active for an animal (e.g., a Carnivore's Ambush Predator ability)."
    },
    {
      term: "Random Event",
      definition: "A simulation-wide event that affects all animals and the environment for one week (e.g., Drought, Resource Bloom)."
    },
    {
      term: "Selection",
      definition: "The process within the Evolutionary Algorithm of choosing which animals from a generation will become parents for the next, based on their fitness scores."
    },
    {
      term: "Status",
      definition: "A dynamic, moment-to-moment variable reflecting an animal's well-being (e.g., Health, Hunger, Energy). These are the primary inputs for the MLP."
    },
    {
      term: "Trait",
      definition: "A core, semi-permanent genetic attribute of an animal (e.g., Strength, Agility). These are the values the EA will tune over generations."
    },
    {
      term: "Triggered Event",
      definition: "An automated, situational scenario that occurs when specific conditions are met, presenting a unique challenge or opportunity for an animal's MLP to solve (e.g., Animal Encounter, Sudden Threat)."
    }
  ];

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Terminologies</h1>
        <p className="text-lg text-muted-foreground">
          A dictionary of key concepts used throughout the project.
        </p>
      </div>

      <div className="space-y-4">
        {terminologies.map((item, index) => (
          <div key={index} className="border rounded-lg p-4 space-y-2">
            <h3 className="text-lg font-semibold text-primary">{item.term}</h3>
            <p className="text-sm text-muted-foreground">{item.definition}</p>
          </div>
        ))}
      </div>
    </div>
  );
}