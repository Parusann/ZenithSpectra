import json
import logging

from app.llm.provider import get_llm_provider

logger = logging.getLogger(__name__)

SYSTEM_ROLE = (
    "You are a science intelligence analyst for ZenithSpectra, "
    "an AI-powered platform tracking developments in space exploration and frontier physics. "
    "Only use information from the provided text. "
    "If the text does not contain enough information, say so rather than speculating."
)


async def generate_summary(text: str, level: str) -> str:
    """Generate a summary at the specified level (quick or expanded)."""
    provider = get_llm_provider()

    prompts = {
        "quick": (
            "Summarize this science article in 1-2 sentences. "
            "Be factual. Do not add interpretation. Use accessible language."
        ),
        "expanded": (
            "Provide a 2-3 paragraph summary covering: "
            "(1) what happened or was discovered, "
            "(2) why it matters, "
            "(3) what the source is actually claiming, "
            "(4) what remains uncertain or unconfirmed."
        ),
    }

    return await provider.generate(SYSTEM_ROLE, f"{prompts[level]}\n\nArticle:\n{text}")


async def generate_explanation(text: str, level: str) -> str:
    """Generate an explanation at the specified level."""
    provider = get_llm_provider()

    prompts = {
        "beginner": (
            "Explain this development as if talking to a curious non-scientist. "
            "Avoid jargon. Use analogies where helpful. Keep it under 200 words."
        ),
        "intermediate": (
            "Explain this for someone with basic science literacy (e.g., a university student). "
            "Use correct terminology but define advanced terms. Keep it under 300 words."
        ),
        "technical": (
            "Explain this for a researcher or advanced student. "
            "Use precise terminology. Reference relevant theories or prior work. "
            "Keep it under 400 words."
        ),
    }

    return await provider.generate(SYSTEM_ROLE, f"{prompts[level]}\n\nArticle:\n{text}")


async def answer_question(context: str, question: str) -> str:
    """Answer a user question grounded in article content."""
    provider = get_llm_provider()

    system = (
        "You are a science intelligence assistant for ZenithSpectra. "
        "Answer the user's question based ONLY on the provided article content. "
        "If the article does not contain enough information to answer, say so clearly. "
        "Do not speculate or add information from outside the article. "
        "Cite specific parts of the article when relevant. "
        "Use clear, accessible language."
    )

    return await provider.generate(system, f"Article:\n{context}\n\nQuestion: {question}")


async def evaluate_credibility(text: str, headline: str) -> dict:
    """Evaluate credibility of content. Returns {score_adjustment, explanation}."""
    provider = get_llm_provider()

    prompt = (
        "Analyze this science article for credibility. "
        "Score adjustments from -20 to +10 based on: "
        "tone (sensational vs measured), whether claims are supported by cited evidence, "
        "whether uncertainty is acknowledged, whether the headline matches the actual content. "
        "Return ONLY a JSON object with score_adjustment (integer) and explanation (one sentence)."
        f"\n\nHeadline: {headline}\n\nArticle:\n{text}"
    )

    raw = await provider.generate(SYSTEM_ROLE, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("LLM returned non-JSON credibility response: %s", raw[:200])
        return {"score_adjustment": 0, "explanation": "Could not evaluate credibility."}


async def classify_content(text: str) -> dict:
    """Classify content category, scientific status, and tags."""
    provider = get_llm_provider()

    prompt = (
        "Classify this science article. Return ONLY a JSON object with:\n"
        '- category: one of "space", "quantum", "theoretical", "frontier"\n'
        '- scientific_status: one of "established", "supported", "active_research", '
        '"speculative", "highly_speculative", "media_hype"\n'
        "- tags: array of 3-8 topic tag strings\n\n"
        f"Article:\n{text}"
    )

    raw = await provider.generate(SYSTEM_ROLE, prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("LLM returned non-JSON classification: %s", raw[:200])
        return {"category": "space", "scientific_status": "active_research", "tags": []}
