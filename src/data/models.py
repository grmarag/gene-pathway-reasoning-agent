from dataclasses import dataclass, field
from typing import List

@dataclass
class Gene:
    """
    Represents a gene with an identifier, name, and possible aliases.

    Attributes:
        id (str): Unique identifier for the gene.
        name (str): The gene's primary name.
        aliases (List[str]): Alternative names or identifiers for the gene.
    """
    id: str
    name: str
    aliases: List[str] = field(default_factory=list)

@dataclass
class Pathway:
    """
    Represents a biological pathway including related genes and compounds.

    Attributes:
        id (str): Unique identifier for the pathway.
        number (str): Pathway number.
        title (str): Title or name of the pathway.
        genes (List[Gene]): A list of genes associated with the pathway.
        compounds (List[str]): A list of compounds involved in the pathway.
    """
    id: str
    number: str
    title: str
    genes: List[Gene] = field(default_factory=list)
    compounds: List[str] = field(default_factory=list)