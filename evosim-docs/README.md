# EvoSim Documentation Website

A modern, interactive documentation website for the EvoSim project - "Evolve or Perish: AI-Driven Animal Survival in a Neural Network Battle Royale".

## Features

- **Modern UI**: Built with Next.js 15, TypeScript, and Tailwind CSS
- **Responsive Design**: Mobile-first approach with sidebar navigation
- **Interactive Components**: Syntax highlighting, collapsible sections, and smooth navigation
- **Comprehensive Content**: Complete documentation covering all aspects of the simulation
- **Search & Navigation**: Easy-to-use sidebar with organized sections

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
│   ├── page.tsx           # Home page
│   ├── layout.tsx         # Root layout with sidebar
│   ├── terminologies/     # Terminologies page
│   ├── mlp-evolution/     # MLP & EA design page
│   ├── fitness-function/  # Fitness function page
│   ├── core-mechanics/    # Core mechanics page
│   └── code-implementation/ # Code constants page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   └── app-sidebar.tsx   # Main sidebar component
└── lib/                  # Utility functions
```

## Documentation Sections

### Overview
- Introduction to the EvoSim project
- Two game modes explanation
- Key features and objectives

### Core Concepts
- **Terminologies**: Dictionary of key concepts
- **MLP & Evolutionary Algorithm**: Technical architecture details
- **Fitness Function**: Scoring system and generational goals

### Game Mechanics
- **Core Mechanics**: Simulation flow and action resolution
- **Parameters & Variables**: Animal traits and status systems
- **Map & Objectives**: World design and win conditions
- **Events & Disasters**: Environmental challenges

### Technical Details
- **Quantitative Mechanics**: Numerical values and balancing
- **Code Implementation**: Python constants and configuration
- **Formulas & Computations**: Mathematical calculations
- **Data Structure**: Class blueprints and relationships

### Development
- **Task List**: Implementation phases and milestones
- **Implementation Phases**: Detailed development roadmap

## Technologies Used

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Modern component library
- **Lucide React**: Icon library

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the CS4B Unit 4: Evolutionary Algorithms course.

## Contact

For questions about the EvoSim project or this documentation, please refer to the course materials or contact the development team.