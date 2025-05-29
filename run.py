# import nltk
# nltk.download('punkt_tab')
# nltk.download('stopwords')
# print("dowloaded")
# from nltk.tokenize import word_tokenize

# text = "This is a test."
# tokens = word_tokenize(text)
# print(tokens)
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def extract_keywords(text="hi hello world"):
    
    # Normalize
    KNOWN_SKILLS = {"python", "java", "c++", "catia", "aws", "rest api", "ci/cd", "sql", "matlab", "tensorflow"}  # sample

    text = text.lower()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [
        token for token in tokens 
        if token not in stop_words and token not in string.punctuation
    ]

    # Match with known skills
    

    return filtered_tokens

print(extract_keywords())