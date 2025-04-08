# Gene Pathway Reasoning Agent

## Overview

The **Gene Pathway Reasoning Agent** is a production-ready system that uses a Large Language Model (LLM) to generate biomedical hypotheses regarding gene involvement in specific diseases. It integrates data from KEGG (XML files) and Gene Ontology (GAF files) and employs network analysis to predict downstream gene interactions and their potential impact on disease pathways.

## Features

- **LLM-Powered Agent:** Uses the `GPT-4o-mini` model (via API) to generate evidence-based hypotheses.
- **Database-wide Integration:** Automatically indexes KEGG XML and GO GAF files (via LlamaIndex).
- **Directed Network Analysis:** Builds a directed gene interaction network (via NetworkX) to explore downstream effects.
- **Clean Architecture:** Modular, testable, and easily scalable structure.
- **FastAPI Web UI:** Interactive interface for user queries.
- **Docker Support:** Simplifies deployment across different environments.
- **Centralized Configuration:** All settings (file paths, LLM instructions, etc.) stored in a single config system.
- **Comprehensive Testing:** Includes unit and integration tests.

---

## Repository Structure

```plaintext
gene-pathway-reasoning-agent/
├── README.md
├── pyproject.toml
├── .env
├── Dockerfile
├── docs/
│   └── report.md
├── cache/
│   ├── combined_index.pkl
│   └── gene_network.pkl
├── data/
│   ├── kegg/
│   │   ├── hsa04930.xml
│   │   ├── hsa05010.xml
│   │   ├── hsa05012.xml
│   │   └── hsa05210.xml
│   └── go/
│       └── goa_human.gaf
├── src/
│   ├── config/
│   │   └── settings.py
│   ├── agent/
│   │   └── llm_agent.py
│   ├── data/
│   │   ├── models.py
│   │   ├── parser.py
│   │   └── indexer.py
│   ├── services/
│   │   └── hypothesis_generator.py
│   └── ui/
│       ├── app.py
│       └── templates/
│           └── index.html
└── tests/
    ├── test_parser.py
    ├── test_llm_agent.py
    └── test_integration.py
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gene-pathway-reasoning-agent.git
cd gene-pathway-reasoning-agent
```

### 2. Install Dependencies (Poetry)

Make sure you have Python 3.12+ installed:

```bash
poetry install
eval $(poetry env activate)
```

### 3. Configure Environment

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application (Local)

```bash
uvicorn src.ui.app:app --reload
```

Access at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Docker Deployment

- **Build the Docker image**:

  ```bash
  docker build -t gene-pathway-reasoning-agent .
  ```

- **Run the container**:

  ```bash
  docker run -d -p 8000:8000 gene-pathway-reasoning-agent
  ```

---

## How It Works

1. **Data Parsing & Indexing**  
   - KEGG XML and GO GAF files in `data/` are parsed by `parser.py`.  
   - The parsed data is combined into a searchable index (`create_combined_index`) in `indexer.py`.

2. **Network Analysis**  
   - A directed gene interaction network is built from KEGG data (`build_gene_network`) using NetworkX.  
   - The network is cached for fast access and used to trace downstream interactions.

3. **Hypothesis Generation**  
   - The LLM agent (`llm_agent.py`) combines the indexed data and network analysis results to propose hypotheses.  
   - Single-gene and multi-gene queries are supported.

4. **Web UI**  
   - A FastAPI app (`app.py`) provides a user interface for querying gene pathways and displaying model outputs.

---

## Testing

To run all tests:

```bash
poetry run pytest
```

---

## Documentation

A more detailed report on the system architecture, data handling, and usage examples is available in [`docs/report.md`](docs/report.md).

---

## License

This project is available under the [MIT License](LICENSE).