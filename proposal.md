
EVOLVE OR PERISH: An Animal Survival Simulation Using an Evolutionary Algorithm to Train a Multi-Layer Perceptron

A Research Paper 
Presented to the Faculty of
The College of Liberal Arts and Sciences 
Congress Campus, Caloocan City

In Partial Fulfillment
of the Requirements for the Degree 
BACHELOR OF SCIENCE IN COMPUTER SCIENCE 

By:
Ma. Catherine H. Bae
Emannuel Pabua
Irheil Mae S. Antang
Jhon Keneth Ryan B. Namias
Jin Harold A. Failana
Kevin A. Llanes
Ronan Renz T. Valencia


June 2026

Project Objectives
General:   To design and develop a competitive survival simulation where a Multi-Layer Perceptron, trained by an evolutionary algorithm, learns to effectively control an animal's behavior. The project aims to demonstrate how evolutionary processes can optimize a neural network's decision-making capabilities for survival within a dynamic, resource-limited, and hazardous environment.
        	Specific:
To classify animals into three categories (herbivore, carnivore, omnivore) with unique survival skills and behaviors
To create a training system that uses evolutionary algorithms where animals can improve their behaviors by facing different survival events and scenarios across generations.
To design and implement a multi-layered event system featuring: AI-driven Movement Events, player-interactive Quick Events, simulation-wide Random Events, and hazardous Disasters that occur on a structured weekly cycle.
To develop a competitive survival simulation where AI-driven animals, managed by a Multi-Layer Perceptron trained through evolutionary algorithms, experience survival across multiple generations within a dynamic environment.
To enable the MLP to make decisions for basic actions (moving, hunting, drinking, fleeing) based on the animal's core Status inputs (Health, Hunger, Thirst, Energy, Instinct).
To simulate users with different kinds of events, including hunting, migration, and resource collection.
To create an environment with diverse terrains, such as jungle, lake, and plains.
To create a system that displays animal skills based on specific statuses such as health, hunger, thirst, energy, and instinct.
Scope:
1.	Multi-Layer Perceptron Architecture: Implementation of neural networks with input layers (environmental sensors), multiple hidden layers (behavioral processing), and output layers (action selection) specifically designed for animal behavior control.
2. Evolutionary Training System: Development of genetic algorithms that adjust MLP weights and biases using competitive selection, optimization, and mutation strategies to progressively improve animal behaviors.
3.	Competitive Hunger Games Environment: Creation of a survival simulation featuring resource management, environmental hazards, and inter-animal competition where trained MLPs control animal decision-making.
4. Random Environmental Event System: Dynamic environmental challenges including meteors (area damage), storms (visibility reduction), resource depletion events, and terrain changes that test animal adaptability and survival instincts.
5. Grid Map Navigation: Dynamic grid-based map environment where animals navigate across cells, enabling structured movement, interaction, and spatial awareness within the simulation.
6. Grid-Based Random Spawning System: Implementation of a map divided into grids with a neighbor-aware spawning system, ensuring balanced and randomized placement of animals, resources, and hazards while maintaining strategic spatial interactions.
Limitations:
MLP Architecture Constraints: The neural network complexity will be limited to 2-3 hidden layers to maintain computational feasibility during 10-20 minute classroom sessions while demonstrating multi-layer learning capabilities.
Session Duration Limitations: Game sessions will be constrained to 10-20 minutes to fit classroom schedules, limiting the number of evolutionary generations and behavioral complexity that can be demonstrated.
Simplified Environmental Model: The battle royale environment will use a 2D grid-based representation with text-based gameplay and static chibi images rather than complex 3D graphics or real-time animations
Population Balance Constraints: Animal populations will be artificially balanced (ratios dependent on class size) rather than naturally emerging ecosystem dynamics to ensure fair gameplay within time limits.
Behavioral Complexity Boundaries: Animal behaviors, while driven by a neural network, will be primarily reactive to immediate Status needs (e.g., low hunger triggers food-seeking) and sensory information within a limited range, rather than complex, long-term strategic planning.
Player Interaction: Direct player control is intentionally limited to the initial 'Training' phase and timed 'Quick Events.' The core gameplay loop, including movement and resource gathering, is fully autonomous and governed by the animal's evolved MLP, reinforcing the project's focus on evolutionary algorithms.
