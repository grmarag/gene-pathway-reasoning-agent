import tempfile
from pathlib import Path
import networkx as nx
import pandas as pd
from src.data.parser import parse_kegg_xml, parse_gaf, build_gene_network
from src.data.models import Pathway

def test_parse_kegg_xml(tmp_path: Path):
    xml_content = '''<pathway name="path:00010" number="00010" title="Glycolysis / Gluconeogenesis">
      <entry type="gene" name="gene:GeneA gene:AliasA"/>
      <entry type="compound" name="C00031"/>
    </pathway>'''
    file_path = tmp_path / "test.xml"
    file_path.write_text(xml_content)
    pathway: Pathway = parse_kegg_xml(str(file_path))
    assert pathway.id == "00010"
    assert pathway.title == "Glycolysis / Gluconeogenesis"
    assert len(pathway.genes) == 1
    assert pathway.genes[0].id == "GeneA"
    assert pathway.genes[0].aliases == ["AliasA"]
    assert len(pathway.compounds) == 1

def test_build_gene_network(tmp_path: Path):
    xml_content = '''<pathway name="path:00010" number="00010" title="Test Pathway">
      <entry id="1" type="gene" name="gene:GeneA"/>
      <entry id="2" type="gene" name="gene:GeneB"/>
      <relation entry1="1" entry2="2" type="activation"/>
    </pathway>'''
    file_path = tmp_path / "test_network.xml"
    file_path.write_text(xml_content)
    G: nx.DiGraph = build_gene_network(str(file_path))
    assert isinstance(G, nx.DiGraph)
    # Check that both genes are present.
    assert "GeneA" in G.nodes
    assert "GeneB" in G.nodes
    # Verify the edge from GeneA to GeneB exists.
    assert ("GeneA", "GeneB") in G.edges

def test_parse_gaf(tmp_path: Path):
    gaf_content = """! This is a comment line
col1\tcol2\tcol3
a\tb\tc
d\te\tf
"""
    file_path = tmp_path / "test.gaf"
    file_path.write_text(gaf_content)
    df: pd.DataFrame = parse_gaf(str(file_path))
    # Since comment lines are skipped and header is not explicitly parsed,
    # we expect three rows (including the header row) and three columns.
    assert df.shape == (3, 3)