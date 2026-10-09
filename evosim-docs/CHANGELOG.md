# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-09

### Added

- **Astro 5 Architecture.** Completely migrated documentation from Next.js 15 to an ultra-fast, zero-runtime-JS Astro 5 static site generator.
- **Self-Hosted Express CMS (`cms/`).** Added lightweight schema-driven admin CMS editing `content/*.json` directly:
  - Vanilla JS responsive admin interface accessible at `/admin`.
  - Live site rebuild triggering with real-time log polling (`POST /api/rebuild`).
  - Image upload engine (`public/uploads`) supporting PNG, WebP, SVG, AVIF.
  - Automatic Git commits on content saves.
- **Content Collections Data Model (`content/*.json`).** Structured all documentation pages into granular JSON models:
  - `site.json`: Metadata, research paper authors from UCC, navigation groups, and links.
  - `objectives.json`: General and specific technical objectives.
  - `scope.json` & `limitations.json`: Project boundaries and constraints.
  - `terminologies.json`: 17+ defined terms categorized by domain.
  - `mlp-evolution.json`: 41-16-12-8 neural topology and genetic algorithm steps.
  - `fitness-function.json`: Mathematical equations and weight parameters.
  - `core-mechanics.json`: Herbivore, Carnivore, and Omnivore archetypes, passives, and turn cycles.
  - `parameters.json`: Simulation rates, world generation ratios, and combat thresholds.
  - `map-objectives.json`: 25x25 grid specifications, biomes, and neighbor-aware spawning rules.
  - `events-disasters.json`: Weekly scheduled disasters, random events, and stochastic checks.
  - `quantitative-mechanics.json`: Combat, movement energy, and damage calculations.
  - `code-implementation.json`: Python constants configuration and module architecture.
  - `formulas.json`: Compendium of all algebraic models and checks.
  - `data-structure.json`: Entity schemas and class relationship models.
  - `tasks.json` & `phases.json`: Implementation milestones and development deliverables.
  - `dashboard.json`: Telemetry statistics and generational benchmarks.
- **Cybernetic & Evolutionary Life Design System.** Established comprehensive design tokens adhering to strict Anti-Slop guidelines:
  - Obsidian substrate canvas with bio-luminescent emerald and electric cyan accents.
  - Full WCAG AA contrast compliance in both Dark and Light themes.
  - System font stack prioritizing instant loading and reading legibility.
- **Interactive Documentation Components.**
  - `NeuralNetVisualizer.astro`: Visual topology diagram illustrating 41 Input nodes, dual ReLU hidden layers, and 8 discrete motor actions.
  - `FitnessCalculator.astro`: Live interactive client-side sandbox calculating real-time fitness scores based on slider adjustments.
  - `TableOfContents.astro`: Dynamic scroll-spy navigation tracking section headers.
  - `SearchModal.astro`: Instant client-side search dialog indexed across all pages and terminologies (triggered with `Ctrl+K`).
  - `CodeBlock.astro`: Syntax-styled code containers with copy-to-clipboard functionality.
  - `ThemeToggle.astro`: Accessible, keyboard-navigable dark and light theme switcher with no-flash initialization.
- **Home Server Docker Deployment.**
  - `Dockerfile` using Node 22 Alpine, integrating Git for CMS auto-commits.
  - `docker-compose.yml` publishing to port 8092 (`8092:4000`).
  - `scripts/sync-server.sh`: Tailscale-enabled synchronization and deployment automation.
- **Quality & Testing Suite.**
  - `scripts/lint.js`: Enforces zero em dashes and checks link integrity.
  - `scripts/test.js`: Validates all JSON files, mathematical formulas, and Astro routes.

[unreleased]: https://github.com/Meixii/unit-iv-hunger-games/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Meixii/unit-iv-hunger-games/releases/tag/v0.1.0
