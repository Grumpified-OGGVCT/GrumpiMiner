#!/usr/bin/env python3
"""
Example usage of the GrumpiMiner combination testing framework.
Demonstrates testing interactions between multiple dimensions.
"""

from grumpi_miner.combination_generator import CombinationGenerator, DimensionCombination
from grumpi_miner.test_executor import TestExecutor, TestStatus
from grumpi_miner.reporter import TestReporter
from grumpi_miner.dimensions import (
    FormatVariation,
    StructuralArchitecture,
    ModelOrchestration,
    ContextRepresentation,
)


def example_test_function(combination: DimensionCombination) -> bool:
    """
    Example test function that validates dimension combinations.
    
    This demonstrates testing the INTERACTIONS between dimensions,
    not just each dimension independently.
    """
    dims = combination.dimensions
    
    # Example interaction rule: JSON format with hierarchical structure
    # requires extended context representation
    if (dims.get("FormatVariation") == FormatVariation.JSON and
        dims.get("StructuralArchitecture") == StructuralArchitecture.HIERARCHICAL and
        dims.get("ContextRepresentation") == ContextRepresentation.MINIMAL):
        # This combination is invalid - hierarchical JSON needs more context
        return False
    
    # Example interaction rule: Parallel orchestration with static temporal
    # dynamics is incompatible
    if (dims.get("ModelOrchestration") == ModelOrchestration.PARALLEL and
        dims.get("TemporalDynamics")):
        from grumpi_miner.dimensions import TemporalDynamics
        if dims.get("TemporalDynamics") == TemporalDynamics.STATIC:
            return False
    
    # Most combinations are valid
    return True


def run_basic_example():
    """Run a basic example with 2-way combinations."""
    print("\n" + "="*80)
    print("BASIC EXAMPLE: 2-Way Dimension Combinations")
    print("="*80)
    
    # Generate 2-way combinations
    generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
    combinations = generator.generate_all_combinations(max_per_dimension=2)
    
    # Execute tests
    executor = TestExecutor(test_function=example_test_function)
    suite = executor.execute_batch(
        combinations[2][:10],  # Test first 10 combinations
        suite_name="Basic 2-Way Combinations"
    )
    
    # Report results
    reporter = TestReporter(verbose=True)
    report = reporter.generate_report(suite, include_details=False)
    print(report)


def run_advanced_example():
    """Run an advanced example with 3-way combinations."""
    print("\n" + "="*80)
    print("ADVANCED EXAMPLE: 3-Way Dimension Combinations")
    print("="*80)
    
    # Generate 3-way combinations
    generator = CombinationGenerator(min_dimensions=3, max_dimensions=3)
    combinations = generator.generate_all_combinations(max_per_dimension=2)
    
    # Execute tests
    executor = TestExecutor(test_function=example_test_function)
    suite = executor.execute_batch(
        combinations[3][:20],  # Test first 20 combinations
        suite_name="Advanced 3-Way Combinations"
    )
    
    # Report results
    reporter = TestReporter(verbose=False)
    report = reporter.generate_report(
        suite,
        include_details=False,
        include_dimension_analysis=True
    )
    print(report)


def run_comprehensive_example():
    """Run a comprehensive example testing all dimension sizes."""
    print("\n" + "="*80)
    print("COMPREHENSIVE EXAMPLE: Multi-Way Dimension Combinations")
    print("="*80)
    
    # Generate samples across different combination sizes
    generator = CombinationGenerator(min_dimensions=2, max_dimensions=5)
    samples = generator.generate_sample_combinations(samples_per_size=5)
    
    # Execute tests for each combination size
    reporter = TestReporter(verbose=False)
    
    for size in sorted(samples.keys()):
        if samples[size]:
            print(f"\n--- Testing {size}-Way Combinations ---")
            
            executor = TestExecutor(test_function=example_test_function)
            suite = executor.execute_batch(
                samples[size],
                suite_name=f"{size}-Way Combinations"
            )
            
            # Print summary
            summary = suite.get_summary()
            print(f"Total: {summary['total_tests']}, "
                  f"Passed: {summary['status_counts']['passed']}, "
                  f"Failed: {summary['status_counts']['failed']}, "
                  f"Pass Rate: {summary['pass_rate']:.1f}%")


def run_interactive_callback_example():
    """Run example with real-time callback reporting."""
    print("\n" + "="*80)
    print("INTERACTIVE EXAMPLE: Real-Time Test Reporting")
    print("="*80)
    
    generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
    combinations = generator.generate_all_combinations(max_per_dimension=2)
    
    def progress_callback(result):
        """Callback to print each result as it completes."""
        status_symbol = "✓" if result.status == TestStatus.PASSED else "✗"
        print(f"{status_symbol} {result}")
    
    executor = TestExecutor(test_function=example_test_function)
    suite = executor.execute_with_callback(
        combinations[2][:10],
        callback=progress_callback,
        suite_name="Interactive Tests"
    )
    
    print(f"\nCompleted {len(suite.results)} tests")


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# GrumpiMiner - Total Frontier Exploration System")
    print("# Mining Across ALL Complexity Dimensions Simultaneously")
    print("#"*80)
    
    # Run examples
    run_basic_example()
    run_advanced_example()
    run_comprehensive_example()
    run_interactive_callback_example()
    
    print("\n" + "#"*80)
    print("# Examples Complete!")
    print("#"*80 + "\n")
