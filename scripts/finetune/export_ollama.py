"""
Export fine-tuned Gemma 4 LoRA adapter to Ollama-compatible GGUF format.

This script:
1. Merges the LoRA adapter with the base model
2. Converts merged weights to GGUF format
3. Generates an Ollama Modelfile
4. Optionally imports into Ollama directly

Prerequisites:
    pip install transformers peft torch
    git clone https://github.com/ggerganov/llama.cpp (for convert_hf_to_gguf.py)

Usage:
    python scripts/finetune/export_ollama.py
    python scripts/finetune/export_ollama.py --quant q5_k_m --import-ollama
"""

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Export fine-tuned model to Ollama")
    p.add_argument("--adapter", default="scripts/finetune/output/adapter",
                    help="Path to LoRA adapter directory")
    p.add_argument("--output", default="scripts/finetune/output/export",
                    help="Export output directory")
    p.add_argument("--quant", default="q4_k_m",
                    choices=["f16", "q8_0", "q5_k_m", "q4_k_m", "q4_0"],
                    help="GGUF quantization level")
    p.add_argument("--model-name", default="zenithspectra",
                    help="Ollama model name")
    p.add_argument("--llama-cpp", default=None,
                    help="Path to llama.cpp directory (for GGUF conversion)")
    p.add_argument("--import-ollama", action="store_true",
                    help="Automatically import into Ollama after export")
    return p.parse_args()


def merge_adapter(adapter_path: Path, output_path: Path):
    """Merge LoRA adapter weights into base model."""
    import json
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # Read base model name from training config
    config_path = adapter_path.parent / "train_config.json"
    if config_path.exists():
        with open(config_path) as f:
            train_config = json.load(f)
        base_model = train_config["base_model"]
    else:
        # Fall back to adapter config
        with open(adapter_path / "adapter_config.json") as f:
            adapter_config = json.load(f)
        base_model = adapter_config["base_model_name_or_path"]

    print(f"Loading base model: {base_model}")
    base = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16,
        device_map="cpu",  # merge on CPU to avoid VRAM issues
    )

    print(f"Loading adapter: {adapter_path}")
    model = PeftModel.from_pretrained(base, str(adapter_path))

    print("Merging adapter into base model...")
    merged = model.merge_and_unload()

    print(f"Saving merged model: {output_path / 'merged'}")
    merged_path = output_path / "merged"
    merged_path.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(str(merged_path))

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.save_pretrained(str(merged_path))

    return merged_path


def convert_to_gguf(merged_path: Path, output_path: Path, quant: str, llama_cpp: str = None):
    """Convert merged HF model to GGUF format."""
    gguf_path = output_path / f"zenithspectra-{quant}.gguf"

    # Find llama.cpp convert script
    if llama_cpp:
        convert_script = Path(llama_cpp) / "convert_hf_to_gguf.py"
    else:
        # Try common locations
        candidates = [
            Path.home() / "llama.cpp" / "convert_hf_to_gguf.py",
            Path("llama.cpp") / "convert_hf_to_gguf.py",
            Path("/opt/llama.cpp") / "convert_hf_to_gguf.py",
        ]
        convert_script = None
        for c in candidates:
            if c.exists():
                convert_script = c
                break

    if convert_script is None or not convert_script.exists():
        print("ERROR: llama.cpp not found. Please either:")
        print("  1. Clone it: git clone https://github.com/ggerganov/llama.cpp")
        print("  2. Specify path: --llama-cpp /path/to/llama.cpp")
        print()
        print(f"Merged model saved at: {merged_path}")
        print("You can manually convert with:")
        print(f"  python llama.cpp/convert_hf_to_gguf.py {merged_path} --outtype {quant} --outfile {gguf_path}")
        return None

    print(f"Converting to GGUF ({quant})...")
    cmd = [
        sys.executable, str(convert_script),
        str(merged_path),
        "--outtype", quant,
        "--outfile", str(gguf_path),
    ]
    subprocess.run(cmd, check=True)
    print(f"GGUF saved: {gguf_path}")
    return gguf_path


def create_modelfile(gguf_path: Path, output_path: Path, model_name: str):
    """Generate Ollama Modelfile."""
    modelfile_content = f"""FROM {gguf_path.resolve()}

TEMPLATE \"\"\"{{{{ if .System }}}}<start_of_turn>system
{{{{ .System }}}}<end_of_turn>
{{{{ end }}}}{{{{ range .Messages }}}}{{{{ if eq .Role "user" }}}}<start_of_turn>user
{{{{ .Content }}}}<end_of_turn>
{{{{ else if eq .Role "assistant" }}}}<start_of_turn>model
{{{{ .Content }}}}<end_of_turn>
{{{{ end }}}}{{{{ end }}}}<start_of_turn>model
\"\"\"

PARAMETER stop <end_of_turn>
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

SYSTEM \"\"\"You are a science intelligence analyst for ZenithSpectra, an AI-powered platform tracking developments in space exploration and frontier physics. Only use information from the provided text. If the text does not contain enough information, say so rather than speculating.\"\"\"
"""
    modelfile_path = output_path / "Modelfile"
    with open(modelfile_path, "w") as f:
        f.write(modelfile_content)
    print(f"Modelfile saved: {modelfile_path}")
    return modelfile_path


def import_to_ollama(modelfile_path: Path, model_name: str):
    """Import model into Ollama."""
    print(f"Importing into Ollama as '{model_name}'...")
    cmd = ["ollama", "create", model_name, "-f", str(modelfile_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Model imported! Run with: ollama run {model_name}")
    else:
        print(f"Ollama import failed: {result.stderr}")
        print(f"Manual import: ollama create {model_name} -f {modelfile_path}")


def main():
    args = parse_args()
    adapter_path = Path(args.adapter)
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    if not adapter_path.exists():
        print(f"ERROR: Adapter not found at {adapter_path}")
        print("Run training first: python scripts/finetune/train.py")
        sys.exit(1)

    # Step 1: Merge
    merged_path = merge_adapter(adapter_path, output_path)

    # Step 2: Convert to GGUF
    gguf_path = convert_to_gguf(merged_path, output_path, args.quant, args.llama_cpp)

    if gguf_path:
        # Step 3: Create Modelfile
        modelfile_path = create_modelfile(gguf_path, output_path, args.model_name)

        # Step 4: Optional Ollama import
        if args.import_ollama:
            import_to_ollama(modelfile_path, args.model_name)
        else:
            print(f"\nTo import into Ollama:")
            print(f"  ollama create {args.model_name} -f {modelfile_path}")


if __name__ == "__main__":
    main()
