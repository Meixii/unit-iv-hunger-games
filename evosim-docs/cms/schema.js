/**
 * Schema definitions for EvoSim Documentation CMS.
 * Dictates fields rendered in the /admin UI and validated upon save.
 */

export const schema = {
  site: {
    label: "Site Settings & Metadata",
    description: "Monograph title, institution, authors list, version, and navigation metadata.",
    file: "site.json",
    fields: [
      { name: "identity.name", label: "Documentation Title", type: "text" },
      { name: "identity.shortName", label: "Short Name (Sidebar)", type: "text" },
      { name: "identity.projectTitle", label: "Full Project Subtitle", type: "text" },
      { name: "identity.version", label: "System Version", type: "text" },
      { name: "identity.date", label: "Publication Date", type: "text" },
      { name: "identity.institution", label: "Academic Institution", type: "text" },
      { name: "identity.campus", label: "Campus Location", type: "text" },
      { name: "identity.department", label: "Faculty / College", type: "text" },
      { name: "identity.degree", label: "Degree Program", type: "text" },
      { name: "seo.canonicalUrl", label: "Canonical URL", type: "url" },
      { name: "seo.description", label: "SEO Meta Description", type: "textarea" },
      {
        name: "authors",
        label: "Research Authors",
        type: "list",
        itemType: "object",
        itemLabel: "{name}",
        newItem: { name: "", role: "Author" },
        itemFields: [
          { name: "name", label: "Author Full Name", type: "text" },
          { name: "role", label: "Role / Contribution", type: "text" }
        ]
      },
      { name: "links.github", label: "GitHub Repository Link", type: "url" },
      { name: "links.docLink", label: "External Research Document Link", type: "url" },
      { name: "footer.notice", label: "Footer Copyright / Notice", type: "text" }
    ]
  },

  objectives: {
    label: "Project Objectives",
    description: "General research objective and specific technical goals.",
    file: "objectives.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      { name: "general.title", label: "General Objective Title", type: "text" },
      { name: "general.description", label: "General Objective Statement", type: "textarea" },
      {
        name: "specific",
        label: "Specific Objectives",
        type: "list",
        itemType: "object",
        itemLabel: "{title}",
        newItem: { id: "obj-new", title: "", detail: "" },
        itemFields: [
          { name: "id", label: "Unique ID", type: "text" },
          { name: "title", label: "Goal Title", type: "text" },
          { name: "detail", label: "Detailed Specification", type: "textarea" }
        ]
      }
    ]
  },

  scope: {
    label: "Project Scope",
    description: "System boundaries and supported components.",
    file: "scope.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      {
        name: "items",
        label: "Scope Boundaries",
        type: "list",
        itemType: "object",
        itemLabel: "{title}",
        newItem: { title: "", summary: "" },
        itemFields: [
          { name: "title", label: "Component Name", type: "text" },
          { name: "summary", label: "Scope Description", type: "textarea" }
        ]
      }
    ]
  },

  limitations: {
    label: "Project Limitations",
    description: "Deliberate design constraints and out-of-scope boundaries.",
    file: "limitations.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      {
        name: "items",
        label: "Technical Constraints",
        type: "list",
        itemType: "object",
        itemLabel: "{title}",
        newItem: { title: "", category: "Architecture", detail: "" },
        itemFields: [
          { name: "title", label: "Constraint Name", type: "text" },
          { name: "category", label: "Domain Category", type: "text" },
          { name: "detail", label: "Constraint Analysis", type: "textarea" }
        ]
      }
    ]
  },

  terminologies: {
    label: "Terminologies Dictionary",
    description: "Alphabetical terminology definitions and concepts.",
    file: "terminologies.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      {
        name: "terms",
        label: "Defined Terms",
        type: "list",
        itemType: "object",
        itemLabel: "{term} ({category})",
        newItem: { term: "", category: "General", definition: "" },
        itemFields: [
          { name: "term", label: "Term", type: "text" },
          { name: "category", label: "Subsystem Category", type: "text" },
          { name: "definition", label: "Rigorous Definition", type: "textarea" }
        ]
      }
    ]
  },

  mlpEvolution: {
    label: "MLP & Evolutionary Algorithm",
    description: "Neural network topology, sensory grid, and genetic algorithm pipeline.",
    file: "mlp-evolution.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      { name: "mlp.summary", label: "MLP Architecture Summary", type: "textarea" },
      { name: "evolution.summary", label: "Evolution Pipeline Summary", type: "textarea" },
      {
        name: "evolution.steps",
        label: "Genetic Algorithm Steps",
        type: "list",
        itemType: "object",
        itemLabel: "Step {step}: {name}",
        newItem: { step: 1, name: "", detail: "" },
        itemFields: [
          { name: "step", label: "Sequence Number", type: "number" },
          { name: "name", label: "Phase Name", type: "text" },
          { name: "detail", label: "Algorithmic Detail", type: "textarea" }
        ]
      }
    ]
  },

  fitnessFunction: {
    label: "Fitness Function & Goals",
    description: "Multivariable fitness equations, weights, and generational targets.",
    file: "fitness-function.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      { name: "formula", label: "Fitness Equation", type: "text" },
      {
        name: "weights",
        label: "Weight Vector Constants",
        type: "list",
        itemType: "object",
        itemLabel: "{name}: {value}",
        newItem: { name: "", value: 1, description: "" },
        itemFields: [
          { name: "name", label: "Weight Name", type: "text" },
          { name: "value", label: "Numerical Value", type: "number" },
          { name: "description", label: "Rationale", type: "textarea" }
        ]
      }
    ]
  },

  coreMechanics: {
    label: "Core Mechanics & Animals",
    description: "Species classifications, passives, traits, and turn cycle.",
    file: "core-mechanics.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      {
        name: "categories",
        label: "Animal Archetypes",
        type: "list",
        itemType: "object",
        itemLabel: "{name}",
        newItem: { name: "", diet: "", primaryTrait: "", passive: "", description: "" },
        itemFields: [
          { name: "name", label: "Species Archetype", type: "text" },
          { name: "diet", label: "Dietary Rule", type: "text" },
          { name: "primaryTrait", label: "Primary Trait", type: "text" },
          { name: "passive", label: "Passive Ability", type: "textarea" },
          { name: "description", label: "Ecological Role", type: "textarea" }
        ]
      }
    ]
  },

  parameters: {
    label: "Simulation Parameters",
    description: "Numeric constants, rate thresholds, and world generation parameters.",
    file: "parameters.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" }
    ]
  },

  mapObjectives: {
    label: "Map & Objectives",
    description: "Grid dimensions, terrain biomes, and neighbor-aware spawning.",
    file: "map-objectives.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" }
    ]
  },

  eventsDisasters: {
    label: "Events & Disasters",
    description: "Weekly natural disasters, random occurrences, and triggered dice checks.",
    file: "events-disasters.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" }
    ]
  },

  codeImplementation: {
    label: "Code Implementation Constants",
    description: "Python constants config and module architecture.",
    file: "code-implementation.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      { name: "pythonConstants", label: "Python Constants (config.py)", type: "textarea" }
    ]
  },

  tasks: {
    label: "Development Task List",
    description: "Engineering tasks tracking status, priority, and phases.",
    file: "tasks.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      {
        name: "tasks",
        label: "Engineering Tasks",
        type: "list",
        itemType: "object",
        itemLabel: "[{status}] {id}: {title}",
        newItem: { id: "TASK-X", phase: "Phase 1", title: "", priority: "Medium", status: "planned", description: "" },
        itemFields: [
          { name: "id", label: "Task Identifier", type: "text" },
          { name: "phase", label: "Milestone Phase", type: "text" },
          { name: "title", label: "Task Title", type: "text" },
          {
            name: "status",
            label: "Completion Status",
            type: "select",
            options: [
              { value: "completed", label: "Completed" },
              { value: "in_progress", label: "In Progress" },
              { value: "planned", label: "Planned" }
            ]
          },
          {
            name: "priority",
            label: "Priority Level",
            type: "select",
            options: [
              { value: "High", label: "High" },
              { value: "Medium", label: "Medium" },
              { value: "Low", label: "Low" }
            ]
          },
          { name: "description", label: "Detailed Scope", type: "textarea" }
        ]
      }
    ]
  },

  phases: {
    label: "Implementation Phases",
    description: "Sequential development roadmap milestones.",
    file: "phases.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" }
    ]
  },

  dashboard: {
    label: "Simulation Dashboard Telemetry",
    description: "Top-level telemetry, species distributions, and benchmark milestones.",
    file: "dashboard.json",
    fields: [
      { name: "title", label: "Page Title", type: "text" },
      { name: "lede", label: "Page Lede", type: "textarea" },
      {
        name: "metrics",
        label: "Key Metrics",
        type: "list",
        itemType: "object",
        itemLabel: "{label}: {value}",
        newItem: { label: "", value: "", subtext: "" },
        itemFields: [
          { name: "label", label: "Metric Label", type: "text" },
          { name: "value", label: "Metric Value", type: "text" },
          { name: "subtext", label: "Additional Context", type: "text" }
        ]
      }
    ]
  }
};
