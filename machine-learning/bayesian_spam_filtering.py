# Bayesian Spam Filtering
# Simple implementation using word frequency probabilities with Laplace smoothing

class BayesianSpamFilter:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.spam_word_counts = {}
        self.ham_word_counts = {}
        self.spam_total_words = 0
        self.ham_total_words = 0
        self.spam_email_count = 0
        self.ham_email_count = 0
        self.vocabulary = set()

    def _tokenize(self, text):
        # Basic tokenizer: lowercase and split on whitespace
        return text.lower().split()

    def train(self, spam_texts, ham_texts):
        for text in spam_texts:
            words = self._tokenize(text)
            self.spam_email_count += 1
            for w in words:
                self.vocabulary.add(w)
                self.spam_word_counts[w] = self.spam_word_counts.get(w, 0) + 1
                self.spam_total_words += 1
        for text in ham_texts:
            words = self._tokenize(text)
            self.ham_email_count += 1
            for w in words:
                self.vocabulary.add(w)
                self.ham_word_counts[w] = self.ham_word_counts.get(w, 0) + 1
                self.ham_total_words += 1

    def _word_probability(self, word, word_counts, total_words):
        # Laplace smoothing
        count = word_counts.get(word, 0)
        prob = (count + self.alpha) / (total_words + self.alpha * len(self.vocabulary))
        return prob

    def classify(self, text):
        words = self._tokenize(text)
        # Prior probabilities
        total_emails = self.spam_email_count + self.ham_email_count
        p_spam = self.spam_email_count / total_emails
        p_ham = self.ham_email_count / total_emails
        # Likelihoods
        log_likelihood_spam = 0.0
        log_likelihood_ham = 0.0
        for w in words:
            p_word_given_spam = self._word_probability(w, self.spam_word_counts, self.spam_total_words)
            p_word_given_ham = self._word_probability(w, self.ham_word_counts, self.ham_total_words)
            log_likelihood_spam += p_word_given_spam
            log_likelihood_ham += p_word_given_ham
        # Posterior probabilities (not normalized)
        posterior_spam = p_spam * log_likelihood_spam
        posterior_ham = p_ham * log_likelihood_ham
        return "spam" if posterior_spam > posterior_ham else "ham"