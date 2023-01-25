import json
import sys

if __name__ == "__main__":
    path = sys.argv[1]
    cnt_lines = 0
    try:
        with open(path) as f:
            for line in f:
                cnt_lines += 1
                token_ids = json.loads(line)
                # print(tokenizer.decode(token_ids))
                if cnt_lines % 10000 == 0:
                    print(cnt_lines)
    except Exception as e:
        print(line)
