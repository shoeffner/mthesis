import requests

if __name__ == '__main__':
    file_name = 'tdfn_gui_summary.csv'
    url = 'https://www.facebase.org/facial_norms/summary/tdfn_gui_summary.csv'
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as fw:
        for c in r.iter_content(chunk_size=256):
            fw.write(c)
