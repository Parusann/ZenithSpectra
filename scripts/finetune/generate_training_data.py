"""
Generate fine-tuning dataset for ZenithSpectra's Gemma 4 model.

Creates training examples that teach the model ZenithSpectra's exact output
formats: quick summaries, multi-level explanations, credibility evaluation
(JSON), content classification (JSON), and grounded Q&A.

Usage:
    python scripts/finetune/generate_training_data.py

Outputs: scripts/finetune/data/train.jsonl
"""

import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

SYSTEM_PROMPT = (
    "You are a science intelligence analyst for ZenithSpectra, an AI-powered "
    "platform tracking developments in space exploration and frontier physics. "
    "Only use information from the provided text. If the text does not contain "
    "enough information, say so rather than speculating."
)


def make_example(system: str, user: str, model_response: str) -> dict:
    """Create a single training example in Gemma 4 conversational format."""
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "model", "content": model_response},
        ]
    }


# --- SUMMARIZATION EXAMPLES ---
SUMMARY_EXAMPLES = [
    make_example(
        SYSTEM_PROMPT,
        "Summarize this science article in 1-2 sentences. Be factual. Do not add interpretation. Use accessible language.\n\n"
        "NASA's Perseverance rover has detected organic molecules in Jezero Crater rocks that show patterns consistent with biological processes, "
        "according to a study published in Nature. The molecules, found in carbonate-rich samples, contain carbon-hydrogen bonds arranged in ways "
        "that on Earth are typically associated with microbial activity. However, researchers caution that abiotic chemical processes could also "
        "produce similar signatures. The samples are scheduled for return to Earth via the Mars Sample Return mission for definitive analysis.",
        "NASA's Perseverance rover found organic molecules in Jezero Crater rocks with patterns that could indicate biological activity, "
        "though abiotic processes may also explain the signatures. The samples will be returned to Earth for definitive analysis."
    ),
    make_example(
        SYSTEM_PROMPT,
        "Summarize this science article in 1-2 sentences. Be factual. Do not add interpretation. Use accessible language.\n\n"
        "Researchers at IBM Quantum have demonstrated a 1,121-qubit processor called Condor that achieved quantum error correction below "
        "the fault-tolerance threshold for the first time in a superconducting system. The breakthrough uses a novel surface code implementation "
        "that reduces physical qubit overhead by 40% compared to previous approaches. This milestone brings practical quantum computing closer "
        "to reality, though researchers estimate commercially useful quantum advantage is still 5-10 years away.",
        "IBM demonstrated a 1,121-qubit processor that achieved quantum error correction below the fault-tolerance threshold for the first time "
        "in a superconducting system. The advance reduces qubit overhead by 40%, though practical quantum advantage remains years away."
    ),
    make_example(
        SYSTEM_PROMPT,
        "Provide a 2-3 paragraph summary covering: (1) what happened or was discovered, (2) why it matters, "
        "(3) what the source is actually claiming, (4) what remains uncertain or unconfirmed.\n\n"
        "A team at CERN's LHCb detector has observed an unexpected asymmetry in the decay rates of charm mesons that deviates from "
        "Standard Model predictions by 3.8 sigma. The measurement, based on Run 3 data collected between 2022-2025, shows CP violation "
        "in the charm sector at levels not predicted by current theoretical frameworks. The result has been submitted to Physical Review Letters.",
        "CERN's LHCb experiment has measured CP violation in charm meson decays at 3.8 sigma above Standard Model predictions, "
        "using data from Run 3 (2022-2025). This is the strongest evidence yet for new physics in the charm quark sector.\n\n"
        "If confirmed, this finding would indicate that our current understanding of matter-antimatter asymmetry is incomplete and "
        "could point toward new particles or forces not accounted for in the Standard Model. CP violation is central to explaining "
        "why the universe contains more matter than antimatter.\n\n"
        "The team claims a 3.8-sigma deviation, which is statistically significant but below the 5-sigma threshold typically required "
        "for a discovery claim in particle physics. The result needs independent confirmation from ATLAS or CMS experiments, "
        "and systematic uncertainties in the charm sector are notoriously difficult to control."
    ),
]

