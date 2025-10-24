# Model Registry Documentation

Model Registry - Complete specifications for all 7 cloud models
Defines capabilities, use cases, optimal persona assignments, and verified benchmarks

## Source Code

See `grumpi_miner/model_registry.py` for the complete implementation.

## Usage

```python
from grumpi_miner.model_registry import MODEL_REGISTRY, get_model_spec

# Get a specific model
spec = get_model_spec("qwen3-vl:235b-cloud")
print(spec.display_name)
print(spec.primary_capabilities)
```

## Model Specifications

The registry contains detailed specifications for all 7 Ollama Cloud models, including:

- Benchmarks and performance metrics
- Optimal use cases
- Architectural innovations
- Deep-dive profiling dimensions

For complete details, see the source code.
