import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('pexels.csv')
    for id in (set(range(120)) - set(df['id'].values)):
        print(f'../pexels_face_images/resized/{id:0>4}.jpeg')