# --- EXPLANATION EXAMPLES ---
EXPLANATION_EXAMPLES = [
    make_example(
        SYSTEM_PROMPT,
        "Explain this development as if talking to a curious non-scientist. Avoid jargon. Use analogies where helpful. "
        "Keep it under 200 words.\n\n"
        "Scientists have detected gravitational waves from a binary neutron star merger at a distance of 40 megaparsecs, "
        "with an associated kilonova producing heavy elements including gold and platinum through rapid neutron capture.",
        "Imagine two incredibly dense stars — each packing the mass of our Sun into a ball the size of a city — spiraling "
        "toward each other and finally crashing together. Scientists detected the ripples this collision sent through space "
        "itself, like vibrations from dropping a bowling ball on a trampoline.\n\n"
        "When these stars collided, the explosion was so extreme that it actually created gold, platinum, and other heavy "
        "elements. It turns out the gold in your jewelry was likely forged in ancient collisions just like this one.\n\n"
        "This is exciting because it proves two things at once: we can detect these cosmic ripples (gravitational waves), "
        "and we now know where many of the heaviest elements in the universe come from."
    ),
    make_example(
        SYSTEM_PROMPT,
        "Explain this for someone with basic science literacy (e.g., a university student). Use correct terminology but "
        "define advanced terms. Keep it under 300 words.\n\n"
        "A quantum computing team has demonstrated logical qubit error rates below 10^-6 using a distance-7 surface code "
        "on a 72-qubit superconducting processor.",
        "A team has achieved a major milestone in quantum error correction by bringing logical qubit error rates below "
        "one-in-a-million (10⁻⁶) on a superconducting processor.\n\n"
        "The key concept here is the difference between physical and logical qubits. Physical qubits are the actual "
        "hardware components — superconducting circuits cooled to near absolute zero. They're inherently noisy, meaning "
        "errors creep in during calculations. A logical qubit is constructed from multiple physical qubits working together "
        "to detect and correct these errors, similar to how error-correcting codes work in digital communications.\n\n"
        "The 'surface code' is the specific error-correction scheme used here. It arranges qubits in a 2D grid where "
        "each logical qubit is protected by measuring neighboring qubits for signs of errors. 'Distance-7' means the code "
        "can detect and correct up to 3 simultaneous errors — the higher the distance, the more robust the protection, "
        "but the more physical qubits are needed.\n\n"
        "Using 72 physical qubits to achieve sub-10⁻⁶ logical error rates demonstrates that scaling up the number of "
        "physical qubits genuinely improves reliability, which was not guaranteed by theory alone. This is a prerequisite "
        "for building quantum computers that can tackle problems beyond classical capabilities."
    ),
    make_example(
        SYSTEM_PROMPT,
        "Explain this for a researcher or advanced student. Use precise terminology. Reference relevant theories or "
        "prior work. Keep it under 400 words.\n\n"
        "New observations from the James Webb Space Telescope reveal that galaxies at z > 10 are significantly more "
        "massive than predicted by ΛCDM simulations, with stellar masses exceeding 10^10 solar masses at z ≈ 13.",
        "JWST's NIRCam and NIRSpec observations continue to challenge hierarchical structure formation models. The "
        "detection of galaxies with stellar masses M★ > 10¹⁰ M☉ at redshifts z ≈ 13 — corresponding to approximately "
        "330 Myr after the Big Bang — substantially exceeds predictions from state-of-the-art ΛCDM hydrodynamical "
        "simulations including IllustrisTNG, EAGLE, and FLAMINGO.\n\n"
        "The tension is quantifiable: the observed stellar mass density at z > 10 exceeds ΛCDM predictions by factors "
        "of 10-100×, depending on the simulation and assumed initial mass function. This is related to the 'impossibly "
        "early galaxy problem' first identified by Labbé et al. (2023) and subsequently confirmed by multiple independent "
        "photometric and spectroscopic surveys.\n\n"
        "Several explanations have been proposed. Modified star formation efficiency at high redshift, where the absence "
        "of metals and feedback mechanisms could permit near-maximal baryon-to-star conversion rates (ε★ → 1), would "
        "alleviate the tension without modifying cosmology. Alternatively, a top-heavy IMF at high-z would increase "
        "the mass-to-light ratio, though this remains observationally unconstrained.\n\n"
        "More exotic solutions include primordial black hole seeding from the dark sector, early dark energy models "
        "that accelerate structure growth, or modifications to the matter power spectrum at small scales. The spectroscopic "
        "confirmation from NIRSpec is critical, as photometric redshifts at z > 10 are susceptible to degeneracies "
        "with dusty galaxies at z ≈ 2-5. Current spectroscopic confirmation rates are approximately 70% for the "
        "highest-confidence photometric candidates."
    ),
]

