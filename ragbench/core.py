import math

def ranking_metrics(ranking, relevant, k):
    if k < 1 or len(ranking) != len(set(ranking)):
        raise ValueError('Positive k and unique ranked IDs are required')
    relevant = set(relevant)
    if not relevant:
        raise ValueError('At least one relevant item is required')
    hits = [int(item in relevant) for item in ranking[:k]]
    dcg = sum(hit / math.log2(i + 2) for i, hit in enumerate(hits))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(k, len(relevant))))
    return {'recall': sum(hits) / len(relevant), 'ndcg': dcg / ideal,
            'mrr': next((1 / (i + 1) for i, hit in enumerate(hits) if hit), 0.)}

import re
from collections import Counter
import numpy as np

def tokens(text):
    return re.findall(r'\w+', text.lower())

def token_f1(answer, reference):
    a, b = Counter(tokens(answer)), Counter(tokens(reference))
    overlap = sum((a & b).values())
    denominator = sum(a.values()) + sum(b.values())
    return 2 * overlap / denominator if denominator else 1.

def run(data):
    rows = []
    for sample in data['samples']:
        metrics = ranking_metrics(sample['retrieved'], sample['relevant'], data['k']) if sample['relevant'] else None
        context_ids = set(sample['retrieved'][:data['k']])
        citations = set(sample['citations'])
        rows.append({'id': sample['id'], 'retrieval': metrics,
                     'answer_f1': token_f1(sample['answer'], sample['reference']),
                     'exact_match': tokens(sample['answer']) == tokens(sample['reference']),
                     'citation_id_precision': len(citations & context_ids) / len(citations) if citations else None,
                     'correct_abstention': not sample['answer'].strip() if not sample['relevant'] else None})
    if not rows:
        raise ValueError('No evaluation samples')
    retrieval = [r['retrieval'] for r in rows if r['retrieval'] is not None]
    return {'dataset': data['dataset'], 'samples': len(rows), 'retrieval_samples': len(retrieval),
            'answer_f1': float(np.mean([r['answer_f1'] for r in rows])),
            'exact_match': float(np.mean([r['exact_match'] for r in rows])),
            'retrieval': {key: float(np.mean([r[key] for r in retrieval])) for key in ['recall','mrr','ndcg']} if retrieval else {},
            'per_sample': rows}
