import spacy
import pandas as pd
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_lg")

# todo: set as env variable for raw main table
filepath = "./data/raw/etpl_all_programsJune3.xls"

columns = [
    "NAME_1",
    "DESCRIPTION",
    "PREREQUISITES",
    "DESCRIPTION",
    "FEATURESDESCRIPTION"
]

random_state = 42
N = 100
df = pd.read_excel(filepath, usecols=columns)
small_df = df.sample(n=N, random_state=random_state)
#  need to suss this out but basically, need a giant list of words,
# ONET tech list, (maybe even skills), Credential Engine Competency framework(s)
# (https://credentialfinder.org/ , select frameworks)

# random_state, N patterns
patterns =\
    [
        # these break up small_df.iloc[0] into unstandardized tokens
        #[{'POS': 'PUNCT'}],
        ("A", [{'POS': 'CCONJ'}]),
        # modifiction that breaks up small_df.iloc[7]
        ("B", [{'ORTH': '/'}]),
        # modifiction that comnbines small_df.iloc[15], [1]
        # this should **rewrite** the rules for 0a, 1 above
        ("C", [{'ORTH': ','}]),
        # modifiction seen generally past 50 or os
        ("D", [{'ORTH': ';'}])
    ]

matcher = Matcher(nlp.vocab)

# note: the signature suggests that patterns

for pattern_name, pattern in patterns:
    matcher.add(pattern_name, None, pattern)

doc = nlp(small_df.iloc[0].PREREQUISITES)

#doc = nlp("HELLO WORLD on Google Maps.")  # Can we get away with POS, ORTH tagger only
# "H.S. diploma or GED. If not must pass the Wonderlic test."
matches = matcher(doc) #  [(14862748245026736845, 2, 3)] --> [or]

# Matcher call
# https://spacy.io/api/matcher#call
# A list of (match_id, start, end) tuples, describing the matches. A match tuple describes a span doc[start:end]. The match_id is the ID of the added match pattern.