#!/usr/bin/python3
# splitcsvcategory.py

import pandas as pd

df = pd.read_csv('~/Documents/ISI2019/reposwithexcerpts.csv')
df.drop_duplicates(inplace=True)
df.sort_values(by=['URL', 'category'], inplace=True)

print(df.to_string())
(df[df['category']=='description'])[['URL', 'excerpt']].to_csv(path_or_buf='~/Documents/ISI2019/SM2KG/data/description.csv', index=False)
(df[df['category']=='installation'])[['URL', 'excerpt']].to_csv(path_or_buf='~/Documents/ISI2019/SM2KG/data/installation.csv', index=False)
(df[df['category']=='invocation'])[['URL', 'excerpt']].to_csv(path_or_buf='~/Documents/ISI2019/SM2KG/data/invocation.csv', index=False)
(df[df['category']=='citation'])[['URL', 'excerpt']].to_csv(path_or_buf='~/Documents/ISI2019/SM2KG/data/citation.csv', index=False)
