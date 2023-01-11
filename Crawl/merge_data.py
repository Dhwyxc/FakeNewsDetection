import pandas as pd
fn = pd.read_csv('../Data/fake_news.csv', encoding='utf-8')
rn = pd.read_csv('../Data/real_news_11.1.23.csv', encoding='utf-8')
data = pd.concat([rn, fn], ignore_index=True)
data = data.drop_duplicates()

print(data)
data.info()
label_count = data.groupby(['label'])['data'].count()
print(label_count)

data.to_csv('../Data/dataset_lasted_11.1.23.csv', encoding='utf-8', index=False)