# --- CREDIBILITY EVALUATION EXAMPLES ---
CREDIBILITY_EXAMPLES = [
    make_example(
        SYSTEM_PROMPT,
        "Analyze this science article for credibility. Score adjustments from -20 to +10 based on: "
        "tone (sensational vs measured), whether claims are supported by cited evidence, whether uncertainty "
        "is acknowledged, whether the headline matches the actual content. Return ONLY a JSON object with "
        "score_adjustment (integer) and explanation (one sentence).\n\n"
        "Headline: Scientists Find Key to Immortality in New Gene Discovery\n\n"
        "Article: Researchers at Stanford identified a gene variant associated with a 3% increase in lifespan "
        "in lab mice. The study, published in Cell, involved 200 mice over 2 years. Lead author Dr. Chen noted "
        "the findings are preliminary and may not translate to humans.",
        '{"score_adjustment": -15, "explanation": "Sensationalized headline claims \'immortality\' when the study found only a 3% lifespan increase in mice with clear caveats about human applicability."}'
    ),
    make_example(
        SYSTEM_PROMPT,
        "Analyze this science article for credibility. Score adjustments from -20 to +10 based on: "
        "tone (sensational vs measured), whether claims are supported by cited evidence, whether uncertainty "
        "is acknowledged, whether the headline matches the actual content. Return ONLY a JSON object with "
        "score_adjustment (integer) and explanation (one sentence).\n\n"
        "Headline: New Measurement Constrains Neutrino Mass Upper Bound\n\n"
        "Article: The KATRIN experiment has reported a new upper limit on the electron antineutrino mass of "
        "0.45 eV at 90% confidence level, improving on their previous result of 0.8 eV. The measurement used "
        "tritium beta decay spectroscopy over a 250-day data collection period. Systematic uncertainties were "
        "carefully characterized, and the team notes that reaching the target sensitivity of 0.2 eV will require "
        "additional running time and detector upgrades.",
        '{"score_adjustment": 8, "explanation": "Measured tone with accurate headline, specific methodology cited, uncertainties acknowledged, and clear statement of limitations."}'
    ),
    make_example(
        SYSTEM_PROMPT,
        "Analyze this science article for credibility. Score adjustments from -20 to +10 based on: "
        "tone (sensational vs measured), whether claims are supported by cited evidence, whether uncertainty "
        "is acknowledged, whether the headline matches the actual content. Return ONLY a JSON object with "
        "score_adjustment (integer) and explanation (one sentence).\n\n"
        "Headline: Quantum Computer Solves Problem in Minutes That Would Take Classical Computer Millions of Years\n\n"
        "Article: Google's latest quantum processor completed a specific random circuit sampling task in 3 minutes "
        "that would take the fastest supercomputer an estimated 47 years. However, the task was specifically designed "
        "to favor quantum processors and has no known practical applications. Independent researchers have suggested "
        "that improved classical algorithms could narrow the gap significantly.",
        '{"score_adjustment": -5, "explanation": "While the article body is balanced with appropriate caveats, the headline \'millions of years\' significantly overstates the actual 47-year estimate from the article."}'
    ),
]

# --- CLASSIFICATION EXAMPLES ---
CLASSIFICATION_EXAMPLES = [
    make_example(
        SYSTEM_PROMPT,
        "Classify this science article. Return ONLY a JSON object with:\n"
        "- category: one of \"space\", \"quantum\", \"theoretical\", \"frontier\"\n"
        "- scientific_status: one of \"established\", \"supported\", \"active_research\", \"speculative\", \"highly_speculative\", \"media_hype\"\n"
        "- tags: array of 3-8 topic tag strings\n\n"
        "Article: ESA's JUICE spacecraft has entered orbit around Jupiter's moon Ganymede, becoming the first spacecraft "
        "to orbit a moon other than Earth's. Initial radar measurements confirm the presence of a subsurface ocean beneath "
        "Ganymede's ice shell, consistent with earlier Hubble and Galileo observations. The mission will spend 9 months "
        "characterizing the ocean's depth, salinity, and potential habitability.",
        '{"category": "space", "scientific_status": "established", "tags": ["jupiter", "ganymede", "subsurface ocean", "ESA", "JUICE mission", "planetary science", "astrobiology"]}'
    ),
    make_example(
        SYSTEM_PROMPT,
        "Classify this science article. Return ONLY a JSON object with:\n"
        "- category: one of \"space\", \"quantum\", \"theoretical\", \"frontier\"\n"
        "- scientific_status: one of \"established\", \"supported\", \"active_research\", \"speculative\", \"highly_speculative\", \"media_hype\"\n"
        "- tags: array of 3-8 topic tag strings\n\n"
        "Article: A new theoretical framework proposes that dark matter consists of primordial black holes formed "
        "during a first-order phase transition in the early universe. The authors argue this could explain both the "
        "dark matter density and the unexpectedly massive galaxies observed by JWST at high redshift. The paper, "
        "published as a preprint on arXiv, has not yet been peer-reviewed.",
        '{"category": "theoretical", "scientific_status": "speculative", "tags": ["dark matter", "primordial black holes", "cosmology", "JWST", "early universe", "phase transition"]}'
    ),
    make_example(
        SYSTEM_PROMPT,
        "Classify this science article. Return ONLY a JSON object with:\n"
        "- category: one of \"space\", \"quantum\", \"theoretical\", \"frontier\"\n"
        "- scientific_status: one of \"established\", \"supported\", \"active_research\", \"speculative\", \"highly_speculative\", \"media_hype\"\n"
        "- tags: array of 3-8 topic tag strings\n\n"
        "Article: Microsoft and Quantinuum have announced a breakthrough in topological qubits, demonstrating "
        "non-Abelian anyons in a controlled laboratory setting for the first time. The result, published in Nature, "
        "shows that topological qubits have inherently lower error rates than superconducting or trapped-ion alternatives. "
        "However, scaling beyond the current 12-qubit prototype remains an open engineering challenge.",
        '{"category": "quantum", "scientific_status": "supported", "tags": ["topological qubits", "non-Abelian anyons", "quantum error correction", "Microsoft", "Quantinuum"]}'
    ),
]

