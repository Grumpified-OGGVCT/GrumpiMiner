"""
Dimension definitions for the GrumpiMiner system.
Each dimension represents a key aspect of complexity to be tested in combination.
"""

from enum import Enum
from typing import List, Dict, Any


class FormatVariation(Enum):
    """Format variations for content representation."""
    NATURAL_LANGUAGE = "natural_language"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    CODE = "code"
    LATEX = "latex"
    DIAGRAMS = "diagrams"
    HYBRID = "hybrid"


class StructuralArchitecture(Enum):
    """Structural architecture patterns."""
    FLAT = "flat"
    HIERARCHICAL = "hierarchical"
    GRAPH = "graph"
    TREE = "tree"
    MESH = "mesh"
    LAYERED = "layered"


class ModelOrchestration(Enum):
    """Model orchestration patterns."""
    SINGLE = "single"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    ENSEMBLE = "ensemble"
    CASCADING = "cascading"


class ContextRepresentation(Enum):
    """Context representation methods."""
    MINIMAL = "minimal"
    EXTENDED = "extended"
    CONTEXTUAL = "contextual"
    GLOBAL = "global"
    WINDOWED = "windowed"
    DYNAMIC = "dynamic"


class InstructionSemantics(Enum):
    """Instruction semantic patterns."""
    IMPERATIVE = "imperative"
    DECLARATIVE = "declarative"
    FUNCTIONAL = "functional"
    CONSTRAINT_BASED = "constraint_based"
    GOAL_ORIENTED = "goal_oriented"
    EXAMPLE_BASED = "example_based"


class VerificationProtocol(Enum):
    """Verification protocol types."""
    NONE = "none"
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    FORMAL = "formal"
    STATISTICAL = "statistical"
    HEURISTIC = "heuristic"


class MetaCognitiveScaffolding(Enum):
    """Meta-cognitive scaffolding levels."""
    NONE = "none"
    REFLECTION = "reflection"
    PLANNING = "planning"
    MONITORING = "monitoring"
    EVALUATION = "evaluation"
    ADAPTIVE = "adaptive"


class ConstraintArchitecture(Enum):
    """Constraint architecture types."""
    UNCONSTRAINED = "unconstrained"
    SOFT = "soft"
    HARD = "hard"
    ADAPTIVE = "adaptive"
    HIERARCHICAL = "hierarchical"
    NEGOTIABLE = "negotiable"


class CrossModalTranslation(Enum):
    """Cross-modal translation capabilities."""
    NONE = "none"
    TEXT_TO_CODE = "text_to_code"
    CODE_TO_TEXT = "code_to_text"
    DIAGRAM_TO_TEXT = "diagram_to_text"
    TEXT_TO_DIAGRAM = "text_to_diagram"
    MULTIMODAL = "multimodal"


class TemporalDynamics(Enum):
    """Temporal dynamics patterns."""
    STATIC = "static"
    SEQUENTIAL = "sequential"
    CONCURRENT = "concurrent"
    REAL_TIME = "real_time"
    ADAPTIVE = "adaptive"
    PREDICTIVE = "predictive"


# All dimension classes for iteration
DIMENSION_CLASSES = [
    FormatVariation,
    StructuralArchitecture,
    ModelOrchestration,
    ContextRepresentation,
    InstructionSemantics,
    VerificationProtocol,
    MetaCognitiveScaffolding,
    ConstraintArchitecture,
    CrossModalTranslation,
    TemporalDynamics,
]


def get_dimension_name(dimension_class: type) -> str:
    """Get the human-readable name of a dimension class."""
    names = {
        FormatVariation: "Format Variation",
        StructuralArchitecture: "Structural Architecture",
        ModelOrchestration: "Model Orchestration",
        ContextRepresentation: "Context Representation",
        InstructionSemantics: "Instruction Semantics",
        VerificationProtocol: "Verification Protocol",
        MetaCognitiveScaffolding: "Meta-Cognitive Scaffolding",
        ConstraintArchitecture: "Constraint Architecture",
        CrossModalTranslation: "Cross-Modal Translation",
        TemporalDynamics: "Temporal Dynamics",
    }
    return names.get(dimension_class, dimension_class.__name__)
