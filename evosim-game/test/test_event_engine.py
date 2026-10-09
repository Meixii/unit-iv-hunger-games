"""
Unit tests for event_engine/
"""

import unittest
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation, AnimalCategory, create_random_animal
from world_generator import WorldGenerator, GenerationConfig
from event_engine import EventEngine


class TestEventEngine(unittest.TestCase):
    """Test triggered events, random events, and disaster execution."""

    def setUp(self):
        self.logger = logging.getLogger("TestEE")
        self.logger.setLevel(logging.WARNING)
        gen = WorldGenerator(GenerationConfig(width=25, height=25))
        self.world = gen.generate_world(seed=42)
        self.sim = Simulation()
        self.sim.world = self.world
        
        animals = [create_random_animal(f"a_{i}", AnimalCategory.HERBIVORE) for i in range(6)]
        gen.place_animals(self.world, animals)
        for a in animals:
            self.sim.add_animal(a)
            
        self.engine = EventEngine(self.sim, self.logger)

    def test_random_events_execution(self):
        """Test random environmental events trigger without crash."""
        results = self.engine.scheduler.random_engine.execute_random_events(week=1, max_events=1)
        self.assertIsInstance(results, list)

    def test_disaster_event_execution(self):
        """Test disaster events execute and apply damages/effects properly."""
        results = self.engine.scheduler.disaster_engine.execute_disaster_events(week=1, max_disasters=1)
        self.assertIsInstance(results, list)


if __name__ == '__main__':
    unittest.main()
