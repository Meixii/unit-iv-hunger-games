# Design System & Direction: EvoSim Documentation

Reading this as: Technical documentation and research monograph for AI researchers, computer science faculty, and students, in a Cybernetic & Evolutionary Life style, dial ENERGY 2 / RHYTHM 2 / MOTION 1.

## 1. Visual Identity & Atmosphere

- **Theme Concept**: Cybernetic Biology & Neural Evolution.
- **Tone**: Rigorous, scientific, modern, and engaging without decorative clutter.
- **Atmosphere**: Deep obsidian substrate, bio-luminescent emerald signals (life/fitness/mutation), electric cyan (neural weights/MLP nodes), and amber warning tones (environmental disasters/hazards).

## 2. Color Palette & Token System

### Dark Canvas (Primary Default)
- `--bg-canvas`: `#080c10` (deep obsidian substrate)
- `--bg-surface`: `#0f1722` (panel and card background)
- `--bg-surface-raised`: `#162232` (elevated items, hover states, active pill buttons)
- `--border-subtle`: `#1f2d42` (crisp structural rules and dividers)
- `--border-highlight`: `#2d4260` (focused inputs and active sidebar links)
- `--text-primary`: `#f1f5f9` (high legibility, 13.8:1 contrast against canvas)
- `--text-secondary`: `#94a3b8` (metadata, descriptions, 5.2:1 contrast against canvas)
- `--text-muted`: `#64748b` (labels, legends, 4.6:1 contrast against canvas)

### Bio-Signals & Accents
- `--accent-bio`: `#10b981` (emerald green: survival, fitness reward, elite traits)
- `--accent-bio-subtle`: `rgba(16, 185, 129, 0.12)`
- `--accent-neural`: `#06b6d4` (cyan: MLP layers, sensory nodes, neural weights)
- `--accent-neural-subtle`: `rgba(6, 182, 212, 0.12)`
- `--accent-hazard`: `#f59e0b` (amber: disasters, status depletion, environmental threats)
- `--accent-perish`: `#f43f5e` (rose red: health depletion, carnivore lethal strikes)

### Light Canvas (Full Contrast Support, WCAG AA Compliant)
- `--bg-canvas`: `#f8fafc` (crisp laboratory paper)
- `--bg-surface`: `#ffffff` (elevated white cards)
- `--bg-surface-raised`: `#f1f5f9` (hover and active items)
- `--border-subtle`: `#cbd5e1` (dividers and frames)
- `--border-highlight`: `#94a3b8` (focused frames)
- `--text-primary`: `#0f172a` (high contrast, 15.2:1 ratio)
- `--text-secondary`: `#475569` (body text, 6.4:1 ratio)
- `--text-muted`: `#64748b` (captions, 4.8:1 ratio)
- `--accent-bio`: `#059669` (darker emerald for light canvas, 4.7:1 contrast)
- `--accent-neural`: `#0891b2` (darker cyan for light canvas, 4.6:1 contrast)

## 3. Typography

- **System Sans**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
  - High legibility, neutral, fast loading, zero external font bloat.
- **Monospace**: `ui-monospace, "SF Mono", "Fira Code", "Cascadia Code", Menlo, monospace`
  - For math formulas, MLP input/hidden nodes, weights, code samples, and data structures.
- **Hierarchy**:
  - `h1`: 2.25rem (36px), font-weight 700, letter-spacing -0.025em
  - `h2`: 1.5rem (24px), font-weight 600, letter-spacing -0.02em, crisp bottom subtle border
  - `h3`: 1.25rem (20px), font-weight 600
  - Body: 1rem (16px), line-height 1.65, max line width 75ch for optimal reading comfort.

## 4. Dials & Liveliness Levers

- **ENERGY 2**: High visual clarity. Visual punch is focused on real data: the neural network architecture topology, mathematical formula boxes, interactive fitness calculation slider, and live terminology filtering.
- **RHYTHM 2**: Predictable documentation layout (header, left sidebar navigation, main content stream, right table-of-contents) broken rhythmically by structured comparison cards, formulas, and diagrams.
- **MOTION 1**: Restrained, functional motion only. Crossfade theme toggle, active link indicators, smooth scrolling on anchor jumps, modal open/close transitions. All motion strictly honors `prefers-reduced-motion`.

## 5. Anti-Slop Discipline

- **No em dashes** (Unicode U+2014) in copy, labels, or navigation. Use commas, colons, or parentheses.
- **No generic AI buzzwords** ("cutting-edge", "revolutionary", "seamless").
- **Real academic and technical content** from the EvoSim research paper presented with full fidelity.
- **No dead controls**: Search input filters live results; Table of Contents updates dynamically; Theme toggle persists across visits; Copy code buttons notify on success.
- **Mobile First**: Clean off-canvas drawer navigation for mobile, zero horizontal overflow, and minimum 44px tap targets.
