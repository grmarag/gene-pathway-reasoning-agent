import threading
import concurrent.futures
import nltk
from math import ceil
from pathlib import Path
from typing import List, Optional, Dict

from llama_index.core import (
    Document,
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.readers.base import BaseReader

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords
_ = stopwords.words("english")

class PlainTextReader(BaseReader):
    """
    A reader for plain text files with special handling for large GAF files.

    Methods:
        load_data(file: Path, extra_info: Optional[Dict] = None) -> List[Document]:
            Reads file data and returns a list of Document objects.
    """

    def load_data(self, file: Path, extra_info: Optional[Dict] = None) -> List[Document]:
        """
        Load data from a file and return a list of Document objects.

        Args:
            file (Path): The file to load.
            extra_info (Optional[Dict]): Additional information to associate with the document.

        Returns:
            List[Document]: A list of documents containing the file's content.
        """
        extra_info = extra_info or {"file_path": str(file)}
        # Use streamlined (streaming) file reading for large GAF files.
        if file.suffix.lower() == ".gaf":
            documents = []
            chunk_lines = []
            chunk_line_count = 10000
            with open(file, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    chunk_lines.append(line)
                    if (i + 1) % chunk_line_count == 0:
                        documents.append(Document(text="".join(chunk_lines), extra_info=extra_info))
                        chunk_lines = []
                if chunk_lines:
                    documents.append(Document(text="".join(chunk_lines), extra_info=extra_info))
            return documents
        else:
            # For smaller files, read the entire file at once.
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
            return [Document(text=text, extra_info=extra_info)]

def create_combined_index(kegg_dir: Path, go_dir: Path, thread_count: int = 4) -> VectorStoreIndex:
    """
    Create a combined index from KEGG and Gene Ontology documents.

    Args:
        kegg_dir (Path): Directory containing KEGG XML files.
        go_dir (Path): Directory containing Gene Ontology GAF files.
        thread_count (int): Number of threads to use for parallel processing.

    Returns:
        VectorStoreIndex: An index created from the combined documents.
    """
    kegg_reader = SimpleDirectoryReader(
        str(kegg_dir),
        recursive=False,
        file_extractor={".xml": PlainTextReader()}
    )
    kegg_docs = kegg_reader.load_data()
    go_reader = SimpleDirectoryReader(
        str(go_dir),
        recursive=False,
        file_extractor={".gaf": PlainTextReader()}
    )
    go_docs = go_reader.load_data()

    # Function to split a document into smaller chunks.
    def split_doc(doc: Document) -> List[Document]:
        """
        Split a document into smaller chunks for more efficient indexing.

        Args:
            doc (Document): The document to split.

        Returns:
            List[Document]: A list of document chunks.
        """
        # Force stopwords to load in this thread to avoid lazy loader issues.
        from nltk.corpus import stopwords
        _ = stopwords.words("english")
        # Create a local SentenceSplitter instance to avoid shared state issues.
        local_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        chunks = local_splitter.split_text(doc.text)
        return [Document(text=chunk, extra_info=doc.extra_info) for chunk in chunks]

    split_go_docs = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(split_doc, go_docs)
        for doc_chunks in results:
            split_go_docs.extend(doc_chunks)

    combined_docs = kegg_docs + split_go_docs
    node_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = node_splitter.get_nodes_from_documents(combined_docs)
    storage_context = StorageContext.from_defaults()

    def process_chunk(chunk_nodes, chunk_id):
        """
        Process a chunk of nodes to build part of the vector store index.
        
        Args:
            chunk_nodes: List of nodes in the chunk.
            chunk_id: Identifier for the current chunk (for logging or debugging purposes).
        """
        VectorStoreIndex(chunk_nodes, storage_context=storage_context)

    total_nodes = len(nodes)
    chunk_size = ceil(total_nodes / thread_count)
    threads = []
    
    for i in range(thread_count):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_nodes)
        chunk_nodes = nodes[start_idx:end_idx]
        thread = threading.Thread(target=process_chunk, args=(chunk_nodes, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    final_index = VectorStoreIndex([], storage_context=storage_context)
    return final_index