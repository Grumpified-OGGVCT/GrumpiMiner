# Quick Start: Ollama Integration

This guide helps you get started with GrumpiMiner's Ollama Cloud integration in 5 minutes.

## Step 1: Choose Your Ollama Setup

### Option A: Ollama Cloud (Recommended for GitHub Actions)

1. Sign up at [Ollama Cloud](https://ollama.com/)
2. Get your API key from the dashboard
3. Set environment variables:
   ```bash
   export OLLAMA_BASE_URL="https://api.ollama.cloud"
   export OLLAMA_API_KEY="your-api-key-here"
   ```

### Option B: Local Ollama (For Development)

1. Install Ollama: https://ollama.com/download
2. Start Ollama service:
   ```bash
   ollama serve
   ```
3. Pull a model:
   ```bash
   ollama pull llama3.2:3b
   ```
4. Set environment variable:
   ```bash
   export OLLAMA_BASE_URL="http://localhost:11434"
   ```

## Step 2: Configure GitHub Actions (For CI/CD)

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:
   - Name: `OLLAMA_API_KEY`, Value: `your-api-key`
   - Name: `OLLAMA_BASE_URL`, Value: `https://api.ollama.cloud` (optional)

## Step 3: Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Grumpified-OGGVCT/GrumpiMiner.git
cd GrumpiMiner

# Install package
pip install -e .
```

## Step 4: Run Your First Analysis

### Using Python API

```python
from grumpi_miner.ollama_client import create_client

# Create client (uses environment variables)
client = create_client()

# Run a simple analysis
response = client.generate(
    model="llama3.2:3b",
    prompt="Explain the GrumpiMiner testing framework in 3 sentences.",
    system="You are a helpful technical documentation assistant."
)

print(response.content)
```

### Using Command Line

```bash
# Run comprehensive code analysis
python scripts/ollama_analysis.py \
    --model llama3.2:3b \
    --analysis-type comprehensive \
    --output docs/my-analysis.md

# View results
cat docs/my-analysis.md
```

## Step 5: Verify GitHub Actions

Push your code to trigger workflows:

```bash
git add .
git commit -m "Test Ollama integration"
git push
```

Check the **Actions** tab in GitHub to see:
- ✅ Test Suite running
- ✅ Ollama Analysis generating
- ✅ Documentation building

## Common Use Cases

### 1. Code Quality Analysis

```python
code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
"""

response = client.generate(
    model="deepseek-coder:6.7b",
    prompt=f"Review this code and suggest improvements:\n\n{code}",
    system="You are an expert code reviewer."
)
```

### 2. Structured Output (JSON Schema)

```python
schema = {
    "type": "object",
    "properties": {
        "issues": {
            "type": "array",
            "items": {"type": "string"}
        },
        "severity": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["issues", "severity"]
}

result = client.structured_output(
    model="llama3.2:3b",
    prompt="Analyze this codebase for security issues...",
    schema=schema
)

print(f"Found {len(result['issues'])} issues")
print(f"Severity: {result['severity']}")
```

### 3. Vision Analysis (Diagrams)

```python
response = client.vision_analyze(
    model="llava:13b",
    prompt="What does this architecture diagram show? Explain the components.",
    images=["docs/architecture.png"]
)

print(response.content)
```

### 4. Generate Embeddings

```python
# For semantic search or similarity matching
embedding = client.embeddings(
    model="nomic-embed-text",
    prompt="GrumpiMiner is a testing framework for dimension combinations"
)

print(f"Embedding dimension: {len(embedding)}")
```

## Available Models

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| `llama3.2:3b` | 3B | Quick analysis, general tasks | ⚡⚡⚡ |
| `llama3.2:7b` | 7B | Balanced quality/speed | ⚡⚡ |
| `deepseek-coder:6.7b` | 6.7B | Code analysis | ⚡⚡ |
| `codellama:13b` | 13B | Deep code understanding | ⚡ |
| `llava:13b` | 13B | Vision, diagrams | ⚡ |

## Troubleshooting

### "Connection refused"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Start Ollama
ollama serve
```

### "Model not found"

```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3.2:3b
```

### "Authentication failed"

```bash
# Verify API key
echo $OLLAMA_API_KEY

# Re-export if needed
export OLLAMA_API_KEY="your-actual-key"
```

## Next Steps

- 📚 Read [Full Integration Guide](OLLAMA_INTEGRATION.md)
- 🔍 Explore [Model Registry](model-registry.md)
- 🤖 Check [GitHub Workflows](.github/workflows/)
- 📊 View [Analysis Examples](../examples/)

## Getting Help

- **Documentation**: https://docs.ollama.com/
- **GitHub Issues**: https://github.com/Grumpified-OGGVCT/GrumpiMiner/issues
- **Ollama Discord**: https://discord.gg/ollama

---

**Ready to go!** Start analyzing your code with AI-powered insights. 🚀
