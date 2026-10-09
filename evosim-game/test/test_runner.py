"""
Master test runner for EvoSim.
Runs all unit and integration test suites.
"""

import unittest
import sys
import os

# Set paths
test_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(test_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)


def run_all_tests():
    """Discover and execute all test cases."""
    print("=" * 70)
    print("               EVOSIM COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    if result.wasSuccessful():
        print("RESULT: ALL TESTS PASSED SUCCESSFULLY! ✅")
    else:
        print("RESULT: TEST SUITE FAILED ❌")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
