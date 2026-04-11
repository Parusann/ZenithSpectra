"""Keyword-based category classification for content items."""

from app.models.content import Category

# Keywords mapped to categories — checked against title + cleaned content
CATEGORY_KEYWORDS: dict[Category, list[str]] = {
    Category.SPACE: [
        "nasa", "esa", "spacex", "rocket", "launch", "orbit", "satellite",
        "mars", "moon", "lunar", "asteroid", "comet", "telescope", "hubble",
        "james webb", "jwst", "exoplanet", "galaxy", "cosmic", "spacecraft",
        "astronaut", "iss", "space station", "artemis", "starship", "falcon",
        "rover", "solar system", "nebula", "supernova", "star", "mercury",
        "venus", "jupiter", "saturn", "uranus", "neptune", "pluto",
    ],
    Category.QUANTUM: [
        "quantum", "qubit", "entanglement", "superposition", "decoherence",
        "quantum computing", "quantum computer", "quantum error",
        "quantum communication", "quantum network", "quantum teleportation",
        "quantum sensor", "quantum cryptography", "quantum supremacy",
        "quantum advantage", "topological", "bose-einstein",
    ],
    Category.THEORETICAL: [
        "black hole", "dark matter", "dark energy", "string theory",
        "general relativity", "gravitational wave", "neutron star",
        "particle physics", "higgs", "antimatter", "neutrino", "muon",
        "standard model", "cosmology", "big bang", "inflation",
        "extra dimension", "unified theory", "quantum gravity",
        "cern", "lhc", "collider", "fermion", "boson",
    ],
    Category.FRONTIER: [
        "time travel", "warp drive", "alcubierre", "wormhole",
        "closed timelike", "simulation theory", "simulation hypothesis",
        "traversable wormhole", "exotic matter", "negative energy",
        "faster than light", "ftl", "tachyon", "multiverse",
    ],
}


def classify_category(title: str, content: str) -> Category:
    """Classify content into a category based on keyword matching.

    Returns the category with the most keyword hits.
    Falls back to SPACE as the broadest category.
    """
    text = f"{title} {content}".lower()

    scores: dict[Category, int] = {cat: 0 for cat in Category}
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[category] += 1

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return Category.SPACE  # default fallback

    return best
