"""
Text Preprocessing and Cleaning Module.
Provides tokenization, stopword filtering, text normalization, and entity masking.
Academic context: Maps to Unit 1 (NLP Foundations & Text Preprocessing) of PES University UE24AM343AB5.
"""

import re
import unicodedata
from typing import List, Dict, Any, Tuple

# Comprehensive English stopwords list (eliminates external nltk download dependency)
ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", 
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", 
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
    "yours", "yourself", "yourselves"
}

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
PHONE_REGEX = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}')
URL_REGEX = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
LINKEDIN_REGEX = re.compile(r'linkedin\.com/in/[\w-]+', re.IGNORECASE)
GITHUB_REGEX = re.compile(r'github\.com/[\w-]+', re.IGNORECASE)


def normalize_text(text: str) -> str:
    """Normalize unicode characters, remove weird symbols, standardize whitespace."""
    if not text:
        return ""
    # Normalize unicode to NFKD form
    text = unicodedata.normalize('NFKD', text)
    # Replace non-breaking spaces and tabs
    text = text.replace('\xa0', ' ').replace('\t', ' ')
    # Replace multiple spaces with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace multiple newlines with at most two newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extract email, phone, LinkedIn, and GitHub links from text."""
    emails = EMAIL_REGEX.findall(text)
    phones = PHONE_REGEX.findall(text)
    # Clean phone numbers
    phone_clean = []
    for match in re.finditer(PHONE_REGEX, text):
        raw_p = match.group().strip()
        if len(re.sub(r'\D', '', raw_p)) >= 10:
            phone_clean.append(raw_p)

    linkedin_matches = LINKEDIN_REGEX.findall(text)
    github_matches = GITHUB_REGEX.findall(text)

    return {
        "emails": list(set(emails)),
        "phones": list(set(phone_clean)),
        "linkedin": list(set(linkedin_matches)),
        "github": list(set(github_matches))
    }


def clean_text_for_nlp(text: str, remove_stopwords: bool = True, lowercase: bool = True) -> str:
    """
    Clean text for classical NLP algorithms (TF-IDF, Cosine Similarity).
    Keeps alphanumeric characters and key technical punctuation (+, # for C++, C#).
    """
    if not text:
        return ""
    
    text = normalize_text(text)
    
    # Preserve technical terms like C++, C#, .NET
    text = re.sub(r'\bC\+\+', 'cpp_lang', text)
    text = re.sub(r'\bC#', 'csharp_lang', text)
    text = re.sub(r'\.NET\b', 'dotnet_framework', text, flags=re.IGNORECASE)
    
    if lowercase:
        text = text.lower()
        
    # Remove email addresses and URLs
    text = EMAIL_REGEX.sub(' ', text)
    text = URL_REGEX.sub(' ', text)
    
    # Remove punctuation except underscores
    text = re.sub(r'[^a-zA-Z0-9_\s]', ' ', text)
    
    # Tokenize
    tokens = text.split()
    
    # Restore placeholders
    restored_tokens = []
    for t in tokens:
        if t == 'cpp_lang':
            restored_tokens.append('c++')
        elif t == 'csharp_lang':
            restored_tokens.append('c#')
        elif t == 'dotnet_framework':
            restored_tokens.append('.net')
        else:
            restored_tokens.append(t)
            
    if remove_stopwords:
        restored_tokens = [t for t in restored_tokens if t.lower() not in ENGLISH_STOPWORDS and len(t) > 1]
        
    return ' '.join(restored_tokens)


def tokenize_sentences(text: str) -> List[str]:
    """Segment text into individual sentences for evidence citation."""
    if not text:
        return []
    # Split on sentence boundaries
    raw_sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 5]
    return sentences
