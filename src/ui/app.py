import markdown
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
from src.services.hypothesis_generator import (
    generate_hypothesis_from_question,
    get_combined_index,
    get_gene_network,
)

app = FastAPI()
templates = Jinja2Templates(directory="src/ui/templates")

@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup event to initialize the combined index and gene network in background threads.
    """
    await asyncio.gather(
        asyncio.to_thread(get_combined_index),
        asyncio.to_thread(get_gene_network)
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Render the main page with an empty result field.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        HTMLResponse: The rendered HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": ""})

@app.post("/query", response_class=HTMLResponse)
async def query(request: Request, question: str = Form(...)):
    """
    Process a user query submitted via a form, generate a hypothesis, and render the result.

    Args:
        request (Request): The incoming HTTP request.
        question (str): The user's query from the form.

    Returns:
        HTMLResponse: The rendered HTML page displaying the generated hypothesis.
    """
    result = await generate_hypothesis_from_question(question)
    result_html = markdown.markdown(result)
    return templates.TemplateResponse("index.html", {"request": request, "result": result_html, "question": question})