import spacy
from spacy.lang.en import English
from collections import Counter
import math
from query_to_text import query_to_text

#start 1. does not work well
nlp = spacy.load("en_core_web_lg")

# strat 2
# nlp_basic = English() 
# sentencizer = nlp_basic.create_pipe("sentencizer")j
# nlp_basic.add_pipe(sentencizer)

class Doc:
    def __init__(self, doc, debug = False):
        self.debug = debug
        self.preprocess(doc)


    def resentensizer(self, doc):
        doc = nlp(doc)
        i = 0
        sentences = []
        last_is_punct = None

        for sentence in doc.sents:
            if sentences == [] or last_is_punct:
                sentences.append(sentence.text)
            else:
                sentences[-1] += " " + sentence.text

            last_is_punct = sentence[-1].is_punct

        return [nlp(sentence) for sentence in sentences]



        while i < len(doc):

            if i > 0 and i == doc[i].sent.start:
                #starts a new sentence
                if not doc[i-1].is_punct: #should I merge it with prev sentence?
                    # if doc[i].is_lower: #probably, yes
                        with doc.retokenize() as retokenizer: 
                            retokenizer.merge(doc[doc[i-1].sent.start : doc[i].sent.end])

            i += 1

        return [nlp(sentence.text) for sentence in doc.sents]


    def preprocess(self, doc):
        self.sentences = self.resentensizer(doc)

        tokens = []
        for sentence in self.sentences:
            tokens += sentence
        self.word_counts = Counter(token.lemma_ for token in tokens)
        if self.debug:
            self.debugger()

    def scalar_score(self, sentence): #returns a scalar score for a sentence
        def is_important(token):     #checks if token is important word
            if self.debug:
                # print(token, token.lemma_)
                pass
            if (not token.is_ascii):
                return False
            if token.lemma_ == "-PRON-":
                return True
            if token.is_stop or token.is_punct:
                return False
            return True
        high_weight_words = ["most", "largest"]
        interesting_words = [token for token in sentence if is_important(token)]

        score = sum([self.word_counts[token.lemma_] for token in interesting_words])
        
        if sentence[0].is_stop:
            score *= 0.8
        if set([str(token.lemma_) for token in sentence]) & set(high_weight_words):
            score *= 2

        return score


    def top_k(self, k):
        #returns top k sentences
        if len(self.sentences) <= k:
            sentences = self.sentences
        else:
            
            sentence_scores = [self.scalar_score(sentence) for sentence in self.sentences]
            sentence_scores.sort()
            cutoff = sentence_scores[-k]
            sentences = [sentence for sentence in self.sentences if self.scalar_score(sentence) >= cutoff][:k]
        
        return [sentence.text for sentence in sentences]

    def debugger(self):
        print("Words: ")
        for word in self.word_counts:
            # print(word, self.word_counts[word])
            pass
        print("\n\nSentences:")
        for sentence in self.sentences:
            print("--> (", self.scalar_score(sentence), ") ", sentence, "<--")
            pass
        scalar_scores = [self.scalar_score(sentence) for sentence in self.sentences]
        scalar_scores.sort()
        print(scalar_scores)




debug = False

while True:
    doc = Doc(query_to_text(), debug=debug)
    k = int(input("Want ? out of " +str(len(doc.sentences))+" sentences: "))
    top = doc.top_k(k)
    print(" ".join(top))

    if debug:
        for i, sentence in enumerate(top):
            print(i, sentence)
    print("\n\n")