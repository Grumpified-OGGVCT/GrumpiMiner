#!/usr/bin/env python3
"""
Vision Documents Generator
===========================

Generates an index and documentation from the vision documents in grumpi_miner/
"""

import sys
from pathlib import Path
from datetime import datetime


def generate_vision_index():
    """Generate index page for vision documents"""
    grumpi_dir = Path(__file__).parent.parent / "grumpi_miner"
    docs_dir = Path(__file__).parent.parent / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Find vision documents
    vision_docs = [
        "360-DEGREE WORKFLOW COMPLEXITY MINING ENGINE",
        "RECURSIVE, ADAPTIVE, SELF-VALIDATING ULTIMATE CONVERGENT WORKFLOW MINING SYSTEM"
    ]
    
    # Generate index
    index_content = f"""# GrumpiMiner Vision & Architecture

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

## Overview

GrumpiMiner is a comprehensive testing framework for exploring complexity dimensions
and their interactions. This documentation covers the vision, architecture, and
implementation details.

## Vision Documents

"""
    
    # Add links to vision documents
    for doc_name in vision_docs:
        doc_path = grumpi_dir / doc_name
        if doc_path.exists():
            # Create sanitized filename
            safe_name = doc_name.replace(" ", "-").replace(",", "").lower()
            output_path = docs_dir / f"{safe_name}.md"
            
            # Copy content with markdown formatting
            with open(doc_path, "r") as f:
                content = f.read()
            
            with open(output_path, "w") as f:
                f.write(f"# {doc_name}\n\n")
                f.write(content)
            
            index_content += f"- [{doc_name}](./{safe_name}.md)\n"
    
    # Add model registry documentation
    index_content += "\n## Model Registry\n\n"
    index_content += "- [Model Registry](./model-registry.md) - Complete model specifications\n"
    
    # Write index
    with open(docs_dir / "index.md", "w") as f:
        f.write(index_content)
    
    print(f"✅ Generated vision documentation index in {docs_dir}/")


def generate_model_registry_docs():
    """Generate documentation for model registry"""
    docs_dir = Path(__file__).parent.parent / "docs"
    model_reg_path = Path(__file__).parent.parent / "grumpi_miner" / "model_registry.py"
    
    if not model_reg_path.exists():
        print("⚠️  Model registry not found")
        return
    
    # Read model registry docstring
    with open(model_reg_path, "r") as f:
        content = f.read()
    
    # Extract module docstring
    import ast
    tree = ast.parse(content)
    docstring = ast.get_docstring(tree) or "Model Registry Documentation"
    
    doc_content = f"""# Model Registry Documentation

{docstring}

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
"""
    
    with open(docs_dir / "model-registry.md", "w") as f:
        f.write(doc_content)
    
    print("✅ Generated model registry documentation")


def main():
    try:
        generate_vision_index()
        generate_model_registry_docs()
        print("✅ Documentation generation complete!")
        return 0
    except Exception as e:
        print(f"❌ Failed to generate documentation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
