"""Rule-based credibility scoring engine (spec Section 8.2).

Computes a credibility score starting from the source baseline,
then applies adjustments based on content signals.
"""

import re

from app.models.content import SourceType


# Source type base score ranges
SOURCE_BASE_SCORES = {
    SourceType.AGENCY: 95,
    SourceType.JOURNAL: 95,
    SourceType.RESEARCH_INSTITUTION: 90,
    SourceType.PREPRINT: 70,
    SourceType.SCIENCE_MEDIA: 60,
    SourceType.GENERAL_NEWS: 50,
}

# Domains that indicate primary sources
PRIMARY_DOMAINS = {".gov", ".edu", ".ac.uk", ".ac.jp", "cern.ch", "esa.int"}

# Hype phrases that reduce credibility
HYPE_PHRASES = [
    "proves", "breakthrough", "changes everything", "game changer",
    "revolutionary", "groundbreaking", "mind-blowing", "shocking",
    "you won't believe", "finally proven", "scientists baffled",
]

# Hedging phrases that indicate responsible reporting
HEDGING_PHRASES = [
    "suggests", "preliminary", "may indicate", "could potentially",
    "further research", "not yet confirmed", "remains unclear",
    "initial findings", "early results", "appears to",
]


def score_credibility(
    source_baseline: int,
    source_type: SourceType,
    original_url: str,
    title: str,
    content: str,
) -> tuple[int, str]:
    """Compute credibility score and explanation.

    Returns (score, explanation) tuple.
    """
    score = source_baseline
    reasons = []
    text = f"{title} {content}".lower()

    # Check if primary source
    is_primary = any(domain in original_url.lower() for domain in PRIMARY_DOMAINS)
    if is_primary:
        score += 10
        reasons.append("primary institutional source")

    # Check for DOI or arxiv links (has linked paper)
    has_paper_link = bool(
        re.search(r"doi\.org/|arxiv\.org/abs/|arxiv\.org/pdf/", content.lower())
    )
    if has_paper_link:
        score += 5
        reasons.append("links to paper/study")

    # Check if peer-reviewed source (not preprint)
    if source_type == SourceType.JOURNAL:
        score += 10
        reasons.append("peer-reviewed journal")
    elif source_type == SourceType.PREPRINT:
        reasons.append("preprint (not peer-reviewed)")

    # Detect hedging language (positive signal)
    hedging_count = sum(1 for phrase in HEDGING_PHRASES if phrase in text)
    if hedging_count >= 2:
        score += 3
        reasons.append("appropriate hedging language")

    # Detect hype language (negative signal)
    hype_count = sum(1 for phrase in HYPE_PHRASES if phrase in text)
    if hype_count >= 1:
        score -= 10 * min(hype_count, 2)
        reasons.append(f"hype language detected ({hype_count} instances)")

    # Clamp score to 0-100
    score = max(0, min(100, score))

    # Build explanation
    source_label = source_type.value.replace("_", " ").title()
    if score >= 90:
        level = "Very high credibility"
    elif score >= 75:
        level = "High credibility"
    elif score >= 60:
        level = "Moderate credibility"
    elif score >= 40:
        level = "Low credibility"
    else:
        level = "Very low credibility"

    detail = ", ".join(reasons) if reasons else "baseline score"
    explanation = f"{level}: {source_label} source. {detail}."

    return score, explanation