# --- Q&A EXAMPLES ---
QA_EXAMPLES = [
    make_example(
        SYSTEM_PROMPT,
        "Article:\nThe Parker Solar Probe completed its closest approach to the Sun, passing within 6.1 million kilometers "
        "of the solar surface at a speed of 635,000 km/h. During the flyby, the probe's WISPR instrument captured "
        "images of coronal structures never seen before, including helical magnetic flux ropes that extend millions "
        "of kilometers into the heliosphere. Temperature measurements confirmed the corona exceeds 1 million degrees "
        "Celsius, while the photosphere below remains at approximately 5,500°C — deepening the coronal heating mystery.\n\n"
        "Question: Why is the corona hotter than the surface?",
        "According to the article, this remains an unsolved mystery. The article states that temperature measurements "
        "confirmed the corona exceeds 1 million degrees Celsius while the photosphere below is approximately 5,500°C, "
        "describing this as 'the coronal heating mystery.' The article does not provide an explanation for why this "
        "temperature inversion occurs — it identifies it as an open question that the Parker Solar Probe's observations "
        "are helping to investigate, with newly captured images of helical magnetic flux ropes that may play a role."
    ),
    make_example(
        SYSTEM_PROMPT,
        "Article:\nCRISPR-based gene drives have been successfully tested in wild populations of Anopheles gambiae "
        "mosquitoes in Burkina Faso, reducing malaria-carrying mosquito populations by 72% in the test region over "
        "18 months. The trial, conducted by Target Malaria and published in Science, used a suppression drive targeting "
        "the doublesex gene. Ecological monitoring showed no significant impact on non-target insect species, though "
        "the monitoring period was limited to 2 years. WHO has not yet approved gene drives for broader deployment.\n\n"
        "Question: Is this safe for other animals?",
        "The article provides limited information on this question. It states that ecological monitoring showed 'no "
        "significant impact on non-target insect species,' which is encouraging. However, the article also notes an "
        "important caveat: the monitoring period was limited to only 2 years, which may not be sufficient to detect "
        "longer-term ecological effects. The article does not discuss potential impacts on animals that feed on mosquitoes, "
        "such as birds, bats, or fish. Additionally, the WHO has not yet approved gene drives for broader deployment, "
        "suggesting that safety questions remain under evaluation."
    ),
]

def main():
    all_examples = (
        SUMMARY_EXAMPLES
        + EXPLANATION_EXAMPLES
        + CREDIBILITY_EXAMPLES
        + CLASSIFICATION_EXAMPLES
        + QA_EXAMPLES
    )

    output_path = DATA_DIR / "train.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")

    print(f"Generated {len(all_examples)} training examples -> {output_path}")
    print(f"  Summaries:     {len(SUMMARY_EXAMPLES)}")
    print(f"  Explanations:  {len(EXPLANATION_EXAMPLES)}")
    print(f"  Credibility:   {len(CREDIBILITY_EXAMPLES)}")
    print(f"  Classification:{len(CLASSIFICATION_EXAMPLES)}")
    print(f"  Q&A:           {len(QA_EXAMPLES)}")
    print()
    print("NOTE: This is a seed dataset. For best results, expand to 200-500+")
    print("examples per task type using real articles from your database.")


if __name__ == "__main__":
    main()
