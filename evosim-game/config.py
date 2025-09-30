"""
EvoSim Game - Centralized Configuration

This module centralizes ALL configuration for EvoSim and provides:
- A single source of truth for simulation config (SimulationConfig)
- JSON load/save helpers
- Runtime application of constant overrides to the constants module
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Tuple

import constants as constants_module
from tkinter import Tk, ttk, filedialog, messagebox
import tkinter as tk


# =============================================================================
# SIMULATION CONFIG (moved from simulation_controller.py)
# =============================================================================

@dataclass
class SimulationConfig:
    """Configuration for simulation parameters."""
    max_weeks: int = 20
    max_generations: int = 10
    population_size: int = 5
    enable_logging: bool = True
    log_level: str = "INFO"
    random_seed: Optional[int] = None
    world_config: Optional[Any] = None  # GenerationConfig from world_generator

    def __post_init__(self) -> None:
        if self.max_weeks <= 0:
            raise ValueError(f"Max weeks must be positive, got {self.max_weeks}")
        if self.max_generations <= 0:
            raise ValueError(f"Max generations must be positive, got {self.max_generations}")
        if self.population_size <= 0:
            raise ValueError(f"Population size must be positive, got {self.population_size}")


# =============================================================================
# APP CONFIG WRAPPER
# =============================================================================

@dataclass
class AppConfig:
    """
    Container for all configurable settings.

    - simulation: Parameters for the simulation controller
    - constants_overrides: mapping of names in constants.py to new values
    """
    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    constants_overrides: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_defaults() -> "AppConfig":
        return AppConfig()

    @staticmethod
    def load(path: str) -> "AppConfig":
        data = ConfigManager.load_json(path)
        sim_data = data.get("simulation", {})
        constants_overrides = data.get("constants_overrides", {})
        simulation = SimulationConfig(**sim_data) if sim_data else SimulationConfig()
        return AppConfig(simulation=simulation, constants_overrides=constants_overrides)

    def save(self, path: str) -> None:
        data = {
            "simulation": asdict(self.simulation),
            "constants_overrides": self.constants_overrides,
        }
        ConfigManager.save_json(path, data)

    def apply_to_runtime(self) -> Dict[str, Any]:
        """
        Apply constants_overrides to the constants module at runtime.
        Returns a report with applied, skipped, and errors.
        """
        return ConfigManager.apply_constants(self.constants_overrides)


# =============================================================================
# CONFIG MANAGER
# =============================================================================

class ConfigManager:
    """Utility helpers for JSON config and runtime application of overrides."""

    @staticmethod
    def load_json(path: str) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_json(path: str, data: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def apply_constants(overrides: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to apply overrides to values in constants.py.

        Only existing uppercase attributes will be updated.
        """
        applied: Dict[str, Tuple[Any, Any]] = {}
        skipped: Dict[str, str] = {}
        errors: Dict[str, str] = {}

        for name, new_value in (overrides or {}).items():
            try:
                if not isinstance(name, str) or not name.isupper():
                    skipped[name] = "Only uppercase names in constants can be overridden"
                    continue
                if not hasattr(constants_module, name):
                    skipped[name] = "Name not found in constants"
                    continue
                old_value = getattr(constants_module, name)
                setattr(constants_module, name, new_value)
                applied[name] = (old_value, new_value)
            except Exception as exc:
                errors[name] = str(exc)

        return {
            "applied": applied,
            "skipped": skipped,
            "errors": errors,
        }


# =============================================================================
# CONVENIENCE API
# =============================================================================

def load_and_apply_config(path: str) -> AppConfig:
    """Load config file and apply constant overrides immediately."""
    cfg = AppConfig.load(path)
    cfg.apply_to_runtime()
    return cfg


__all__ = [
    "SimulationConfig",
    "AppConfig",
    "ConfigManager",
    "load_and_apply_config",
]


# =============================================================================
# TKINTER GUI
# =============================================================================

