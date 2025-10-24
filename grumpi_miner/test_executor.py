"""
Test execution engine for GrumpiMiner.
Executes tests for dimension combinations and records results.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
from enum import Enum

from .combination_generator import DimensionCombination


class TestStatus(Enum):
    """Status of a test execution."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestResult:
    """Result of executing a test on a dimension combination."""
    combination: DimensionCombination
    status: TestStatus
    execution_time: float = 0.0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        status_str = f"[{self.status.value.upper()}]"
        combo_str = str(self.combination)
        time_str = f"({self.execution_time:.3f}s)"
        
        result = f"{status_str} {combo_str} {time_str}"
        if self.error_message:
            result += f"\n  Error: {self.error_message}"
        return result


@dataclass
class TestSuite:
    """Collection of test results."""
    name: str
    results: List[TestResult] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    def add_result(self, result: TestResult) -> None:
        """Add a test result to the suite."""
        self.results.append(result)
    
    def mark_complete(self) -> None:
        """Mark the test suite as complete."""
        self.end_time = datetime.now()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of test results."""
        status_counts = {}
        for status in TestStatus:
            status_counts[status.value] = sum(
                1 for r in self.results if r.status == status
            )
        
        total_time = sum(r.execution_time for r in self.results)
        duration = None
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            "name": self.name,
            "total_tests": len(self.results),
            "status_counts": status_counts,
            "total_execution_time": total_time,
            "suite_duration": duration,
            "pass_rate": (
                status_counts["passed"] / len(self.results) * 100
                if self.results else 0
            ),
        }


class TestExecutor:
    """Executes tests on dimension combinations."""
    
    def __init__(self, test_function: Optional[Callable] = None):
        """
        Initialize the test executor.
        
        Args:
            test_function: Function to execute for each combination.
                          Should accept a DimensionCombination and return bool.
        """
        self.test_function = test_function or self._default_test_function
    
    def _default_test_function(self, combination: DimensionCombination) -> bool:
        """Default test function that always passes."""
        # This is a placeholder - real tests would implement actual logic
        return True
    
    def execute_test(
        self, 
        combination: DimensionCombination,
        timeout: Optional[float] = None
    ) -> TestResult:
        """
        Execute a test on a single combination.
        
        Args:
            combination: The dimension combination to test
            timeout: Optional timeout in seconds
        
        Returns:
            TestResult instance
        """
        import time
        
        start_time = time.time()
        status = TestStatus.PENDING
        error_message = None
        metadata = {}
        
        try:
            status = TestStatus.RUNNING
            result = self.test_function(combination)
            status = TestStatus.PASSED if result else TestStatus.FAILED
        except TimeoutError:
            status = TestStatus.ERROR
            error_message = f"Test timed out after {timeout}s"
        except Exception as e:
            status = TestStatus.ERROR
            error_message = str(e)
        
        execution_time = time.time() - start_time
        
        return TestResult(
            combination=combination,
            status=status,
            execution_time=execution_time,
            error_message=error_message,
            metadata=metadata,
        )
    
    def execute_batch(
        self,
        combinations: List[DimensionCombination],
        suite_name: str = "Combination Tests",
        parallel: bool = False,
        max_workers: int = 4
    ) -> TestSuite:
        """
        Execute tests on a batch of combinations.
        
        Args:
            combinations: List of dimension combinations to test
            suite_name: Name of the test suite
            parallel: Whether to run tests in parallel
            max_workers: Maximum number of parallel workers
        
        Returns:
            TestSuite with all results
        """
        suite = TestSuite(name=suite_name)
        
        if parallel:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(self.execute_test, combo): combo
                    for combo in combinations
                }
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    suite.add_result(result)
        else:
            for combo in combinations:
                result = self.execute_test(combo)
                suite.add_result(result)
        
        suite.mark_complete()
        return suite
    
    def execute_with_callback(
        self,
        combinations: List[DimensionCombination],
        callback: Callable[[TestResult], None],
        suite_name: str = "Combination Tests"
    ) -> TestSuite:
        """
        Execute tests with a callback for each result.
        
        Args:
            combinations: List of dimension combinations to test
            callback: Function to call with each TestResult
            suite_name: Name of the test suite
        
        Returns:
            TestSuite with all results
        """
        suite = TestSuite(name=suite_name)
        
        for combo in combinations:
            result = self.execute_test(combo)
            suite.add_result(result)
            callback(result)
        
        suite.mark_complete()
        return suite
