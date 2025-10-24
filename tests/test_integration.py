"""
Integration tests for the complete GrumpiMiner system.
Tests the full workflow of combination generation, execution, and reporting.
"""

import unittest
from grumpi_miner.combination_generator import CombinationGenerator
from grumpi_miner.test_executor import TestExecutor, TestStatus
from grumpi_miner.reporter import TestReporter
from grumpi_miner.dimensions import (
    FormatVariation,
    StructuralArchitecture,
    ModelOrchestration,
    TemporalDynamics,
)


class TestIntegrationWorkflow(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_end_to_end_2way_combinations(self):
        """Test complete workflow with 2-way combinations."""
        # 1. Generate combinations
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        combinations = generator.generate_all_combinations(max_per_dimension=2)
        
        self.assertIn(2, combinations)
        self.assertGreater(len(combinations[2]), 0)
        
        # 2. Execute tests
        executor = TestExecutor()
        suite = executor.execute_batch(
            combinations[2][:5],
            suite_name="Integration Test"
        )
        
        self.assertEqual(len(suite.results), 5)
        
        # 3. Generate report
        reporter = TestReporter()
        report = reporter.generate_report(suite)
        
        self.assertIn("Integration Test", report)
        self.assertIn("Total Tests: 5", report)
    
    def test_end_to_end_3way_combinations(self):
        """Test complete workflow with 3-way combinations."""
        generator = CombinationGenerator(min_dimensions=3, max_dimensions=3)
        combinations = generator.generate_all_combinations(max_per_dimension=1)
        
        executor = TestExecutor()
        suite = executor.execute_batch(
            combinations[3][:10],
            suite_name="3-Way Integration Test"
        )
        
        # Verify all combinations have 3 dimensions
        for result in suite.results:
            self.assertEqual(len(result.combination.dimensions), 3)
        
        reporter = TestReporter()
        report = reporter.generate_report(suite)
        self.assertIn("3-Way Integration Test", report)
    
    def test_combination_interactions_detection(self):
        """Test that the system can detect interaction-specific issues."""
        interaction_issues = []
        
        def interaction_test_function(combination):
            """Test function that fails on specific dimension interactions."""
            dims = combination.dimensions
            
            # Fail when JSON + Hierarchical appears together
            if (dims.get("FormatVariation") == FormatVariation.JSON and
                dims.get("StructuralArchitecture") == StructuralArchitecture.HIERARCHICAL):
                interaction_issues.append(combination)
                return False
            
            return True
        
        # Generate combinations that include this pair
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        group = (FormatVariation, StructuralArchitecture)
        combinations = generator.generate_combinations_for_group(group)
        
        # Execute tests
        executor = TestExecutor(test_function=interaction_test_function)
        suite = executor.execute_batch(combinations)
        
        # Should have detected the interaction issue
        self.assertGreater(len(interaction_issues), 0)
        
        # Should have some failures
        failures = [r for r in suite.results if r.status == TestStatus.FAILED]
        self.assertGreater(len(failures), 0)
    
    def test_multi_dimension_interaction_detection(self):
        """Test detection of 3-way interaction issues."""
        def three_way_test(combination):
            """Fail on specific 3-way interaction."""
            dims = combination.dimensions
            
            # Specific 3-way interaction that should fail
            if (dims.get("FormatVariation") == FormatVariation.JSON and
                dims.get("StructuralArchitecture") == StructuralArchitecture.HIERARCHICAL and
                dims.get("ModelOrchestration") == ModelOrchestration.PARALLEL):
                return False
            
            return True
        
        generator = CombinationGenerator(min_dimensions=3, max_dimensions=3)
        group = (FormatVariation, StructuralArchitecture, ModelOrchestration)
        combinations = generator.generate_combinations_for_group(group)
        
        executor = TestExecutor(test_function=three_way_test)
        suite = executor.execute_batch(combinations)
        
        # Should have at least one failure from the 3-way interaction
        failures = [r for r in suite.results if r.status == TestStatus.FAILED]
        self.assertGreater(len(failures), 0)
        
        # Verify the failure is for the correct 3-way combination
        for failure in failures:
            dims = failure.combination.dimensions
            self.assertEqual(dims.get("FormatVariation"), FormatVariation.JSON)
            self.assertEqual(dims.get("StructuralArchitecture"), StructuralArchitecture.HIERARCHICAL)
            self.assertEqual(dims.get("ModelOrchestration"), ModelOrchestration.PARALLEL)


class TestSystemCapabilities(unittest.TestCase):
    """Test system capabilities as specified in requirements."""
    
    def test_all_10_dimensions_available(self):
        """Verify all 10 dimensions are available for testing."""
        from grumpi_miner.dimensions import DIMENSION_CLASSES
        
        # Must have exactly 10 dimensions
        self.assertEqual(len(DIMENSION_CLASSES), 10)
        
        # Each dimension must have values
        for dim_class in DIMENSION_CLASSES:
            values = list(dim_class)
            self.assertGreater(len(values), 0)
    
    def test_can_generate_all_pairwise_combinations(self):
        """Test that system can generate all pairwise (2-way) combinations."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        pairs = generator.generate_dimension_pairs()
        
        # Should have C(10, 2) = 45 pairs
        self.assertEqual(len(pairs), 45)
    
    def test_can_test_combinations_not_individual_dimensions(self):
        """Verify system tests combinations, not individual dimensions."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        combinations = generator.generate_all_combinations(max_per_dimension=1)
        
        # All combinations should have at least 2 dimensions
        for combo in combinations[2]:
            self.assertGreaterEqual(len(combo.dimensions), 2)
    
    def test_supports_higher_order_combinations(self):
        """Test support for 3-way, 4-way, and higher combinations."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=5)
        
        # Test each level
        for size in range(2, 6):
            groups = generator.generate_dimension_groups(size)
            self.assertGreater(len(groups), 0)
    
    def test_dimension_interaction_tracking(self):
        """Test that dimension interactions are properly tracked."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        group = (FormatVariation, StructuralArchitecture)
        combinations = generator.generate_combinations_for_group(group)
        
        executor = TestExecutor()
        suite = executor.execute_batch(combinations)
        
        # Generate dimension analysis
        reporter = TestReporter()
        analysis = reporter.format_dimension_analysis(suite)
        
        # Should include both dimensions
        self.assertIn("FormatVariation", analysis)
        self.assertIn("StructuralArchitecture", analysis)
    
    def test_json_export_preserves_combination_data(self):
        """Test that JSON export preserves all combination information."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        combinations = generator.generate_all_combinations(max_per_dimension=1)
        
        executor = TestExecutor()
        suite = executor.execute_batch(combinations[2][:5])
        
        reporter = TestReporter()
        json_data = reporter.export_json(suite)
        
        # Should have all results
        self.assertEqual(len(json_data['results']), 5)
        
        # Each result should have combination data
        for result in json_data['results']:
            self.assertIn('combination', result)
            self.assertGreaterEqual(len(result['combination']), 2)


class TestScalability(unittest.TestCase):
    """Test system scalability with large combination spaces."""
    
    def test_sampling_reduces_combination_space(self):
        """Test that sampling effectively reduces the combination space."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        
        # Full space
        all_combos = generator.generate_all_combinations(max_per_dimension=3)
        full_count = len(all_combos[2])
        
        # Sampled space
        samples = generator.generate_sample_combinations(samples_per_size=10)
        sample_count = len(samples[2])
        
        # Sample should be smaller
        self.assertLess(sample_count, full_count)
        self.assertLessEqual(sample_count, 10)
    
    def test_max_per_dimension_limits_combinations(self):
        """Test that max_per_dimension effectively limits combinations."""
        generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        group = (FormatVariation, StructuralArchitecture)
        
        # With limit
        limited = generator.generate_combinations_for_group(group, max_per_dimension=2)
        
        # Without limit
        unlimited = generator.generate_combinations_for_group(group)
        
        # Limited should be smaller
        self.assertLess(len(limited), len(unlimited))


if __name__ == '__main__':
    unittest.main()
