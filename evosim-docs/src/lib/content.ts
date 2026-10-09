import site from "../../content/site.json";
import objectives from "../../content/objectives.json";
import scope from "../../content/scope.json";
import limitations from "../../content/limitations.json";
import terminologies from "../../content/terminologies.json";
import mlpEvolution from "../../content/mlp-evolution.json";
import fitnessFunction from "../../content/fitness-function.json";
import coreMechanics from "../../content/core-mechanics.json";
import parameters from "../../content/parameters.json";
import mapObjectives from "../../content/map-objectives.json";
import eventsDisasters from "../../content/events-disasters.json";
import quantitativeMechanics from "../../content/quantitative-mechanics.json";
import codeImplementation from "../../content/code-implementation.json";
import formulas from "../../content/formulas.json";
import dataStructure from "../../content/data-structure.json";
import tasks from "../../content/tasks.json";
import phases from "../../content/phases.json";
import dashboard from "../../content/dashboard.json";
import pkg from "../../package.json";

export const version = pkg.version;

export const siteData = site;
export const objectivesData = objectives;
export const scopeData = scope;
export const limitationsData = limitations;
export const terminologiesData = terminologies;
export const mlpEvolutionData = mlpEvolution;
export const fitnessFunctionData = fitnessFunction;
export const coreMechanicsData = coreMechanics;
export const parametersData = parameters;
export const mapObjectivesData = mapObjectives;
export const eventsDisastersData = eventsDisasters;
export const quantitativeMechanicsData = quantitativeMechanics;
export const codeImplementationData = codeImplementation;
export const formulasData = formulas;
export const dataStructureData = dataStructure;
export const tasksData = tasks;
export const phasesData = phases;
export const dashboardData = dashboard;

export interface NavItem {
  title: string;
  href: string;
  description?: string;
  category: string;
}

export const allDocPages: NavItem[] = [
  { title: "Introduction", href: "/", category: "Overview", description: "Project overview, research monograph, and authors" },
  { title: "Project Objectives", href: "/objectives", category: "Overview", description: "General and specific research goals" },
  { title: "Project Scope", href: "/scope", category: "Overview", description: "Core boundaries and simulation components" },
  { title: "Project Limitations", href: "/limitations", category: "Overview", description: "Technical constraints and deliberate design boundaries" },
  { title: "Terminologies", href: "/terminologies", category: "Core Concepts", description: "Comprehensive dictionary of simulation terms" },
  { title: "MLP & Evolutionary Algorithm", href: "/mlp-evolution", category: "Core Concepts", description: "Neural topology, sensory inputs, and genetic algorithm cycle" },
  { title: "Fitness Function", href: "/fitness-function", category: "Core Concepts", description: "Quantitative fitness formulas and generational milestones" },
  { title: "Core Mechanics", href: "/core-mechanics", category: "Game Mechanics", description: "Animal classifications, passives, and turn cycles" },
  { title: "Parameters & Variables", href: "/parameters", category: "Game Mechanics", description: "Environmental and animal status thresholds" },
  { title: "Map & Objectives", href: "/map-objectives", category: "Game Mechanics", description: "Grid map architecture, biomes, and spawn algorithms" },
  { title: "Events & Disasters", href: "/events-disasters", category: "Game Mechanics", description: "Random events, weekly disasters, and triggered encounters" },
  { title: "Quantitative Mechanics", href: "/quantitative-mechanics", category: "Technical Details", description: "Action computations, damage formulas, and movement energy" },
  { title: "Code Implementation", href: "/code-implementation", category: "Technical Details", description: "Python configuration constants and module architecture" },
  { title: "Formulas & Computations", href: "/formulas", category: "Technical Details", description: "Unified catalog of mathematical models and equations" },
  { title: "Data Structure", href: "/data-structure", category: "Technical Details", description: "Data models, entity schemas, and class relationships" },
  { title: "Development Task List", href: "/development-tasks", category: "Development", description: "Structured development task breakdown and tracking" },
  { title: "Implementation Phases", href: "/phases", category: "Development", description: "Five-phase development roadmap and milestones" },
  { title: "Simulation Dashboard", href: "/dashboard", category: "Development", description: "Real-time generational analytics and simulation status" }
];

export function getPageNavigation(currentPath: string) {
  // Normalize trailing slashes
  const normalized = currentPath === "" ? "/" : currentPath.replace(/\/$/, "") || "/";
  const index = allDocPages.findIndex(p => p.href === normalized);

  if (index === -1) {
    return { previous: undefined, next: undefined };
  }

  const previous = index > 0 ? allDocPages[index - 1] : undefined;
  const next = index < allDocPages.length - 1 ? allDocPages[index + 1] : undefined;

  return { previous, next };
}

export function pageTitle(title?: string): string {
  if (!title || title === "Introduction") {
    return `${site.identity.shortName} | ${site.identity.projectTitle}`;
  }
  const template = site.seo?.titleTemplate || "%s";
  return template.replace("%s", title);
}

export interface SearchEntry {
  title: string;
  category: string;
  url: string;
  snippet: string;
}

export function buildSearchIndex(): SearchEntry[] {
  const index: SearchEntry[] = [];

  // Add pages
  for (const page of allDocPages) {
    index.push({
      title: page.title,
      category: page.category,
      url: page.href,
      snippet: page.description || ""
    });
  }

  // Add terminologies
  for (const t of terminologies.terms) {
    index.push({
      title: t.term,
      category: `Term: ${t.category}`,
      url: `/terminologies#term-${t.term.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`,
      snippet: t.definition
    });
  }

  // Add parameters
  for (const sec of parameters.sections) {
    for (const p of sec.parameters) {
      index.push({
        title: p.name,
        category: `Parameter: ${sec.category}`,
        url: `/parameters#param-${p.name.toLowerCase()}`,
        snippet: `${p.value} ${p.unit} | ${p.description}`
      });
    }
  }

  return index;
}
