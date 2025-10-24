"""
Tests for combination generator.
"""

import unittest
from grumpi_miner.combination_generator import (
    CombinationGenerator,
    DimensionCombination,
)
from grumpi_miner.dimensions import (
    FormatVariation,
    StructuralArchitecture,
    DIMENSION_CLASSES,
)


class TestDimensionCombination(unittest.TestCase):
    """Test DimensionCombination class."""
    
    def test_combination_creation(self):
        """Test creating a dimension combination."""
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
            "StructuralArchitecture": StructuralArchitecture.HIERARCHICAL,
        })
        self.assertEqual(len(combo.dimensions), 2)
    
    def test_combination_hash(self):
        """Test combination hash generation."""
        combo1 = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
            "StructuralArchitecture": StructuralArchitecture.HIERARCHICAL,
        })
        combo2 = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
            "StructuralArchitecture": StructuralArchitecture.HIERARCHICAL,
        })
        self.assertEqual(combo1.get_hash(), combo2.get_hash())
    
    def test_combination_string_representation(self):
        """Test string representation of combination."""
        combo = DimensionCombination(dimensions={
            "FormatVariation": FormatVariation.JSON,
        })
        str_repr = str(combo)
        self.assertIn("json", str_repr.lower())


class TestCombinationGenerator(unittest.TestCase):
    """Test CombinationGenerator class."""
    
    def test_generator_initialization(self):
        """Test initializing the generator."""
        gen = CombinationGenerator(min_dimensions=2, max_dimensions=5)
        self.assertEqual(gen.min_dimensions, 2)
        self.assertEqual(gen.max_dimensions, 5)
    
    def test_generate_dimension_pairs(self):
        """Test generating dimension pairs."""
        gen = CombinationGenerator()
        pairs = gen.generate_dimension_pairs()
        
        # Should have C(10, 2) = 45 pairs
        self.assertEqual(len(pairs), 45)
        
        # Each pair should have 2 elements
        for pair in pairs:
            self.assertEqual(len(pair), 2)
    
    def test_generate_dimension_groups(self):
        """Test generating dimension groups of specific size."""
        gen = CombinationGenerator()
        
        # Test 2-way combinations
        groups_2 = gen.generate_dimension_groups(2)
        self.assertEqual(len(groups_2), 45)  # C(10, 2)
        
        # Test 3-way combinations
        groups_3 = gen.generate_dimension_groups(3)
        self.assertEqual(len(groups_3), 120)  # C(10, 3)
    
    def test_generate_combinations_for_group(self):
        """Test generating value combinations for a dimension group."""
        gen = CombinationGenerator()
        group = (FormatVariation, StructuralArchitecture)
        
        combos = gen.generate_combinations_for_group(group)
        
        # Should generate combinations of all values
        format_count = len(list(FormatVariation))
        struct_count = len(list(StructuralArchitecture))
        expected_count = format_count * struct_count
        
        self.assertEqual(len(combos), expected_count)
    
    def test_generate_combinations_with_limit(self):
        """Test generating combinations with max_per_dimension limit."""
        gen = CombinationGenerator()
        group = (FormatVariation, StructuralArchitecture)
        
        combos = gen.generate_combinations_for_group(group, max_per_dimension=2)
        
        # Should generate only 2x2=4 combinations
        self.assertEqual(len(combos), 4)
    
    def test_generate_sample_combinations(self):
        """Test generating sample combinations."""
        gen = CombinationGenerator(min_dimensions=2, max_dimensions=3)
        samples = gen.generate_sample_combinations(samples_per_size=5)
        
        # Should have samples for 2-way and 3-way combinations
        self.assertIn(2, samples)
        self.assertIn(3, samples)
        
        # Each should have up to 5 samples
        self.assertLessEqual(len(samples[2]), 5)
        self.assertLessEqual(len(samples[3]), 5)
    
    def test_all_combinations_structure(self):
        """Test structure of all combinations output."""
        gen = CombinationGenerator(min_dimensions=2, max_dimensions=3)
        all_combos = gen.generate_all_combinations(max_per_dimension=1)
        
        # Should have entries for sizes 2 and 3
        self.assertIn(2, all_combos)
        self.assertIn(3, all_combos)
        
        # All combinations should be DimensionCombination instances
        for size, combos in all_combos.items():
            for combo in combos:
                self.assertIsInstance(combo, DimensionCombination)


class TestCombinationInteractions(unittest.TestCase):
    """Test that combinations properly test interactions between dimensions."""
    
    def test_two_way_interactions(self):
        """Test 2-way dimension interactions are generated."""
        gen = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        combos = gen.generate_all_combinations(max_per_dimension=1)
        
        # Verify we have 2-way combinations
        self.assertIn(2, combos)
        self.assertGreater(len(combos[2]), 0)
        
        # Each combination should have exactly 2 dimensions
        for combo in combos[2]:
            self.assertEqual(len(combo.dimensions), 2)
    
    def test_three_way_interactions(self):
        """Test 3-way dimension interactions are generated."""
        gen = CombinationGenerator(min_dimensions=3, max_dimensions=3)
        combos = gen.generate_all_combinations(max_per_dimension=1)
        
        # Verify we have 3-way combinations
        self.assertIn(3, combos)
        self.assertGreater(len(combos[3]), 0)
        
        # Each combination should have exactly 3 dimensions
        for combo in combos[3]:
            self.assertEqual(len(combo.dimensions), 3)
    
    def test_combinations_are_distinct(self):
        """Test that generated combinations are distinct."""
        gen = CombinationGenerator(min_dimensions=2, max_dimensions=2)
        combos = gen.generate_all_combinations(max_per_dimension=2)
        
        # Get hashes of all combinations
        hashes = [combo.get_hash() for combo in combos[2]]
        
        # All hashes should be unique
        self.assertEqual(len(hashes), len(set(hashes)))


if __name__ == '__main__':
    unittest.main()
