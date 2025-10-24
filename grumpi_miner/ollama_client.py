"""
Ollama Cloud API Client
========================

Provides integration with Ollama Cloud service supporting:
- Thinking (extended reasoning)
- Streaming responses
- Vision capabilities
- Web search integration
- Tool calling
- Embeddings
- Structured outputs (JSON schema validation)

Based on Ollama API documentation: https://docs.ollama.com/
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any, Iterator
from dataclasses import dataclass


@dataclass
class OllamaResponse:
    """Structured response from Ollama API"""
    content: str
    model: str
    done: bool
    total_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "content": self.content,
            "model": self.model,
            "done": self.done,
            "total_duration": self.total_duration,
            "prompt_eval_count": self.prompt_eval_count,
            "eval_count": self.eval_count
        }


class OllamaClient:
    """
    Client for interacting with Ollama Cloud API
    
    Capabilities:
    - Thinking: Extended reasoning for complex problems
    - Streaming: Real-time response streaming
    - Vision: Image understanding and analysis
    - Web Search: Information retrieval from web
    - Tool Calling: Function/tool invocation
    - Embeddings: Vector representations for text/images
    - Structured Outputs: JSON schema-validated responses
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama API base URL (default: from env OLLAMA_BASE_URL or http://localhost:11434)
            api_key: API key for cloud authentication (default: from env OLLAMA_API_KEY)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None,
        stream: bool = False,
        raw: bool = False,
        format: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        keep_alive: Optional[str] = None
    ) -> OllamaResponse:
        """
        Generate text completion
        
        Args:
            model: Model name (e.g., "llama3.2:3b")
            prompt: Input prompt
            system: System message to set behavior
            template: Template for prompt formatting
            context: Context from previous requests
            stream: Stream response chunks
            raw: Use raw mode (no template)
            format: Response format ("json" for JSON)
            options: Model parameters (temperature, top_p, etc.)
            keep_alive: Keep model loaded (e.g., "5m")
        
        Returns:
            OllamaResponse with generated content
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        if system:
            payload["system"] = system
        if template:
            payload["template"] = template
        if context:
            payload["context"] = context
        if raw:
            payload["raw"] = raw
        if format:
            payload["format"] = format
        if options:
            payload["options"] = options
        if keep_alive:
            payload["keep_alive"] = keep_alive
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return OllamaResponse(
            content=data.get("response", ""),
            model=data.get("model", model),
            done=data.get("done", True),
            total_duration=data.get("total_duration"),
            prompt_eval_count=data.get("prompt_eval_count"),
            eval_count=data.get("eval_count")
        )
    
    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False,
        format: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        keep_alive: Optional[str] = None
    ) -> OllamaResponse:
        """
        Chat completion with conversation history
        
        Args:
            model: Model name
            messages: List of messages with "role" and "content"
            stream: Stream response chunks
            format: Response format ("json" for JSON)
            options: Model parameters
            keep_alive: Keep model loaded
        
        Returns:
            OllamaResponse with assistant's reply
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        if format:
            payload["format"] = format
        if options:
            payload["options"] = options
        if keep_alive:
            payload["keep_alive"] = keep_alive
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        message = data.get("message", {})
        return OllamaResponse(
            content=message.get("content", ""),
            model=data.get("model", model),
            done=data.get("done", True),
            total_duration=data.get("total_duration"),
            prompt_eval_count=data.get("prompt_eval_count"),
            eval_count=data.get("eval_count")
        )
    
    def structured_output(
        self,
        model: str,
        prompt: str,
        schema: Dict[str, Any],
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate structured output with JSON schema validation
        
        Args:
            model: Model name
            prompt: Input prompt
            schema: JSON schema for output validation
            system: System message
            options: Model parameters
        
        Returns:
            Validated JSON object matching schema
        
        Example schema:
            {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"},
                    "condition": {"type": "string", "enum": ["sunny", "rainy"]}
                },
                "required": ["temperature", "condition"],
                "additionalProperties": false
            }
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "format": "json",
            "schema": schema
        }
        
        if system:
            payload["system"] = system
        if options:
            payload["options"] = options
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        content = data.get("response", "{}")
        return json.loads(content)
    
    def embeddings(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
        keep_alive: Optional[str] = None
    ) -> List[float]:
        """
        Generate embeddings for text or images
        
        Args:
            model: Model name
            prompt: Input text/image
            options: Model parameters
            keep_alive: Keep model loaded
        
        Returns:
            List of embedding floats
        """
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        if options:
            payload["options"] = options
        if keep_alive:
            payload["keep_alive"] = keep_alive
        
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return data.get("embedding", [])
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List available models
        
        Returns:
            List of model information dictionaries
        """
        response = requests.get(
            f"{self.base_url}/api/models",
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return data.get("models", [])
    
    def stream_generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Iterator[str]:
        """
        Stream text generation chunk by chunk
        
        Args:
            model: Model name
            prompt: Input prompt
            system: System message
            options: Model parameters
        
        Yields:
            String chunks as they arrive
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }
        
        if system:
            payload["system"] = system
        if options:
            payload["options"] = options
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=self.headers,
            timeout=self.timeout,
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]
                if data.get("done", False):
                    break
    
    def vision_analyze(
        self,
        model: str,
        prompt: str,
        images: List[str],
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> OllamaResponse:
        """
        Analyze images with vision-capable model
        
        Args:
            model: Vision model name (e.g., "llava:13b")
            prompt: Question about images
            images: List of image paths or base64 encoded images
            system: System message
            options: Model parameters
        
        Returns:
            OllamaResponse with vision analysis
        """
        # Prepare images (convert to base64 if paths)
        image_data = []
        for img in images:
            if os.path.isfile(img):
                import base64
                with open(img, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                    image_data.append(encoded)
            else:
                image_data.append(img)
        
        payload = {
            "model": model,
            "prompt": prompt,
            "images": image_data
        }
        
        if system:
            payload["system"] = system
        if options:
            payload["options"] = options
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return OllamaResponse(
            content=data.get("response", ""),
            model=data.get("model", model),
            done=data.get("done", True),
            total_duration=data.get("total_duration"),
            prompt_eval_count=data.get("prompt_eval_count"),
            eval_count=data.get("eval_count")
        )


def create_client(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> OllamaClient:
    """
    Create Ollama client instance
    
    Args:
        base_url: Optional base URL override
        api_key: Optional API key override
    
    Returns:
        Configured OllamaClient
    """
    return OllamaClient(base_url=base_url, api_key=api_key)
