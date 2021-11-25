import argparse
from glob import glob
import os
import json
from typing import Any, Dict, List, Tuple
import csv


def read_pairings(pairings_path: str) -> List[Dict[str, Any]]:
    with open(pairings_path, 'r', encoding='utf-8') as f:
        data = [json.loads(sample)for sample in f]
    return data


def convert_dialogue(dialogue: List[Dict[str, str]], sep_token: str) -> Tuple[str]:
    conv_dialogue, ids, speakers = [], [], []
    for d in dialogue['dialogue']:
        conv_dialogue.append(d['text'])
        ids.append(d['id'])
    speakers = dialogue['speakers']
    return sep_token.join(conv_dialogue).replace(',', '<comma>'), sep_token.join(ids), sep_token.join(speakers)


def convert_to_csv(data: Dict[str, List[Dict[str, Any]]], sep_token='<sep>'):
    fields = [
        'correct_answer',
        'is_onboarding',
        'dialogue_1',
        'dilalogue_1_ids',
        'dialogue_1_speakers',
        'dialogue_2',
        'dilalogue_2_ids',
        'dialogue_2_speakers',
        'speakers_to_eval'
    ]
    edited_samples = []
    for sample in data:
        new_sample = ()
        if 'correct_answer' in sample:
            new_sample = (sample['correct_answer'], )
        else:
            new_sample = ('none', )
        new_sample = new_sample + (sample['is_onboarding'], )
        new_sample = new_sample + convert_dialogue(sample['dialogue_dicts'][0], sep_token=sep_token)
        new_sample = new_sample + convert_dialogue(sample['dialogue_dicts'][1], sep_token=sep_token)
        new_sample = new_sample + (sep_token.join(sample['speakers_to_eval']), )
        edited_samples.append(new_sample)
    return fields, edited_samples


def write_to_table(path, fields, table, separator='|'):
    with open(path, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(fields)
        spamwriter.writerows(table_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pairings_folder', default=None, type=str)
    parser.add_argument('--toloka_folder', default=None, type=str)
    parser.add_argument('--toloka_file', default=None, type=str)
    parser.add_argument('--pairings_file', default=None, type=str)

    args = parser.parse_args()

    assert args.pairings_folder is not None, 'define --pairings_folder'
    if args.toloka_folder is None:
        print('--toloka_folder is not define, use --pairings_folder as default folder')
        toloka_folder = args.pairings_folder
    else:
        toloka_folder = args.toloka_folder
    if args.toloka_file is None:
        print('--toloka_file is not define, use f"{pairings_file}_tokoka.csv" as default')
        pairings_file_name = os.listdir(args.pairings_folder)[0]
        toloka_file = f'{pairings_file_name}_tokoka.csv'
    else:
        toloka_file = args.toloka_file

    pairings_path = glob(os.path.join(args.pairings_folder, '*' if args.pairings_file is None else args.pairings_file))[0]

    toloka_path = os.path.join(toloka_folder, toloka_file)

    pairings = read_pairings(pairings_path)
    fields, table_data = convert_to_csv(pairings)
    
    write_to_table(toloka_path, fields, table_data)
