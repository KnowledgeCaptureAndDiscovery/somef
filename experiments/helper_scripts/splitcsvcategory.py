#!/usr/bin/python3
# splitcsvcategory.py

import pandas as pd
import os.path 
df = pd.read_csv('~/Documents/ISI2019/reposwithexcerpts.csv')
df.drop_duplicates(inplace=True)
df.sort_values(by=['URL', 'category'], inplace=True)
if os.path.exists('../training_corpus/none.csv'):
    df_none=pd.read_csv('../training_corpus/none.csv')
    df_none=df_none.append((df[df['category']=='none'])[['URL','contributor', 'excerpt']])
    df_none.drop_duplicates(subset="excerpt").to_csv(path_or_buf='../training_corpus/none.csv', index=False)
else:
    (df[df['category']=='none']) [['URL','contributor', 'excerpt']].to_csv(path_or_buf='../training_corpus/none.csv', index=False)


if os.path.exists('../training_corpus/description.csv'):
    df_description=pd.read_csv('../training_corpus/description.csv')
    df_description=df_description.append((df[df['category']=='description']) [['URL','contributor', 'excerpt']])
    df_description.drop_duplicates(subset="excerpt").to_csv(path_or_buf='../training_corpus/description.csv', index=False)
else:
    (df[df['category']=='description']) [['URL', 'contributor','excerpt']].to_csv(path_or_buf='../training_corpus/description.csv', index=False)


if os.path.exists('../training_corpus/installation.csv'):
    df_installation=pd.read_csv('../training_corpus/installation.csv')
    df_installation=df_installation.append((df[df['category']=='installation'])[['URL','contributor', 'excerpt']])
    df_installation.drop_duplicates(subset="excerpt").to_csv(path_or_buf='../training_corpus/installation.csv', index=False)
else:
    (df[df['category']=='installation'])[['URL','contributor', 'excerpt']].to_csv(path_or_buf='../training_corpus/installation.csv', index=False)

    
if os.path.exists('../training_corpus/invocation.csv'):
    df_invocation=pd.read_csv('../training_corpus/invocation.csv')
    df_invocation=df_invocation.append((df[df['category']=='invocation'])[['URL','contributor', 'excerpt']])
    df_invocation.drop_duplicates(subset="excerpt").to_csv(path_or_buf='../training_corpus/invocation.csv', index=False)
else:
    (df[df['category']=='invocation'])[['URL', 'contributor','excerpt']].to_csv(path_or_buf='../training_corpus/invocation.csv', index=False)

if os.path.exists('../training_corpus/citation.csv'):
    df_citation=pd.read_csv('~/Documents/ISI2019/SM2KG/training_corpus/citation.csv')
    df_citation=df_citation.append((df[df['category']=='citation'])[['URL', 'contributor','excerpt']])
    df_citation.drop_duplicates(subset="excerpt").to_csv(path_or_buf='../training_corpus/citation.csv', index=False)
else:
    (df[df['category']=='citation'])[['URL','contributor','excerpt']].to_csv(path_or_buf='../training_corpus/citation.csv', index=False)