class ConfigGUI:
    """Tabbed GUI for configuring simulation and constants."""

    def __init__(self, initial_config_path: str = "config.json") -> None:
        self.root = Tk()
        self.root.title("EvoSim Configuration")
        self.root.geometry("700x800")

        self.config_path = initial_config_path
        self.app_config: AppConfig = AppConfig.from_defaults()

        self._field_vars: Dict[str, tk.Variable] = {}
        self._dict_texts: Dict[str, tk.Text] = {}

        self._build_ui()
        # Try to load initial config; ignore if missing
        try:
            self._load_from_path(self.config_path)
        except Exception:
            pass

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=8, pady=8)

        ttk.Button(toolbar, text="Load", command=self._on_load).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Save", command=self._on_save).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Apply to Runtime", command=self._on_apply).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Reset to Defaults", command=self._on_reset).pack(side=tk.LEFT, padx=4)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Tabs
        self._build_simulation_tab()
        self._build_constants_tabs()

    # ----------------------- Tabs -----------------------
    def _build_simulation_tab(self) -> None:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Simulation")

        grid = ttk.Frame(frame)
        grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def add_row(row: int, label: str, key: str, default: Any) -> None:
            ttk.Label(grid, text=label).grid(row=row, column=0, sticky=tk.W, padx=4, pady=4)
            var = tk.StringVar(value=str(default) if default is not None else "")
            entry = ttk.Entry(grid, textvariable=var)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=4, pady=4)
            grid.columnconfigure(1, weight=1)
            self._field_vars[f"simulation.{key}"] = var

        sim = self.app_config.simulation
        add_row(0, "Max Weeks", "max_weeks", sim.max_weeks)
        add_row(1, "Max Generations", "max_generations", sim.max_generations)
        add_row(2, "Population Size", "population_size", sim.population_size)
        add_row(3, "Enable Logging (True/False)", "enable_logging", sim.enable_logging)
        add_row(4, "Log Level", "log_level", sim.log_level)
        add_row(5, "Random Seed", "random_seed", sim.random_seed if sim.random_seed is not None else "")

        ttk.Label(grid, text="Note: world_config can be set in code or extended here.").grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=4, pady=4)

    def _build_constants_tabs(self) -> None:
        # Group constants logically by names
        groups: Dict[str, Tuple[str, ...]] = {
            "World": (
                "GRID_WIDTH", "GRID_HEIGHT", "TERRAIN_DISTRIBUTION", "FOOD_SPAWN_CHANCE", "WATER_SPAWN_CHANCE",
                "TERRAIN_MOVEMENT_MODIFIERS", "SWAMP_SICKNESS_CHANCE",
            ),
            "Animals": (
                "STANDARD_TRAIT_MIN", "STANDARD_TRAIT_MAX", "PRIMARY_TRAIT_MIN", "PRIMARY_TRAIT_MAX",
                "BASE_HEALTH", "HEALTH_PER_ENDURANCE", "BASE_ENERGY", "ENERGY_PER_ENDURANCE",
                "INITIAL_TRAINING_POINTS",
            ),
            "Status & Costs": (
                "HUNGER_DEPLETION_RATE", "THIRST_DEPLETION_RATE", "PASSIVE_ENERGY_REGEN",
                "STARVATION_DAMAGE", "DEHYDRATION_DAMAGE",
                "MOVEMENT_BASE_COST", "MOVEMENT_AGILITY_MULTIPLIER", "REST_ENERGY_GAIN",
                "PLANT_FOOD_GAIN", "PREY_FOOD_GAIN", "DRINKING_THIRST_GAIN",
            ),
            "Combat": (
                "STRENGTH_DAMAGE_MULTIPLIER", "AGILITY_EVASION_MULTIPLIER",
            ),
            "Events & Disasters": (
                "RESOURCE_SCARCITY_GAIN", "ROCKSLIDE_ESCAPE_DC", "ROCKSLIDE_HIDE_DC", "ROCKSLIDE_DAMAGE",
                "CURIOUS_OBJECT_DC", "MIGRATION_ENERGY_BONUS", "RESOURCE_BLOOM_MULTIPLIER",
                "DROUGHT_WATER_REDUCTION", "WILDFIRE_DAMAGE", "FLOOD_DAMAGE", "CONTAMINATION_SAVE_DC",
                "EARTHQUAKE_INJURY_CHANCE", "WINTER_DEPLETION_MULTIPLIER",
            ),
            "Fitness & MLP": (
                "FITNESS_WEIGHTS", "INPUT_NODES", "HIDDEN_LAYER_1_NODES", "HIDDEN_LAYER_2_NODES",
                "OUTPUT_NODES", "HIDDEN_ACTIVATION", "OUTPUT_ACTIVATION",
            ),
            "Simulation": (
                "MAX_WEEKS_PER_GENERATION", "POPULATION_SIZE", "ELITE_PERCENTAGE", "TOURNAMENT_SIZE",
                "MUTATION_RATE",
            ),
            "Logging": (
                "DEBUG_MODE", "LOG_LEVEL", "SAVE_SIMULATION_DATA",
            ),
        }

        for tab_name, keys in groups.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)

            canvas = tk.Canvas(frame)
            scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
            inner = ttk.Frame(canvas)
            inner.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            win = canvas.create_window((0, 0), window=inner, anchor="nw")
            canvas.configure(yscrollcommand=scroll.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

            row = 0
            for key in keys:
                if not hasattr(constants_module, key):
                    continue
                val = getattr(constants_module, key)
                ttk.Label(inner, text=key).grid(row=row, column=0, sticky=tk.W, padx=6, pady=6)
                if isinstance(val, (dict, list)):
                    txt = tk.Text(inner, height=5, width=50)
                    txt.insert("1.0", json.dumps(val, indent=2))
                    txt.grid(row=row, column=1, sticky=tk.EW, padx=6, pady=6)
                    self._dict_texts[f"constants.{key}"] = txt
                else:
                    var = tk.StringVar(value=str(val))
                    ent = ttk.Entry(inner, textvariable=var)
                    ent.grid(row=row, column=1, sticky=tk.EW, padx=6, pady=6)
                    self._field_vars[f"constants.{key}"] = var
                inner.columnconfigure(1, weight=1)
                row += 1

    # ----------------------- Actions -----------------------
    def _on_load(self) -> None:
        path = filedialog.askopenfilename(title="Load Config", filetypes=[("JSON", "*.json"), ("All", "*.*")], initialfile=self.config_path)
        if not path:
            return
        try:
            self._load_from_path(path)
            self.config_path = path
            messagebox.showinfo("Config", f"Loaded: {path}")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to load config: {exc}")

    def _on_save(self) -> None:
        path = filedialog.asksaveasfilename(title="Save Config", defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=self.config_path)
        if not path:
            return
        try:
            cfg = self._collect_config_from_ui()
            cfg.save(path)
            self.config_path = path
            messagebox.showinfo("Config", f"Saved: {path}")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to save config: {exc}")

    def _on_apply(self) -> None:
        try:
            cfg = self._collect_config_from_ui()
            report = cfg.apply_to_runtime()
            self.app_config = cfg
            messagebox.showinfo("Applied", json.dumps(report, indent=2, default=str))
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to apply: {exc}")

    def _on_reset(self) -> None:
        self.app_config = AppConfig.from_defaults()
        self._populate_ui_from_config(self.app_config)

    # ----------------------- Helpers -----------------------
    def _load_from_path(self, path: str) -> None:
        cfg = AppConfig.load(path)
        self._populate_ui_from_config(cfg)
        self.app_config = cfg

    def _populate_ui_from_config(self, cfg: AppConfig) -> None:
        # Simulation fields
        sim = cfg.simulation
        mapping = {
            "max_weeks": sim.max_weeks,
            "max_generations": sim.max_generations,
            "population_size": sim.population_size,
            "enable_logging": sim.enable_logging,
            "log_level": sim.log_level,
            "random_seed": "" if sim.random_seed is None else sim.random_seed,
        }
        for key, value in mapping.items():
            var = self._field_vars.get(f"simulation.{key}")
            if var is not None:
                var.set(str(value))

        # Constants overrides: merge current constants with overrides, show effective values
        for name, var in list(self._field_vars.items()):
            if not name.startswith("constants."):
                continue
            const_name = name.split(".", 1)[1]
            effective = cfg.constants_overrides.get(const_name, getattr(constants_module, const_name, ""))
            var.set(self._to_string(effective))
        for name, txt in list(self._dict_texts.items()):
            const_name = name.split(".", 1)[1]
            effective = cfg.constants_overrides.get(const_name, getattr(constants_module, const_name, {}))
            try:
                txt.delete("1.0", tk.END)
                txt.insert("1.0", json.dumps(effective, indent=2))
            except Exception:
                txt.delete("1.0", tk.END)
                txt.insert("1.0", str(effective))

    def _collect_config_from_ui(self) -> AppConfig:
        # Simulation
        def parse_bool(text: str) -> bool:
            return text.strip().lower() in {"1", "true", "yes", "y", "on"}

        def parse_maybe_int(text: str) -> Optional[int]:
            t = text.strip()
            if t == "":
                return None
            return int(t)

        sim = SimulationConfig(
            max_weeks=int(self._field_vars["simulation.max_weeks"].get()),
            max_generations=int(self._field_vars["simulation.max_generations"].get()),
            population_size=int(self._field_vars["simulation.population_size"].get()),
            enable_logging=parse_bool(self._field_vars["simulation.enable_logging"].get()),
            log_level=self._field_vars["simulation.log_level"].get().strip() or "INFO",
            random_seed=parse_maybe_int(self._field_vars["simulation.random_seed"].get()),
        )

        # Constants overrides
        overrides: Dict[str, Any] = {}

        # Simple fields
        for name, var in self._field_vars.items():
            if not name.startswith("constants."):
                continue
            const_name = name.split(".", 1)[1]
            text = var.get().strip()
            if text == "":
                continue
            overrides[const_name] = self._parse_scalar(text)

        # Dict/list fields
        for name, txt in self._dict_texts.items():
            const_name = name.split(".", 1)[1]
            content = txt.get("1.0", tk.END).strip()
            if content == "":
                continue
            try:
                overrides[const_name] = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: store as string
                overrides[const_name] = content

        return AppConfig(simulation=sim, constants_overrides=overrides)

    def _parse_scalar(self, text: str) -> Any:
        t = text.strip()
        # Try bool
        lower = t.lower()
        if lower in {"true", "false"}:
            return lower == "true"
        # Try int
        try:
            return int(t)
        except ValueError:
            pass
        # Try float
        try:
            return float(t)
        except ValueError:
            pass
        # Otherwise, return as string
        return t

    def _to_string(self, value: Any) -> str:
        if isinstance(value, bool):
            return "True" if value else "False"
        if isinstance(value, (int, float, str)):
            return str(value)
        try:
            return json.dumps(value)
        except Exception:
            return str(value)

    def run(self) -> None:
        self.root.mainloop()


def run_config_gui(config_path: str = "config.json") -> None:
    gui = ConfigGUI(config_path)
    gui.run()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="EvoSim configuration manager")
    parser.add_argument("--config", default="config.json", help="Path to JSON config file")
    parser.add_argument("--save-defaults", action="store_true", help="Write default config to path and exit")
    parser.add_argument("--gui", action="store_true", help="Launch graphical configuration UI")
    args = parser.parse_args()

    if args.save_defaults:
        AppConfig.from_defaults().save(args.config)
        print(f"Wrote default config to {args.config}")
    elif args.gui:
        run_config_gui(args.config)
    else:
        cfg = load_and_apply_config(args.config)
        report = cfg.apply_to_runtime()
        print("Applied constant overrides:", json.dumps(report, indent=2, default=str))
        print("Simulation config:", json.dumps(asdict(cfg.simulation), indent=2))
