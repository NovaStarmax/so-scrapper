import pandas as pd
import re
import unicodedata
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from datetime import datetime
import os
import html
from langdetect import detect

class TextMining:
    def __init__(self, df: pd.DataFrame, text_column: str = "text", language: str = "english", tokens_column="tokens"):
        self.df = df.copy()
        self.text_column = text_column
        self.language = language
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop_words = set(stopwords.words(language))
        self.stemmer = SnowballStemmer(language)
        self.lemmatizer = WordNetLemmatizer()
        self.token_column = tokens_column

    def lowercase(self):
        self.df[self.text_column] = self.df[self.text_column].fillna("").str.lower()
        return self

    def remove_accents(self):
        def strip_accents(text):
            text = unicodedata.normalize('NFD', text)
            text = text.encode('ascii', 'ignore').decode("utf-8")
            return str(text)
        self.df[self.text_column] = self.df[self.text_column].apply(strip_accents)
        return self

    def extract_target_char(self, char: str, new_column: str):
        escaped_char = re.escape(char)
        pattern = f'{escaped_char}([\\w-]+)'
        def process_text(text):
            if pd.isna(text):
                return '', text
            text = str(text)
            matches = re.findall(pattern, text)
            cleaned = re.sub(pattern, '', text)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            return ", ".join(matches), cleaned
        results = self.df[self.text_column].apply(process_text)
        self.df[new_column] = results.apply(lambda x: x[0])
        self.df[self.text_column] = results.apply(lambda x: x[1])
        return self

    def extract_url(self, url_column: str = "urls"):
        url_pattern = r"http[s]?://\S+|www\.\S+"
        self.df[url_column] = self.df[self.text_column].apply(
            lambda x: ", ".join(re.findall(url_pattern, str(x))) if pd.notna(x) else None
        )
        self.df[self.text_column] = self.df[self.text_column].apply(
            lambda x: re.sub(url_pattern, "", str(x)).strip() if pd.notna(x) else x
        )
        return self

    def clean_regex(self, columns):
        for col in columns:
            self.df[col] = self.df[col].apply(
                lambda x: re.sub(r"[^A-Za-z0-9]", " ", str(x)) if pd.notna(x) else x
            )
            self.df[col] = self.df[col].apply(
                lambda x: re.sub(r"\s+", " ", str(x)).strip() if pd.notna(x) else x
            )
        return self

    def decode_html(self):
        self.df[self.text_column] = self.df[self.text_column].apply(
            lambda x: html.unescape(str(x)) if pd.notna(x) else x
        )
        return self

    def remove_custom_noise(self, custom_words=None):
        if custom_words is None:
            custom_words = {
                            "quot", "amp", "nbsp", "lt", "gt", "rel", "nofollow", "referrer", "noreferrer", "style", "pre", "nan",
                            "text", "align", "left", "right", "div", "class", "table", "thead", "tbody", "img", "src", "alt", "code", "nomebeneficio", "deducao", "fundeb", "apoyo", "columna", "meses", "autocompasion", "parte",
                            "nomebeneficio", "deducao", "fundeb", "apoyo", "columna", "meses", "autocompasion", "parte"
}
            self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [w for w in tokens if w not in custom_words]
        )
        return self

    def tokenize(self):
        self.df[self.token_column] = self.df[self.text_column].apply(
            lambda x: self.tokenizer.tokenize(str(x)) if pd.notna(x) else []
        )
        return self

    def remove_stopwords(self):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [word for word in tokens if word.lower() not in self.stop_words]
        )
        return self

    def remove_short_tokens(self, min_len=3):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [word for word in tokens if len(word) >= min_len]
        )
        return self

    def remove_long_tokens(self, max_len=20):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [word for word in tokens if len(word) <= max_len]
        )
        return self
    
    def remove_numeric_tokens(self):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [token for token in tokens if not token.isdigit()]
        )
        return self
    
    def remove_repeated_tokens(self):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [w for i, w in enumerate(tokens) if i == 0 or w != tokens[i-1]]
        )
        return self
    
    def remove_tokens_starting_with_html_custom(self):
        prefixes = ["href", "val", "option",
                    "insert", "enter", "image", "description", "col1", "col2", "grid", "prettyprint", "override", "support", "import"]
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [t for t in tokens if not any(t.startswith(p) for p in prefixes)]
        )
        return self
    
    def filter_non_english_rows(self):
        self.df = self.df[self.df[self.text_column].apply(lambda x: detect(x) == "en")]
        return self

    def apply_stemmer(self):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [self.stemmer.stem(word) for word in tokens]
        )
        return self

    def apply_lemmatizer(self):
        self.df[self.token_column] = self.df[self.token_column].apply(
            lambda tokens: [self.lemmatizer.lemmatize(word) for word in tokens]
        )
        return self

    def build_clean_text(self, output_column: str = "clean_text"):
        self.df[output_column] = self.df[self.token_column].apply(lambda tokens: " ".join(tokens))
        return self

    def export_csv(self, name: str = None):
        data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(data_dir, exist_ok=True)
        if name is None:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            name = f"export_{timestamp}.csv"
        path = os.path.join(data_dir, name)
        self.df.to_csv(path, index=False)
        return path

    def get_df(self):
        return self.df
