# EvoSim Documentation Website

A modern, interactive documentation website for the EvoSim project - "Evolve or Perish: An Animal Survival Simulation Using an Evolutionary Algorithm to Train a Multi-Layer Perceptron".

## Features

- **Modern UI**: Built with Next.js 15, TypeScript, and Tailwind CSS
- **shadcn/ui Style**: Professional documentation layout inspired by shadcn/ui docs
- **Responsive Design**: Mobile-first approach with sidebar navigation
- **Dark Mode**: Default dark theme with proper contrast and readability
- **Interactive Components**: Syntax highlighting, collapsible sections, and smooth navigation
- **Comprehensive Content**: Complete documentation covering all aspects of the simulation
- **Academic Focus**: Research paper structure with objectives, scope, and limitations

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd evosim-docs
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Home page (Introduction)
│   ├── layout.tsx         # Root layout with sidebar & max-width container
│   ├── objectives/        # Project objectives page
│   ├── scope/             # Project scope page
│   ├── limitations/       # Project limitations page
│   ├── terminologies/     # Terminologies page
│   ├── mlp-evolution/     # MLP & EA design page
│   ├── fitness-function/  # Fitness function page
│   ├── core-mechanics/    # Core mechanics page
│   ├── parameters/        # Parameters & variables page
│   ├── map-objectives/    # Map & objectives page
│   ├── events-disasters/  # Events & disasters page
│   ├── quantitative-mechanics/ # Quantitative mechanics page
│   ├── code-implementation/ # Code constants page
│   ├── formulas/          # Formulas & computations page
│   ├── data-structure/    # Data structure page
│   ├── development-tasks/ # Development task list page
│   └── phases/            # Implementation phases page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   └── app-sidebar.tsx   # Main sidebar component
└── lib/                  # Utility functions
```

## Documentation Sections

### Overview
- **Introduction**: Project overview and research paper information
- **Project Objectives**: General and specific objectives
- **Project Scope**: Six core technical components
- **Project Limitations**: Technical and design constraints

### Core Concepts
- **Terminologies**: Dictionary of key concepts and definitions
- **MLP & Evolutionary Algorithm**: Technical architecture details
- **Fitness Function**: Scoring system and generational goals

### Game Mechanics
- **Core Mechanics**: Simulation flow and action resolution
- **Parameters & Variables**: Animal traits, status, and effects
- **Map & Objectives**: World design and win conditions
- **Events & Disasters**: Environmental challenges and random events

### Technical Details
- **Quantitative Mechanics**: Numerical values and balancing
- **Code Implementation**: Python constants and configuration
- **Formulas & Computations**: Mathematical calculations and formulas
- **Data Structure**: Class blueprints and relationships

### Development
- **Task List**: Detailed implementation phases and milestones
- **Implementation Phases**: High-level development roadmap

## Technologies Used

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Modern component library with professional styling
- **Lucide React**: Icon library
- **react-syntax-highlighter**: Code syntax highlighting
- **Dracula Theme**: Code highlighting theme

## Design Features

- **shadcn/ui Inspired Layout**: Professional documentation style with proper spacing
- **Max-width Container**: Content constrained to `max-w-4xl` for optimal readability
- **Dark Mode Default**: Professional dark theme with proper contrast
- **Responsive Typography**: Consistent heading hierarchy and text sizing
- **Clean Navigation**: Organized sidebar with clear section hierarchy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Academic Context

This project is part of the CS4B Unit 4: Evolutionary Algorithms course at The College of Liberal Arts and Sciences, Congress Campus, Caloocan City. It serves as a research paper and practical demonstration of evolutionary algorithms applied to neural network training.

### Research Team
- Ma. Catherine H. Bae
- Emannuel Pabua
- Irheil Mae S. Antang
- Jhon Keneth Ryan B. Namias
- Jin Harold A. Failana
- Kevin A. Llanes
- Ronan Renz T. Valencia

## License

This project is part of the CS4B Unit 4: Evolutionary Algorithms course.

## Contact

For questions about the EvoSim project or this documentation, please refer to the course materials or contact the development team.