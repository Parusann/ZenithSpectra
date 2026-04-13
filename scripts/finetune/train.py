"""
Fine-tune Gemma 4 E4B for ZenithSpectra science intelligence tasks.

Recommended hardware: AMD RX 7900 XTX (24GB) or NVIDIA GPU with 12GB+ VRAM.
Uses QLoRA (4-bit quantization + LoRA adapters) to fit in VRAM.

Setup (WSL2 Ubuntu for AMD):
    pip install torch --index-url https://download.pytorch.org/whl/rocm7.0
    pip install transformers trl peft datasets accelerate
    # For AMD: build bitsandbytes from ROCm fork (see README)

Usage:
    python scripts/finetune/train.py
    python scripts/finetune/train.py --model google/gemma-4-E4B-it --epochs 5
    python scripts/finetune/train.py --model google/gemma-4-31B-it --lora-rank 8  # tight VRAM
"""

import argparse
import json
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTTrainer, SFTConfig


def parse_args():
    p = argparse.ArgumentParser(description="Fine-tune Gemma 4 for ZenithSpectra")
    p.add_argument("--model", default="google/gemma-4-E4B-it",
                    help="Base model (default: google/gemma-4-E4B-it)")
    p.add_argument("--data", default="scripts/finetune/data/train.jsonl",
                    help="Training data JSONL path")
    p.add_argument("--output", default="scripts/finetune/output",
                    help="Output directory for adapter weights")
    p.add_argument("--epochs", type=int, default=3,
                    help="Number of training epochs")
    p.add_argument("--lora-rank", type=int, default=32,
                    help="LoRA rank (lower = less VRAM, 8 for 31B, 32-64 for E4B)")
    p.add_argument("--lora-alpha", type=int, default=64,
                    help="LoRA alpha (typically 2x rank)")
    p.add_argument("--max-seq-len", type=int, default=4096,
                    help="Maximum sequence length (2048 for 31B, 4096 for E4B)")
    p.add_argument("--batch-size", type=int, default=2,
                    help="Per-device batch size (1 for 31B, 2-4 for E4B)")
    p.add_argument("--grad-accum", type=int, default=4,
                    help="Gradient accumulation steps")
    p.add_argument("--lr", type=float, default=2e-4,
                    help="Learning rate")
    p.add_argument("--no-4bit", action="store_true",
                    help="Disable 4-bit quantization (use 16-bit, needs more VRAM)")
    return p.parse_args()


def load_model_and_tokenizer(args):
    """Load base model with quantization config."""
    print(f"Loading model: {args.model}")

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    if args.no_4bit:
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
    else:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            quantization_config=bnb_config,
            device_map="auto",
        )
        model = prepare_model_for_kbit_training(model)

    return model, tokenizer


def apply_lora(model, args):
    """Apply LoRA adapter configuration."""
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=args.lora_rank,
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def format_chat(example, tokenizer):
    """Format a training example using the model's chat template."""
    messages = example["messages"]
    # Gemma 4 uses 'model' role — ensure compatibility
    formatted = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False,
    )
    return {"text": formatted}


def main():
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load model
    model, tokenizer = load_model_and_tokenizer(args)
    model = apply_lora(model, args)

    # Load dataset
    print(f"Loading dataset: {args.data}")
    dataset = load_dataset("json", data_files=args.data, split="train")
    dataset = dataset.map(
        lambda x: format_chat(x, tokenizer),
        remove_columns=dataset.column_names,
    )
    print(f"Dataset size: {len(dataset)} examples")

    # Training config
    training_args = SFTConfig(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        weight_decay=0.01,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        optim="adamw_8bit",
        bf16=True,
        logging_steps=1,
        save_strategy="epoch",
        save_total_limit=2,
        max_seq_length=args.max_seq_len,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        dataset_text_field="text",
        report_to="none",
        remove_unused_columns=False,
    )

    # Train
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    print("Starting training...")
    trainer.train()

    # Save adapter
    adapter_path = output_dir / "adapter"
    model.save_pretrained(str(adapter_path))
    tokenizer.save_pretrained(str(adapter_path))
    print(f"Adapter saved to: {adapter_path}")

    # Save training config for reference
    config_path = output_dir / "train_config.json"
    with open(config_path, "w") as f:
        json.dump({
            "base_model": args.model,
            "lora_rank": args.lora_rank,
            "lora_alpha": args.lora_alpha,
            "epochs": args.epochs,
            "max_seq_length": args.max_seq_len,
            "batch_size": args.batch_size,
            "learning_rate": args.lr,
        }, f, indent=2)

    print(f"\nTraining complete! Next steps:")
    print(f"  1. Export to GGUF:  python scripts/finetune/export_ollama.py")
    print(f"  2. Import to Ollama: ollama create zenithspectra -f scripts/finetune/output/Modelfile")


if __name__ == "__main__":
    main()
