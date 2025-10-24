"""
Test reporting utilities for GrumpiMiner.
Formats and displays test results in various formats.
"""

from typing import List, Dict, Any, Optional
from .test_executor import TestSuite, TestResult, TestStatus
from .combination_generator import DimensionCombination


class TestReporter:
    """Formats and displays test results."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the test reporter.
        
        Args:
            verbose: Whether to include detailed output
        """
        self.verbose = verbose
    
    def format_summary(self, suite: TestSuite) -> str:
        """Format a summary of the test suite."""
        summary = suite.get_summary()
        
        lines = [
            f"\n{'='*70}",
            f"Test Suite: {summary['name']}",
            f"{'='*70}",
            f"Total Tests: {summary['total_tests']}",
            f"",
        ]
        
        # Status breakdown
        lines.append("Status Breakdown:")
        for status, count in summary['status_counts'].items():
            if count > 0:
                percentage = (count / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
                lines.append(f"  {status.upper():12} : {count:5} ({percentage:5.1f}%)")
        
        lines.append("")
        lines.append(f"Pass Rate: {summary['pass_rate']:.1f}%")
        lines.append(f"Total Execution Time: {summary['total_execution_time']:.3f}s")
        
        if summary['suite_duration']:
            lines.append(f"Suite Duration: {summary['suite_duration']:.3f}s")
        
        lines.append(f"{'='*70}\n")
        
        return "\n".join(lines)
    
    def format_detailed_results(self, suite: TestSuite) -> str:
        """Format detailed results for all tests."""
        lines = [
            f"\nDetailed Results for '{suite.name}':",
            f"{'-'*70}",
        ]
        
        for i, result in enumerate(suite.results, 1):
            lines.append(f"\n{i}. {result}")
            
            if self.verbose and result.metadata:
                lines.append("   Metadata:")
                for key, value in result.metadata.items():
                    lines.append(f"     {key}: {value}")
        
        lines.append(f"\n{'-'*70}\n")
        return "\n".join(lines)
    
    def format_failures(self, suite: TestSuite) -> str:
        """Format only failed and error test results."""
        failures = [
            r for r in suite.results
            if r.status in [TestStatus.FAILED, TestStatus.ERROR]
        ]
        
        if not failures:
            return "\nNo failures or errors!\n"
        
        lines = [
            f"\nFailures and Errors ({len(failures)}):",
            f"{'-'*70}",
        ]
        
        for i, result in enumerate(failures, 1):
            lines.append(f"\n{i}. {result}")
        
        lines.append(f"\n{'-'*70}\n")
        return "\n".join(lines)
    
    def format_dimension_analysis(self, suite: TestSuite) -> str:
        """Analyze results by dimension."""
        from collections import defaultdict
        
        dimension_stats = defaultdict(lambda: {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'error': 0
        })
        
        # Collect stats for each dimension type
        for result in suite.results:
            for dim_name, dim_value in result.combination.dimensions.items():
                key = f"{dim_name}:{dim_value.value}"
                dimension_stats[key]['total'] += 1
                
                if result.status == TestStatus.PASSED:
                    dimension_stats[key]['passed'] += 1
                elif result.status == TestStatus.FAILED:
                    dimension_stats[key]['failed'] += 1
                elif result.status == TestStatus.ERROR:
                    dimension_stats[key]['error'] += 1
        
        lines = [
            f"\nDimension Analysis:",
            f"{'-'*70}",
        ]
        
        for dim_key in sorted(dimension_stats.keys()):
            stats = dimension_stats[dim_key]
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            lines.append(
                f"{dim_key:50} : {stats['total']:4} tests, "
                f"{pass_rate:5.1f}% pass rate"
            )
        
        lines.append(f"\n{'-'*70}\n")
        return "\n".join(lines)
    
    def generate_report(
        self, 
        suite: TestSuite, 
        include_details: bool = False,
        include_dimension_analysis: bool = True
    ) -> str:
        """
        Generate a comprehensive report.
        
        Args:
            suite: The test suite to report on
            include_details: Whether to include detailed results
            include_dimension_analysis: Whether to include dimension analysis
        
        Returns:
            Formatted report string
        """
        report_parts = [
            self.format_summary(suite),
        ]
        
        if include_dimension_analysis:
            report_parts.append(self.format_dimension_analysis(suite))
        
        report_parts.append(self.format_failures(suite))
        
        if include_details:
            report_parts.append(self.format_detailed_results(suite))
        
        return "\n".join(report_parts)
    
    def export_json(self, suite: TestSuite) -> Dict[str, Any]:
        """Export test suite results as JSON-serializable dict."""
        return {
            "name": suite.name,
            "start_time": suite.start_time.isoformat(),
            "end_time": suite.end_time.isoformat() if suite.end_time else None,
            "summary": suite.get_summary(),
            "results": [
                {
                    "combination": {
                        dim_name: dim_value.value
                        for dim_name, dim_value in result.combination.dimensions.items()
                    },
                    "status": result.status.value,
                    "execution_time": result.execution_time,
                    "error_message": result.error_message,
                    "metadata": result.metadata,
                    "timestamp": result.timestamp.isoformat(),
                }
                for result in suite.results
            ],
        }
