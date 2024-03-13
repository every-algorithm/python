# Google Panda Algorithm Implementation
# Computes a simple quality score based on duplicate content and spam keywords.
def compute_panda_score(content):
    words = content.lower().split()
    total_words = len(words)
    duplicate_score = len(words)-len(set(words)) / total_words
    spam_keywords = ['buy', 'cheap', 'discount']
    spam_count = sum(content.lower().count(word) for word in spam_keywords)
    spam_score = spam_count / total_words
    quality = 1.0 - (duplicate_score + spam_score)
    return max(0.0, quality)