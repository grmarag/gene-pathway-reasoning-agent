import pytest
from fastapi.testclient import TestClient
from fastapi.responses import HTMLResponse
from src.ui.app import app, templates

# Define dummy classes to simulate the index and query engine.
class DummyQueryEngine:
    def query(self, question):
        return "dummy index context"

class DummyIndex:
    def as_query_engine(self):
        return DummyQueryEngine()

# Override the template rendering to avoid file dependencies.
@pytest.fixture(autouse=True)
def override_templates():
    def fake_template_response(template_name: str, context: dict, **kwargs):
        content = f"Template: {template_name}, context: {context}"
        return HTMLResponse(content=content)
    templates.TemplateResponse = fake_template_response

# Override heavy dependencies in the app namespace.
@pytest.fixture(autouse=True)
def override_heavy_dependencies(monkeypatch):
    # Patch the functions that were imported in app.py.
    monkeypatch.setattr("src.ui.app.get_combined_index", lambda: DummyIndex())
    monkeypatch.setattr("src.ui.app.get_gene_network", lambda: {})

# Define a dummy hypothesis generator.
async def fake_generate_hypothesis_from_question(question: str, **kwargs) -> str:
    return "This is a test hypothesis."

# Override the hypothesis generation function in the app's namespace.
@pytest.fixture(autouse=True)
def override_generate_hypothesis(monkeypatch):
    monkeypatch.setattr(
        "src.ui.app.generate_hypothesis_from_question",
        fake_generate_hypothesis_from_question,
    )

client = TestClient(app)

def test_read_root():
    """Test that GET / returns the expected HTML response."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Template: index.html" in response.text
    # The 'result' key should be empty on the root page.
    assert "'result': ''" in response.text

def test_query_endpoint():
    """Test that POST /query returns a response containing the dummy hypothesis and submitted question."""
    question_text = "What is gene involvement in disease?"
    response = client.post("/query", data={"question": question_text})
    assert response.status_code == 200
    # The dummy hypothesis is transformed by markdown into a paragraph tag.
    assert "<p>This is a test hypothesis.</p>" in response.text
    assert question_text in response.text