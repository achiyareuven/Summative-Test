from app.logger import Logger
from app.enrich.utils_clear_text import to_list_pairs_words, removing_stopwords

logger = Logger.get_logger()


class TextProcessor:
    def __init__(self, list_hostile, less_hostile):
        self.list_hostile = list_hostile
        self.less_hostile = less_hostile




    def is_bds(self,score):
        return score >= 20


    def percent_bds(self,text):
        score = 0
        text_without_stopwords=removing_stopwords(text)
        list_clean_text = text_without_stopwords.lower().split()
        list_pairs_words = to_list_pairs_words(list_clean_text)
        for word in list_clean_text:
            if word in self.list_hostile:
                score += 10
            elif word in self.less_hostile:
                score += 5

        for pairs_words in list_pairs_words:
            if pairs_words in self.list_hostile:
                score += 10
            elif pairs_words in self.less_hostile:
                score += 5

        max_score = len(list_clean_text) * 2
        return round((score/max_score)*100,2)

    def bds_level(self,score):
        if score <20:
            return "none"
        if (score >= 20) and score <40 :
            return "medium"
        else:
            return "high"

    def get_dict_result_processing(self,text):
        try:
            score = self.percent_bds(text)
            level = self.bds_level(score)
            is_bds = self.is_bds(score)
            logger.info("Text analysis to add fields was successful.")
            return {
                "bds_percent":score,
                "bds_level":level,
                "is_bds":is_bds
            }

        except Exception as e:
            logger.error(f"Text parsing to add fields failed. {e}")
