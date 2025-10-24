"""
Tests for dimension definitions and utilities.
"""

import unittest
from grumpi_miner.dimensions import (
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
    DIMENSION_CLASSES,
    get_dimension_name,
)


class TestDimensions(unittest.TestCase):
    """Test dimension definitions."""
    
    def test_all_dimensions_defined(self):
        """Test that all 10 dimensions are defined."""
        self.assertEqual(len(DIMENSION_CLASSES), 10)
    
    def test_format_variation_values(self):
        """Test FormatVariation enum has expected values."""
        expected_values = {
            "natural_language", "xml", "json", "yaml", 
            "code", "latex", "diagrams", "hybrid"
        }
        actual_values = {v.value for v in FormatVariation}
        self.assertEqual(actual_values, expected_values)
    
    def test_structural_architecture_values(self):
        """Test StructuralArchitecture enum has values."""
        self.assertGreater(len(list(StructuralArchitecture)), 0)
    
    def test_all_dimension_classes_have_values(self):
        """Test that all dimension classes have at least one value."""
        for dim_class in DIMENSION_CLASSES:
            with self.subTest(dimension=dim_class.__name__):
                values = list(dim_class)
                self.assertGreater(len(values), 0)
    
    def test_dimension_name_retrieval(self):
        """Test get_dimension_name function."""
        name = get_dimension_name(FormatVariation)
        self.assertEqual(name, "Format Variation")
        
        name = get_dimension_name(TemporalDynamics)
        self.assertEqual(name, "Temporal Dynamics")
    
    def test_dimension_values_are_unique(self):
        """Test that dimension values within each class are unique."""
        for dim_class in DIMENSION_CLASSES:
            with self.subTest(dimension=dim_class.__name__):
                values = [v.value for v in dim_class]
                self.assertEqual(len(values), len(set(values)))


if __name__ == '__main__':
    unittest.main()
