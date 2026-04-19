"""
Downloads a small subset of the tatsu-lab/alpaca dataset from Hugging Face
and converts it to the train.txt format used by train.py:

    <prompt line>
    <response line>

    <prompt line>
    <response line>
    ...

Only the first MAX_EXAMPLES examples are kept to stay small.
"""

from datasets import load_dataset

MAX_EXAMPLES = 500   # adjust up/down as needed
OUTPUT_FILE = "train.txt"

print("Downloading tatsu-lab/alpaca (train split)...")
ds = load_dataset("tatsu-lab/alpaca", split="train")

examples = []

for row in ds:
    instruction = row["instruction"].strip()
    inp = row.get("input", "").strip()
    output = row["output"].strip()

    # Combine instruction + input as the prompt when input is present
    if inp:
        prompt = f"{instruction}\n{inp}"
    else:
        prompt = instruction

    if prompt and output:
        examples.append((prompt, output))

    if len(examples) >= MAX_EXAMPLES:
        break

print(f"Writing {len(examples)} examples to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i, (prompt, response) in enumerate(examples):
        f.write(f"{prompt}\n{response}")
        if i < len(examples) - 1:
            f.write("\n\n")

print("Done!")
