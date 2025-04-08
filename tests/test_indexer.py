from pathlib import Path
from src.data.indexer import PlainTextReader

def test_plain_text_reader_non_gaf(tmp_path: Path):
    # Create a temporary text file (non .gaf).
    file_path = tmp_path / "test.txt"
    file_path.write_text("This is a test.")
    reader = PlainTextReader()
    docs = reader.load_data(file_path)
    # Expect one document with the file's contents.
    assert len(docs) == 1
    assert "This is a test." in docs[0].text

def test_plain_text_reader_gaf(tmp_path: Path):
    # Create a temporary .gaf file with more lines than the chunk threshold.
    file_path = tmp_path / "test.gaf"
    # Assuming chunk_line_count in your code is 10,000.
    content = "\n".join(["line"] * 15000)
    file_path.write_text(content)
    reader = PlainTextReader()
    docs = reader.load_data(file_path)
    # Should split into two chunks/documents.
    assert len(docs) == 2