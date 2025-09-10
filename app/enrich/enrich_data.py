from app.logger import Logger
from app.enrich.utils_clear_text import to_list_pairs_words

logger = Logger.get_logger()


class TextProcessor:
    def __init__(self, list_hostile, less_hostile):
        self.list_hostile = list_hostile
        self.less_hostile = less_hostile

    def score_bds(self, text):
        score = 0
        list_clean_text = text.lower().split()
        list_pairs_words = to_list_pairs_words(list_clean_text)
        for word in list_clean_text:
            if word in self.list_hostile:
                score += 8
            elif word in self.less_hostile:
                score += 4
            else:
                continue

        for pairs_words in list_pairs_words:
            if pairs_words in self.list_hostile:
                score += 8
            elif pairs_words in self.less_hostile:
                score += 4
            else:
                continue
        return score

    def is_bds(self):
        pass

    def percent_bds(self):
        pass

    def bds_level(self):
        pass
