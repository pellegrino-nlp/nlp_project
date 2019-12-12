import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

def normalize(string):
    """
    Convert to all lowercase  
    Normalize the unicode chars  
    Remove any non-alpha or whitespace characters  
    Remove any alpha strings with 2 characters or less  
    """
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # keep only alpha chars
    string = re.sub(r'[^a-z]', ' ', string)
    
    # remove strings less than 2 chars in length
    string = re.sub(r'\b[a-z]{,2}\b', '', string)
    
    # convert newlines and tabs to a single space
    string = re.sub(r'[\r|\n|\r\n]+', ' ', string)
    
    # strip extra whitespace
    string = string.strip()
    
    return string


def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string_of_stems = ' '.join(stems)
    return string_of_stems

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string_of_lemmas = ' '.join(lemmas)
    return string_of_lemmas

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string, return_str=True)

extra_words = ['http', 'https', 'www', 'banner', 'request', 'img', 'com', 'png', 'welcome',
                'doctype', 'abbr', 'address', 'base', 'body', 'src',
                'br', 'div' , 'org', 'icu', 'href', 'image', 'logo', 'github']

def remove_stopwords(tokenized_string, extra_words=extra_words, exclude_words=[]):
    words = tokenized_string.split()
    stopword_list = stopwords.words('english')

    # remove the excluded words from the stopword list
    stopword_list = set(stopword_list) - set(exclude_words)

    # add in the user specified extra words
    stopword_list = stopword_list.union(set(extra_words))

    filtered_words = [w for w in words if w not in stopword_list]
    final_string = " ".join(filtered_words)
    return final_string

def prep_articles(df):
    df = df.assign(original = df.readme_contents)
    df = df.assign(normalized = df.original.apply(normalize))
    df = df.assign(stemmed = df.normalized.apply(stem))
    df = df.assign(lemmatized = df.normalized.apply(lemmatize))
    df = df.assign(cleaned = df.lemmatized.apply(remove_stopwords))
    df.drop(columns=(["readme_contents", "repo"]), inplace=True)
    return df

def word_freq(dfx, language="language", cleaned="cleaned"):
    # create list of words by language

    js_words = ' '.join(dfx[dfx[language] == 'JavaScript'][cleaned]).split()
    p_words = ' '.join(dfx[dfx[language] == 'Python'][cleaned]).split()
    j_words = ' '.join(dfx[dfx[language] == 'Java'][cleaned]).split()
    php_words = ' '.join(dfx[dfx[language] == 'PHP'][cleaned]).split()
    go_words = ' '.join(dfx[dfx[language] == 'Go'][cleaned]).split()
    jup_words = ' '.join(dfx[dfx[language] == 'Jupyter Notebook'][cleaned]).split()
    html_words = ' '.join(dfx[dfx[language] == 'HTML'][cleaned]).split()
    swift_words = ' '.join(dfx[dfx[language] == 'Swift'][cleaned]).split()
    ts_words = ' '.join(dfx[dfx[language] == 'TypeScript'][cleaned]).split()
    ruby_words = ' '.join(dfx[dfx[language]== 'Ruby'][cleaned]).split()
    cpp_words = ' '.join(dfx[dfx[language] == 'C++'][cleaned]).split()
    css_words = ' '.join(dfx[dfx[language] == 'CSS'][cleaned]).split()
    shell_words = ' '.join(dfx[dfx[language] == 'Shell'][cleaned]).split()
    c_words = ' '.join(dfx[dfx[language] == 'C'][cleaned]).split()
    csharp_words = ' '.join(dfx[dfx[language] == 'C#'][cleaned]).split()
    all_words = ' '.join(dfx[cleaned]).split()

    # create Series of word frequency by language

    js_freq = pd.Series(js_words).value_counts()
    p_freq = pd.Series(p_words).value_counts()
    j_freq = pd.Series(j_words).value_counts()
    php_freq = pd.Series(php_words).value_counts()
    go_freq = pd.Series(go_words).value_counts()
    jup_freq = pd.Series(jup_words).value_counts()
    html_freq = pd.Series(html_words).value_counts()
    swift_freq = pd.Series(swift_words).value_counts()
    ts_freq = pd.Series(ts_words).value_counts()
    ruby_freq = pd.Series(ruby_words).value_counts()
    cpp_freq = pd.Series(cpp_words).value_counts()
    css_freq = pd.Series(css_words).value_counts()
    shell_freq = pd.Series(shell_words).value_counts()
    c_freq = pd.Series(c_words).value_counts()
    csharp_freq = pd.Series(csharp_words).value_counts()
    all_freq = pd.Series(all_words).value_counts()

    # Combine Series' together into df
    word_counts = (pd.concat([all_freq, js_freq, p_freq, j_freq, php_freq, go_freq, jup_freq, html_freq, swift_freq, ts_freq, ruby_freq, cpp_freq, css_freq, c_freq, csharp_freq], axis=1, sort=True)
     .set_axis(['all', 'javascript', 'python', 'java', 'php', 'go', 'jupyter_notebook', 'html', 'swift', 'typescript', 'ruby', 'C+', 'CSS', 'C', 'C#'], axis=1, inplace=False)
     .fillna(0)
     .apply(lambda s: s.astype(int)))
    
    return word_counts