"""
Combination test generator for GrumpiMiner.
Generates test combinations across all dimensions.
"""

from itertools import combinations, product
from typing import List, Dict, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from .dimensions import DIMENSION_CLASSES, get_dimension_name


@dataclass
class DimensionCombination:
    """Represents a specific combination of dimension values."""
    dimensions: Dict[str, Enum]
    
    def __str__(self) -> str:
        return " + ".join([
            f"{get_dimension_name(type(v))}: {v.value}"
            for v in self.dimensions.values()
        ])
    
    def __repr__(self) -> str:
        return f"DimensionCombination({self.dimensions})"
    
    def get_hash(self) -> str:
        """Generate a unique hash for this combination."""
        parts = []
        for dim_class in DIMENSION_CLASSES:
            dim_name = dim_class.__name__
            if dim_name in self.dimensions:
                parts.append(f"{dim_name}:{self.dimensions[dim_name].value}")
        return "|".join(sorted(parts))


class CombinationGenerator:
    """Generates combinations of dimensions for testing."""
    
    def __init__(self, min_dimensions: int = 2, max_dimensions: int = None):
        """
        Initialize the combination generator.
        
        Args:
            min_dimensions: Minimum number of dimensions to combine (default: 2)
            max_dimensions: Maximum number of dimensions to combine (default: all)
        """
        self.min_dimensions = max(2, min_dimensions)  # At least 2 for combinations
        self.max_dimensions = max_dimensions or len(DIMENSION_CLASSES)
        self.max_dimensions = min(self.max_dimensions, len(DIMENSION_CLASSES))
    
    def generate_dimension_pairs(self) -> List[Tuple[type, type]]:
        """Generate all pairs of dimension classes."""
        return list(combinations(DIMENSION_CLASSES, 2))
    
    def generate_dimension_groups(self, size: int) -> List[Tuple[type, ...]]:
        """Generate all groups of dimension classes of a given size."""
        if size < 2 or size > len(DIMENSION_CLASSES):
            return []
        return list(combinations(DIMENSION_CLASSES, size))
    
    def generate_combinations_for_group(
        self, 
        dimension_group: Tuple[type, ...],
        max_per_dimension: int = None
    ) -> List[DimensionCombination]:
        """
        Generate all value combinations for a group of dimensions.
        
        Args:
            dimension_group: Tuple of dimension classes
            max_per_dimension: Maximum values to use per dimension (for sampling)
        
        Returns:
            List of DimensionCombination instances
        """
        # Get values for each dimension
        dimension_values = []
        for dim_class in dimension_group:
            values = list(dim_class)
            if max_per_dimension:
                values = values[:max_per_dimension]
            dimension_values.append([(dim_class.__name__, v) for v in values])
        
        # Generate all combinations
        combinations_list = []
        for combo in product(*dimension_values):
            dim_dict = {name: value for name, value in combo}
            combinations_list.append(DimensionCombination(dimensions=dim_dict))
        
        return combinations_list
    
    def generate_all_combinations(
        self,
        max_per_dimension: int = None,
        max_total_combinations: int = None
    ) -> Dict[int, List[DimensionCombination]]:
        """
        Generate all combinations across all dimension group sizes.
        
        Args:
            max_per_dimension: Maximum values to use per dimension
            max_total_combinations: Maximum total combinations to generate
        
        Returns:
            Dictionary mapping group size to list of combinations
        """
        results = {}
        total_count = 0
        
        for size in range(self.min_dimensions, self.max_dimensions + 1):
            results[size] = []
            dimension_groups = self.generate_dimension_groups(size)
            
            for group in dimension_groups:
                combos = self.generate_combinations_for_group(
                    group, 
                    max_per_dimension
                )
                results[size].extend(combos)
                total_count += len(combos)
                
                if max_total_combinations and total_count >= max_total_combinations:
                    return results
        
        return results
    
    def generate_sample_combinations(
        self,
        samples_per_size: int = 10
    ) -> Dict[int, List[DimensionCombination]]:
        """
        Generate a sample of combinations for each group size.
        
        Args:
            samples_per_size: Number of combinations to sample per group size
        
        Returns:
            Dictionary mapping group size to sampled combinations
        """
        import random
        
        results = {}
        for size in range(self.min_dimensions, self.max_dimensions + 1):
            all_combos = []
            dimension_groups = self.generate_dimension_groups(size)
            
            # Sample dimension groups first
            sampled_groups = random.sample(
                dimension_groups, 
                min(samples_per_size, len(dimension_groups))
            )
            
            for group in sampled_groups:
                # Take one value from each dimension in the group
                combos = self.generate_combinations_for_group(group, max_per_dimension=1)
                if combos:
                    all_combos.append(combos[0])
            
            results[size] = all_combos
        
        return results
