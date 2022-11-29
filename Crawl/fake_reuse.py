from csv import writer
import pandas as pd
import re
data = []
def reprocess(dt):
    for d in dt:
        if len(d) > 10:
            d = re.sub(r'<[^>]*>', '', d)
            d = re.sub(r'http\S+', '', d)
            d = d.replace('\n', ' ')
            d = re.sub(r'[,;%{}$*+!=-]', '', d)
            d = re.sub(r'[\s]+', ' ', d)
            data.append([d, 1])

dfa = pd.read_csv('../Data/reuse/public_train.csv',encoding='utf-8')
dfb = pd.read_excel('../Data/reuse/warmup_training_dataset.xlsx')
dfc = pd.read_csv('../Data/reuse/vn_news_226_tlfr.csv', encoding='utf-8')
dfa = dfa.groupby('label')
dfa_one = dfa.get_group(1)['post_message']
dfb = dfb.groupby('label')
dfb_one = dfb.get_group(1)['post_message']
dfc = dfc.groupby('label')
dfc_one = dfc.get_group(1)['text']
reprocess(dfa_one)
reprocess(dfb_one)
reprocess(dfc_one)

with open('../Data/fake_news.csv', 'a',encoding='utf-8') as f:
    writer_object = writer(f)
    writer_object.writerows(data)

fn = pd.read_csv('../Data/fake_news.csv', encoding='utf-8')
print(fn)
label_count = fn.groupby(['label'])['data'].count()
print(label_count)
print(fn.isnull().values.any())
fn = fn.drop_duplicates()
label_count_after = fn.groupby(['label'])['data'].count()
print(label_count_after)
fn.to_csv('../Data/fake_news.csv', encoding='utf-8', index=False)
