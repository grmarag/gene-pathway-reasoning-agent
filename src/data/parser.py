import xml.etree.ElementTree as ET
from .models import Pathway, Gene

def parse_kegg_xml(file_path: str) -> Pathway:
    """
    Parse a KEGG XML file to extract pathway information including genes and compounds.

    Args:
        file_path (str): Path to the KEGG XML file.

    Returns:
        Pathway: A Pathway object containing the parsed data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    pathway_id = root.attrib.get('name', '').split(":")[-1]
    pathway_number = root.attrib.get('number', '')
    title = root.attrib.get('title', '')
    
    genes = []
    compounds = []
    for entry in root.findall('entry'):
        entry_type = entry.attrib.get('type')
        if entry_type == "gene":
            # The 'name' attribute contains gene IDs and aliases separated by space.
            gene_info = entry.attrib.get('name', '')
            parts = gene_info.split()
            gene = Gene(
                id=parts[0].split(":")[-1],
                name=parts[0],
                aliases=[p.split(":")[-1] for p in parts[1:]]
            )
            genes.append(gene)
        elif entry_type == "compound":
            compound = entry.attrib.get('name', '')
            compounds.append(compound)
    return Pathway(id=pathway_id, number=pathway_number, title=title, genes=genes, compounds=compounds)

def parse_gaf(file_path: str):
    """
    Parse a Gene Association File (GAF) and return its contents as a DataFrame.

    Args:
        file_path (str): Path to the GAF file.

    Returns:
        pandas.DataFrame: A DataFrame containing the parsed data.
    """
    import pandas as pd
    df = pd.read_csv(file_path, sep='\t', comment='!', header=None)
    return df

def build_gene_network(file_path: str):
    """
    Build a gene interaction network from a KEGG XML file.

    Args:
        file_path (str): Path to the KEGG XML file.

    Returns:
        networkx.DiGraph: A directed graph representing gene interactions.
    """
    import networkx as nx
    tree = ET.parse(file_path)
    root = tree.getroot()
    G = nx.DiGraph()
    mapping = {}
    # Add nodes for gene entries.
    for entry in root.findall('entry'):
        if entry.attrib.get('type') == "gene":
            gene_info = entry.attrib.get('name', '')
            parts = gene_info.split()
            gene_id = parts[0].split(":")[-1]
            G.add_node(gene_id)
            mapping[entry.attrib.get('id')] = gene_id
    # Add edges based on relation tags.
    for relation in root.findall('relation'):
        entry1 = relation.attrib.get('entry1')
        entry2 = relation.attrib.get('entry2')
        if entry1 and entry2:
            gene1 = mapping.get(entry1)
            gene2 = mapping.get(entry2)
            if gene1 and gene2:
                G.add_edge(gene1, gene2, type=relation.attrib.get('type'))
    return G