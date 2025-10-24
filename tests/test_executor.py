"""
Tests for test executor.
"""

import unittest
from grumpi_miner.test_executor import (
    TestExecutor,
    TestResult,
    TestSuite,
    TestStatus,
)
from grumpi_miner.combination_generator import DimensionCombination
from grumpi_miner.dimensions import FormatVariation, StructuralArchitecture


class TestTestResult(unittest.TestCase):
    """Test TestResult class."""
    
    def test_result_creation(self):
        """Test creating a test result."""
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        result = TestResult(
            combination=combo,
            status=TestStatus.PASSED,
            execution_time=0.5,
        )
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertEqual(result.execution_time, 0.5)
    
    def test_result_string_representation(self):
        """Test string representation of result."""
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        result = TestResult(
            combination=combo,
            status=TestStatus.PASSED,
            execution_time=0.5,
        )
        str_repr = str(result)
        self.assertIn("PASSED", str_repr)


class TestTestSuite(unittest.TestCase):
    """Test TestSuite class."""
    
    def test_suite_creation(self):
        """Test creating a test suite."""
        suite = TestSuite(name="Test Suite")
        self.assertEqual(suite.name, "Test Suite")
        self.assertEqual(len(suite.results), 0)
    
    def test_add_result(self):
        """Test adding results to suite."""
        suite = TestSuite(name="Test Suite")
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        result = TestResult(
            combination=combo,
            status=TestStatus.PASSED,
        )
        suite.add_result(result)
        self.assertEqual(len(suite.results), 1)
    
    def test_suite_summary(self):
        """Test suite summary generation."""
        suite = TestSuite(name="Test Suite")
        
        # Add some results
        for status in [TestStatus.PASSED, TestStatus.PASSED, TestStatus.FAILED]:
            combo = DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.JSON,
            })
            result = TestResult(combination=combo, status=status)
            suite.add_result(result)
        
        suite.mark_complete()
        summary = suite.get_summary()
        
        self.assertEqual(summary['total_tests'], 3)
        self.assertEqual(summary['status_counts']['passed'], 2)
        self.assertEqual(summary['status_counts']['failed'], 1)
        self.assertAlmostEqual(summary['pass_rate'], 66.67, places=1)


class TestTestExecutor(unittest.TestCase):
    """Test TestExecutor class."""
    
    def test_executor_creation(self):
        """Test creating a test executor."""
        executor = TestExecutor()
        self.assertIsNotNone(executor.test_function)
    
    def test_default_test_function(self):
        """Test default test function always passes."""
        executor = TestExecutor()
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        result = executor.execute_test(combo)
        self.assertEqual(result.status, TestStatus.PASSED)
    
    def test_custom_test_function(self):
        """Test executor with custom test function."""
        def always_fail(combo):
            return False
        
        executor = TestExecutor(test_function=always_fail)
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        result = executor.execute_test(combo)
        self.assertEqual(result.status, TestStatus.FAILED)
    
    def test_execute_batch(self):
        """Test executing a batch of tests."""
        executor = TestExecutor()
        combos = [
            DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.JSON,
            }),
            DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.XML,
            }),
        ]
        
        suite = executor.execute_batch(combos, suite_name="Batch Test")
        self.assertEqual(suite.name, "Batch Test")
        self.assertEqual(len(suite.results), 2)
    
    def test_execute_with_callback(self):
        """Test executing tests with callback."""
        executor = TestExecutor()
        results_received = []
        
        def callback(result):
            results_received.append(result)
        
        combos = [
            DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.JSON,
            }),
        ]
        
        suite = executor.execute_with_callback(combos, callback)
        self.assertEqual(len(results_received), 1)
        self.assertEqual(len(suite.results), 1)
    
    def test_error_handling(self):
        """Test executor handles exceptions."""
        def error_function(combo):
            raise ValueError("Test error")
        
        executor = TestExecutor(test_function=error_function)
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        result = executor.execute_test(combo)
        
        self.assertEqual(result.status, TestStatus.ERROR)
        self.assertIsNotNone(result.error_message)
        self.assertIn("Test error", result.error_message)


class TestCombinationTesting(unittest.TestCase):
    """Test that the executor properly tests dimension combinations."""
    
    def test_combination_testing_logic(self):
        """Test that test function receives correct combinations."""
        tested_combinations = []
        
        def test_function(combo):
            tested_combinations.append(combo)
            return True
        
        executor = TestExecutor(test_function=test_function)
        combos = [
            DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.JSON,
                "StructuralArchitecture": StructuralArchitecture.HIERARCHICAL,
            }),
        ]
        
        suite = executor.execute_batch(combos)
        
        # Verify the combination was tested
        self.assertEqual(len(tested_combinations), 1)
        self.assertEqual(len(tested_combinations[0].dimensions), 2)
    
    def test_interaction_testing(self):
        """Test that combinations test interactions between dimensions."""
        interactions_found = []
        
        def test_function(combo):
            # Record which dimensions are being tested together
            dim_names = sorted(combo.dimensions.keys())
            interactions_found.append(tuple(dim_names))
            return True
        
        executor = TestExecutor(test_function=test_function)
        
        # Create combinations with different dimension pairs
        combos = [
            DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.JSON,
                "StructuralArchitecture": StructuralArchitecture.HIERARCHICAL,
            }),
            DimensionCombination(dimensions={
                "FormatVariation": FormatVariation.XML,
                "StructuralArchitecture": StructuralArchitecture.FLAT,
            }),
        ]
        
        suite = executor.execute_batch(combos)
        
        # Both combinations should test the same dimension interaction
        self.assertEqual(len(interactions_found), 2)
        self.assertEqual(interactions_found[0], interactions_found[1])
        self.assertIn("FormatVariation", interactions_found[0])
        self.assertIn("StructuralArchitecture", interactions_found[0])


if __name__ == '__main__':
    unittest.main()
