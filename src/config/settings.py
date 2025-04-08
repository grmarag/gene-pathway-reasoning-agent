from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings defined via environment variables.

    Attributes:
        openai_api_key (str): API key for OpenAI services.
        llm_prompt_instructions (str): Prompt instructions for the language model.
        model_name (str): The name of the language model to use.
        kegg_data_dir (Path): Path to the directory containing KEGG data.
        go_data_dir (Path): Path to the directory containing Gene Ontology data.
    """
    model_config = SettingsConfigDict(env_file=".env")
    openai_api_key: str
    llm_prompt_instructions: str = (
        "You are an LLM that generates biomedical hypotheses regarding gene involvement in diseases based on integrated KEGG and Gene Ontology data. "
        "Consider both the aggregated database context and downstream gene interactions computed via network analysis in your reasoning. "
        "Provide concise, evidence-based conclusions."
    )
    model_name: str = "gpt-4o-mini"
    kegg_data_dir: Path = Path("data") / "kegg"
    go_data_dir: Path = Path("data") / "go"

settings = Settings()