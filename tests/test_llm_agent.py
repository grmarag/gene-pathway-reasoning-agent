import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import openai

# Ensure that openai.error exists (if not, create a dummy version).
if not hasattr(openai, "error"):
    openai.error = type("dummy", (), {"OpenAIError": Exception})

from src.agent.llm_agent import LLMReasoningAgent

@pytest.mark.asyncio
async def test_generate_hypothesis_async():
    with patch("src.agent.llm_agent.AsyncOpenAI") as mock_async_openai:
        # Configure the mock instance.
        mock_instance = mock_async_openai.return_value
        # Create a dummy async response with the expected structure.
        dummy_response = AsyncMock()
        dummy_message = AsyncMock()
        dummy_message.content = "Hypothesis: gene X is involved"
        dummy_choice = AsyncMock()
        dummy_choice.message = dummy_message
        dummy_response.choices = [dummy_choice]
        # Patch the async create method so that it returns the dummy response.
        mock_instance.chat.completions.create = AsyncMock(return_value=dummy_response)
        
        agent = LLMReasoningAgent()
        result = await agent.generate_hypothesis_async(
            "What genes are involved in Alzheimer's?", "Context about AD"
        )
        assert "gene X is involved" in result