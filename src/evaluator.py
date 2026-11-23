"""Evaluate JSONL model answers against independently calculated references."""
import argparse
import json
import math
from pathlib import Path


def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]


def score(questions, responses):
    reference = {q['id']: q for q in questions}
    if len(reference) != len(questions):
        raise ValueError('Duplicate question IDs')
    ids = [r['id'] for r in responses]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate response IDs')
    details = []
    for response in responses:
        qid = response['id']
        if qid not in reference:
            raise ValueError(f'Unknown question ID: {qid}')
        q = reference[qid]
        answer = q['answer']
        value = response.get('answer')
        if isinstance(answer, (int, float)) and not isinstance(answer, bool):
            try:
                parsed = float(value)
                tolerance = float(q.get('tolerance', 0))
                correct = (math.isfinite(parsed) and math.isfinite(float(answer))
                           and math.isfinite(tolerance) and tolerance >= 0
                           and abs(parsed - float(answer)) <= tolerance)
            except (ValueError, TypeError):
                correct = False
        else:
            correct = value is not None and str(value).strip().casefold() == str(answer).strip().casefold()
        details.append({'id': qid, 'correct': correct, 'expected': answer, 'submitted': value})
    missing = sorted(set(reference) - set(ids))
    details.extend({'id': qid, 'correct': False, 'expected': reference[qid]['answer'], 'submitted': None} for qid in missing)
    correct_count = sum(row['correct'] for row in details)
    return {'total': len(reference), 'correct': correct_count, 'accuracy': correct_count / len(reference) if reference else 0, 'details': details}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--questions', default='data/sample_questions.jsonl')
    parser.add_argument('--responses', required=True)
    parser.add_argument('--output', default='results/example_report.json')
    args = parser.parse_args()
    report = score(load_jsonl(args.questions), load_jsonl(args.responses))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"Scored {report['correct']}/{report['total']} ({report['accuracy']:.0%}) → {output}")


if __name__ == '__main__':
    main()
