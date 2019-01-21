""" Official evaluation script for v1.1 of the SQuAD dataset. """
from __future__ import print_function
from collections import Counter
import string
import re
import argparse
import json
import sys


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    if args.task == 'sogou':
        prediction_tokens = list(normalize_answer(prediction))
        ground_truth_tokens = list(normalize_answer(ground_truth))
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def evaluate(dataset, predictions, result_file=None):
    f1 = exact_match = total = 0
    rv = {}
    for article in dataset:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                total += 1
                if qa['id'] not in predictions:
                    message = 'Unanswered question ' + qa['id'] + \
                              ' will receive score 0.'
                    print(message, file=sys.stderr)
                    continue
                ground_truths = list(map(lambda x: x['text'], qa['answers']))
                prediction = predictions[qa['id']]
                cur_em = metric_max_over_ground_truths(
                    exact_match_score, prediction, ground_truths)
                exact_match += cur_em
                cur_f1 = metric_max_over_ground_truths(
                    f1_score, prediction, ground_truths)
                f1 += cur_f1
                rv[qa['id']] = {'em': cur_em, 'f1': cur_f1}
    if result_file is not None:
        print('save details results to %s' % result_file)
        json.dump(rv, open(result_file, 'w'))
    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total

    return {'exact_match': exact_match, 'f1': f1}


def evaluate_sogou(datasets, predictions, result_file=None):
    f1 = exact_match = total = 0
    rv = {}
    for d in datasets:
        if d['answer_text'] == '':
            continue
        if d['query_id'] not in predictions:
            print('%s not in predictions' % d['query_id'])
            continue
        total += 1
        ground_truths = [d['answer_text']]
        prediction = predictions[d['query_id']]
        # remove space in the answer text
        prediction = ''.join(prediction.split())
        cur_em = metric_max_over_ground_truths(
            exact_match_score, prediction, ground_truths)
        exact_match += cur_em
        cur_f1 = metric_max_over_ground_truths(
            f1_score, prediction, ground_truths)
        f1 += cur_f1
        rv[d['query_id']] = {'em': cur_em, 'f1': cur_f1}

    if result_file is not None:
        print('save details results to %s' % result_file)
        json.dump(rv, open(result_file, 'w'))
    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total

    return {'exact_match': exact_match, 'f1': f1, 'total': total}


if __name__ == '__main__':
    expected_version = '1.1'
    parser = argparse.ArgumentParser(
        description='Evaluation for SQuAD ' + expected_version)
    parser.add_argument('dataset_file', help='Dataset file')
    parser.add_argument('prediction_file', help='Prediction File')
    parser.add_argument('--result_file', help='resultsfile File')
    parser.add_argument('--task', help='which dataset')
    args = parser.parse_args()
    with open(args.dataset_file) as dataset_file:
        if args.task == 'squad':
            dataset_json = json.load(dataset_file)
            dataset = dataset_json['data']
        else:
            dataset = [json.loads(line) for line in dataset_file]
    with open(args.prediction_file) as prediction_file:
        predictions = json.load(prediction_file)
    if args.task == 'sogou':
        print(json.dumps(evaluate_sogou(dataset, predictions, result_file=args.result_file)))
    elif args.task == 'squad':
        print(json.dumps(evaluate(dataset, predictions, result_file=args.result_file)))