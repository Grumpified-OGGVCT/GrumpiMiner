# Ollama Cloud Integration

GrumpiMiner integrates with [Ollama Cloud](https://docs.ollama.com/) to provide AI-powered code analysis, automated testing insights, and intelligent dimension exploration.

## Features

### Supported Ollama Capabilities

- ✅ **Thinking**: Extended reasoning for complex analysis
- ✅ **Streaming**: Real-time response streaming
- ✅ **Vision**: Image and diagram analysis
- ✅ **Web Search**: Information retrieval
- ✅ **Tool Calling**: Function invocation
- ✅ **Embeddings**: Vector representations
- ✅ **Structured Outputs**: JSON schema validation

## Setup

### 1. Get Ollama Access

```bash
# Option A: Use Ollama Cloud (requires API key)
export OLLAMA_BASE_URL="https://api.ollama.cloud"
export OLLAMA_API_KEY="your-api-key-here"

# Option B: Run Ollama locally
# Download from https://ollama.com/download
ollama serve
export OLLAMA_BASE_URL="http://localhost:11434"
```

### 2. Configure GitHub Actions

Add the following secrets to your GitHub repository:

- `OLLAMA_BASE_URL`: Your Ollama API endpoint
- `OLLAMA_API_KEY`: Your API key (if using cloud)

Go to: `Settings → Secrets and variables → Actions → New repository secret`

### 3. Install Dependencies

```bash
pip install -e .
pip install requests  # For Ollama API calls
```

## Usage

### Python API

```python
from grumpi_miner.ollama_client import create_client

# Create client (uses env vars)
client = create_client()

# Generate text
response = client.generate(
    model="llama3.2:3b",
    prompt="Analyze this code for potential issues..."
)
print(response.content)

# Structured output with JSON schema
schema = {
    "type": "object",
    "properties": {
        "issues": {"type": "array", "items": {"type": "string"}},
        "severity": {"type": "string", "enum": ["low", "medium", "high"]}
    },
    "required": ["issues", "severity"]
}

result = client.structured_output(
    model="llama3.2:3b",
    prompt="Find code issues...",
    schema=schema
)
print(result)  # Guaranteed to match schema

# Vision analysis
response = client.vision_analyze(
    model="llava:13b",
    prompt="What does this diagram show?",
    images=["diagram.png"]
)

# Embeddings
embedding = client.embeddings(
    model="nomic-embed-text",
    prompt="Code quality analysis"
)
```

### Command Line

```bash
# Run code analysis
python scripts/ollama_analysis.py \
    --model llama3.2:3b \
    --analysis-type comprehensive \
    --output docs/analysis-report.md

# Analysis types:
#   - comprehensive: Full codebase review
#   - dimensions: Dimension interaction analysis
#   - testing: Test quality analysis
#   - architecture: Architecture review
```

### GitHub Actions

The repository includes automated workflows:

#### 1. Test Suite (`.github/workflows/test.yml`)
Runs on every push/PR to validate code quality.

#### 2. Ollama Analysis (`.github/workflows/ollama-analysis.yml`)
AI-powered code analysis that:
- Analyzes code quality and patterns
- Identifies potential issues
- Suggests improvements
- Generates markdown reports in `docs/`

Trigger manually with custom model:
```bash
# Via GitHub UI: Actions → Ollama-Powered Analysis → Run workflow
# Select model and analysis type
```

#### 3. Documentation (`.github/workflows/docs.yml`)
Automatically generates and publishes documentation to GitHub Pages.

## Available Models

Common models for code analysis:

| Model | Size | Best For |
|-------|------|----------|
| `llama3.2:3b` | 3B | Fast analysis, general code review |
| `llama3.2:7b` | 7B | Balanced quality and speed |
| `deepseek-coder:6.7b` | 6.7B | Code-specific analysis |
| `codellama:13b` | 13B | Deep code understanding |
| `llava:13b` | 13B | Diagram and visualization analysis |

See [Ollama Model Library](https://ollama.com/library) for all models.

## Model Registry Integration

The `model_registry.py` provides detailed specifications for 7 Ollama Cloud models:

```python
from grumpi_miner.model_registry import MODEL_REGISTRY, get_model_spec

# Get model info
spec = get_model_spec("qwen3-vl:235b-cloud")
print(spec.primary_capabilities)  # [VISION, MULTIMODAL, ...]
print(spec.optimal_personas)      # ["VISUAL_ANALYST", ...]
print(spec.benchmarks)            # BenchmarkScores(...)
```

Models include:
- **Qwen3-VL**: Vision specialist
- **Qwen3-Coder**: Coding specialist  
- **DeepSeek-V3.1**: Reasoning engine
- **Kimi-K2**: Agentic research
- **GPT-OSS 120B**: Chain-of-thought
- **GPT-OSS 20B**: Fast validation
- **GLM-4.6**: Alternative reasoning

## Examples

### Example 1: Code Quality Analysis

```python
from grumpi_miner.ollama_client import create_client

client = create_client()

code = """
def process_data(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result
"""

response = client.generate(
    model="deepseek-coder:6.7b",
    prompt=f"Review this code and suggest improvements:\n\n{code}",
    system="You are an expert code reviewer. Provide specific, actionable feedback."
)

print(response.content)
```

### Example 2: Structured Test Results

```python
schema = {
    "type": "object",
    "properties": {
        "test_name": {"type": "string"},
        "passed": {"type": "boolean"},
        "issues_found": {
            "type": "array",
            "items": {"type": "string"}
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["test_name", "passed"],
    "additionalProperties": false
}

result = client.structured_output(
    model="llama3.2:3b",
    prompt="Analyze this test result and extract key information...",
    schema=schema
)

# Result is guaranteed to match schema
assert "test_name" in result
assert "passed" in result
```

### Example 3: Streaming Analysis

```python
for chunk in client.stream_generate(
    model="llama3.2:3b",
    prompt="Explain the GrumpiMiner architecture in detail..."
):
    print(chunk, end="", flush=True)
```

## Troubleshooting

### "Connection refused" Error

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not, start Ollama
ollama serve
```

### Authentication Error

```bash
# Verify API key is set
echo $OLLAMA_API_KEY

# Re-export if needed
export OLLAMA_API_KEY="your-key"
```

### Model Not Found

```bash
# List available models
curl http://localhost:11434/api/models

# Pull a specific model
ollama pull llama3.2:3b
```

## Resources

- [Ollama Documentation](https://docs.ollama.com/)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Model Library](https://ollama.com/library)
- [Structured Outputs Guide](https://docs.ollama.com/capabilities/structured-outputs)

## Contributing

Contributions to improve Ollama integration are welcome! Areas for enhancement:

- Additional analysis types
- More sophisticated prompts
- Integration with additional Ollama features
- Performance optimizations

See `CONTRIBUTING.md` for guidelines.
