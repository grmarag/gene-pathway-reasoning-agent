import pytest
from unittest.mock import patch, AsyncMock
from src.services.hypothesis_generator import generate_hypothesis_from_question

@pytest.mark.asyncio
@patch("src.services.hypothesis_generator.LLMReasoningAgent")
@patch("src.services.hypothesis_generator.get_combined_index")
async def test_generate_hypothesis_from_question(mock_get_index, mock_agent_class):
    mock_query_engine = mock_get_index.return_value.as_query_engine.return_value
    mock_query_engine.query.return_value = "Indexed data context"
    
    mock_agent = mock_agent_class.return_value
    mock_agent.generate_hypothesis_async = AsyncMock(return_value="Hypothesis: gene X is related.")

    result = await generate_hypothesis_from_question("What gene is linked to Parkinson's?")
    
    assert "Hypothesis" in result