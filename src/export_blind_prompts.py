"""Export evaluation prompts without leaking reference answers or tolerances.

Ground truth remains in the separate questions JSONL file. A human/operator
must supply the source DEM statistics or raster to the model being evaluated.
"""
import argparse
import json
from pathlib import Path

from src.evaluator import load_jsonl


def blind_prompts(questions):
    return [{"id": q["id"], "question": q["question"]} for q in questions]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions", default="data/tucson_reference_questions.jsonl")
    parser.add_argument("--output", default="results/tucson/blind_prompts.jsonl")
    args = parser.parse_args()
    questions = load_jsonl(args.questions)
    ids = [q["id"] for q in questions]
    if len(ids) != len(set(ids)):
        parser.error("Duplicate question IDs")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(q) + "\n" for q in blind_prompts(questions)),
        encoding="utf-8",
    )
    print(f"Exported {len(questions)} prompts (without answers): {output}")
    print("Important: questions requiring raster statistics are not answerable without")
    print("providing the model with the actual DEM or independently measured inputs.")


if __name__ == "__main__":
    main()
