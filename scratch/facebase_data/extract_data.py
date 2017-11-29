import sys

CSV = 'tdfn_gui_summary.csv'

def extract_keys():
    keys = set()
    with open(CSV, 'r') as f:
        for line in f.read().splitlines():
            keys.add(line.split(',')[1])
    return list(keys)

def get_mean_of_adults(key, adult_age=18):
    with open(CSV, 'r') as f:
        N = 0
        mean = 0
        for line in f.read().splitlines():
            columns = line.split(',')
            if columns[1] != key or columns[4] != '3':
                continue
            if float(columns[2]) >= adult_age:
                N += int(columns[5])
                mean += float(columns[6]) * int(columns[5])
    return mean / N, N

if __name__ == '__main__':
    # For vim-pymode, sys.argv[0] is this string
    if sys.argv[0] == '/must>not&exist/foo':
        if len(sys.argv) == 1:
            sys.argv += ['palpfislength_l', 'palpfislength_r']

    if len(sys.argv) == 1:
        print('use e.g. python extract_data.py palpfislength_l palpfislength_r')
        print('Keys: ')
        keys = extract_keys()
        for i in range(0, len(keys), 5):
            print(', '.join(keys[i:i+5]))
        exit()

    keys = extract_keys()
    means = {}
    Ns = {}
    for key in sys.argv[1:]:
        if key in keys:
            mean, N = get_mean_of_adults(sys.argv[1])
            means[key] = mean
            Ns[key] = N

            meta_key = key.split('_')[0]
            means[meta_key] = (means.get(meta_key, 0) * Ns.get(meta_key, 0)
                               + mean * N) / (Ns.get(meta_key, 0) + N)
            Ns[meta_key] = Ns.get(meta_key, 0) + N
    for key, N in sorted(Ns.items(), key=lambda t: t[0]):
        print(f'{key}: N: {N}, Mean: {means[key]:.2f}')
