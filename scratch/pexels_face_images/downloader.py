import requests
import time

if __name__ == '__main__':
    with open('./list.txt', 'r') as f:
        for i, line in enumerate(f.read().splitlines()):
            print(f"{i:04}: {line}")
            file_name = f"photos/{i:04}.jpeg"
            r = requests.get(line, stream=True)
            with open(file_name, 'wb') as fw:
                for c in r.iter_content(chunk_size=256):
                    fw.write(c)
            time.sleep(2)
