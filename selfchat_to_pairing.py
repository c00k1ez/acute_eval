import json
import os
from glob import glob


def load_selfchat(selfchat_file):
    conversations = []
    with open(selfchat_file) as f_read:
        for line in f_read:
            conversations.append(json.loads(line.strip()))
    return conversations


if __name__ == '__main__':
    paths = glob('./selfchat_data/*/*.jsonl')
    convs = [load_selfchat(p) for p in paths]
    