# GrumpiMiner

Total Frontier Exploration System (EVERY Dimension Integrated). Mining Across ALL Complexity Dimensions Simultaneously.

## Overview

GrumpiMiner is a comprehensive testing framework designed to test **combinations of dimensions** rather than testing each dimension independently. It systematically explores interactions between multiple complexity dimensions to ensure thorough validation of complex systems.

## Key Concept: Combination Testing

Traditional testing often evaluates dimensions independently:
- ❌ Test format variations alone
- ❌ Test structural architectures alone  
- ❌ Test orchestration patterns alone

GrumpiMiner tests **interactions between dimensions**:
- ✅ Test JSON format + Hierarchical structure + Extended context
- ✅ Test XML format + Flat structure + Sequential orchestration
- ✅ Test any combination of 2, 3, 4, or more dimensions simultaneously

This approach reveals issues that only appear when specific dimensions are combined in particular ways.

## The 10 Complexity Dimensions

1. **Format Variations**: natural language, XML, JSON, YAML, code, LaTeX, diagrams, hybrid
2. **Structural Architectures**: flat, hierarchical, graph, tree, mesh, layered
3. **Model Orchestration Patterns**: single, sequential, parallel, hierarchical, ensemble, cascading
4. **Context Representations**: minimal, extended, contextual, global, windowed, dynamic
5. **Instruction Semantics**: imperative, declarative, functional, constraint-based, goal-oriented, example-based
6. **Verification Protocols**: none, basic, comprehensive, formal, statistical, heuristic
7. **Meta-Cognitive Scaffolding**: none, reflection, planning, monitoring, evaluation, adaptive
8. **Constraint Architecture**: unconstrained, soft, hard, adaptive, hierarchical, negotiable
9. **Cross-Modal Translation**: none, text-to-code, code-to-text, diagram-to-text, text-to-diagram, multimodal
10. **Temporal Dynamics**: static, sequential, concurrent, real-time, adaptive, predictive

## Installation

```bash
# Clone the repository
git clone https://github.com/Grumpified-OGGVCT/GrumpiMiner.git
cd GrumpiMiner

# Install the package
pip install -e .

# For development with testing tools
pip install -e ".[dev]"
```

## Quick Start

```python
from grumpi_miner.combination_generator import CombinationGenerator
from grumpi_miner.test_executor import TestExecutor
from grumpi_miner.reporter import TestReporter

# 1. Generate combinations (e.g., all 2-way dimension combinations)
generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
combinations = generator.generate_all_combinations(max_per_dimension=2)

# 2. Define your test function
def my_test_function(combination):
    """Test logic for dimension combinations."""
    # Your test logic here
    return True  # or False if test fails

# 3. Execute tests
executor = TestExecutor(test_function=my_test_function)
suite = executor.execute_batch(combinations[2], suite_name="My Tests")

# 4. Generate report
reporter = TestReporter()
report = reporter.generate_report(suite)
print(report)
```

## Usage Examples

### Basic 2-Way Combination Testing

```python
# Test all pairs of dimensions
generator = CombinationGenerator(min_dimensions=2, max_dimensions=2)
combinations = generator.generate_all_combinations(max_per_dimension=2)

# combinations[2] contains all 2-way combinations
# Example: Format:JSON + Structure:Hierarchical
```

### Advanced Multi-Way Testing

```python
# Test 3-way combinations
generator = CombinationGenerator(min_dimensions=3, max_dimensions=3)
combinations = generator.generate_all_combinations(max_per_dimension=2)

# combinations[3] contains all 3-way combinations
# Example: Format:JSON + Structure:Hierarchical + Context:Extended
```

### Sampling Large Combination Spaces

```python
# When the full combination space is too large, use sampling
generator = CombinationGenerator(min_dimensions=2, max_dimensions=5)
samples = generator.generate_sample_combinations(samples_per_size=10)

# Get 10 samples each of 2-way, 3-way, 4-way, and 5-way combinations
```

### Real-Time Progress Reporting

```python
def progress_callback(result):
    print(f"{'✓' if result.status == TestStatus.PASSED else '✗'} {result}")

executor = TestExecutor(test_function=my_test_function)
suite = executor.execute_with_callback(combinations, callback=progress_callback)
```

## Running the Examples

```bash
# Run the comprehensive example suite
python examples.py
```

This demonstrates:
- Basic 2-way combinations
- Advanced 3-way combinations
- Comprehensive multi-way testing
- Interactive real-time reporting

## Running Tests

```bash
# Run all unit tests
python -m unittest discover tests/ -v

# Run with pytest (if installed)
pytest tests/ -v
```

## Architecture

The framework consists of four main components:

1. **Dimensions** (`dimensions.py`): Defines the 10 complexity dimensions as enums
2. **Combination Generator** (`combination_generator.py`): Generates all combinations of dimensions
3. **Test Executor** (`test_executor.py`): Executes tests on combinations and records results
4. **Reporter** (`reporter.py`): Formats and displays test results

## Key Features

- ✅ Systematic exploration of dimension combinations (2-way, 3-way, N-way)
- ✅ Configurable sampling for large combination spaces
- ✅ Parallel test execution support
- ✅ Real-time progress reporting with callbacks
- ✅ Comprehensive test result analysis by dimension
- ✅ JSON export for integration with other tools
- ✅ Extensible test functions for custom validation logic

## Testing Philosophy

GrumpiMiner is built on the principle that **interactions matter**. A system may work perfectly when each dimension is tested in isolation, but fail when specific combinations occur. This framework ensures:

- All dimension pairs are tested (2-way combinations)
- Higher-order interactions are explored (3-way, 4-way, etc.)
- Edge cases in dimension interactions are discovered
- Results are tracked and analyzed by dimension

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Ollama Cloud Integration

GrumpiMiner integrates with Ollama Cloud service for AI-powered analysis and insights:

- 🤖 **Automated Code Analysis**: AI-powered code quality and architecture review
- 📊 **Intelligent Reporting**: Structured analysis with actionable recommendations
- 🔍 **Dimension Exploration**: AI-assisted dimension interaction discovery
- 📚 **Auto-Documentation**: Automated documentation generation and publishing

### Quick Setup

```bash
# Set environment variables
export OLLAMA_BASE_URL="https://api.ollama.cloud"  # or http://localhost:11434
export OLLAMA_API_KEY="your-api-key"  # if using cloud

# Run analysis
python scripts/ollama_analysis.py --model llama3.2:3b --analysis-type comprehensive
```

See [Ollama Integration Guide](docs/OLLAMA_INTEGRATION.md) for complete documentation.

## GitHub Actions Workflows

Automated workflows run on every push:

1. **Test Suite** (`.github/workflows/test.yml`): Comprehensive testing across Python versions
2. **Ollama Analysis** (`.github/workflows/ollama-analysis.yml`): AI-powered code analysis
3. **Documentation** (`.github/workflows/docs.yml`): Auto-generate and publish docs to GitHub Pages

## Documentation

Full documentation is available at: [https://grumpified-oggvct.github.io/GrumpiMiner](https://grumpified-oggvct.github.io/GrumpiMiner)

- [Vision Documents](docs/index.md): System vision and architecture
- [Ollama Integration](docs/OLLAMA_INTEGRATION.md): AI-powered features
- [Model Registry](docs/model-registry.md): Model specifications
- [Analysis Reports](docs/analysis-report.md): Latest AI analysis results

## License

This project is licensed under the MIT License - see the LICENSE file for details.
