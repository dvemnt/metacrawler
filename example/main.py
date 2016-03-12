# coding=utf-8

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import handlers


def main():
    """Main function."""
    data = handlers.handler.start()
    with open('output.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
