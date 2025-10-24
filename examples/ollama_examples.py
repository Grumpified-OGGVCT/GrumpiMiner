#!/usr/bin/env python3
"""
Ollama Integration Examples - Demonstrating all capabilities
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from grumpi_miner.ollama_client import create_client


def example_basic():
    """Basic text generation"""
    print("\n=== Example 1: Basic Generation ===")
    client = create_client()
    
    response = client.generate(
        model="llama3.2:3b",
        prompt="Explain GrumpiMiner in 3 sentences.",
        system="You are a technical documentation assistant."
    )
    
    print(f"Response: {response.content}")


def example_structured():
    """Structured output with JSON schema"""
    print("\n=== Example 2: Structured Output ===")
    client = create_client()
    
    schema = {
        "type": "object",
        "properties": {
            "quality": {"type": "string", "enum": ["excellent", "good", "fair"]},
            "issues": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["quality", "issues"]
    }
    
    result = client.structured_output(
        model="llama3.2:3b",
        prompt="Review this code: def add(a,b): return a+b",
        schema=schema
    )
    
    print(json.dumps(result, indent=2))


def example_streaming():
    """Streaming responses"""
    print("\n=== Example 3: Streaming ===")
    client = create_client()
    
    for chunk in client.stream_generate(
        model="llama3.2:3b",
        prompt="Describe GrumpiMiner's architecture."
    ):
        print(chunk, end="", flush=True)
    print()


def main():
    print("GrumpiMiner + Ollama Examples")
    try:
        example_basic()
        example_structured()
        example_streaming()
        print("\n✅ All examples completed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Ollama is running and llama3.2:3b is available")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
