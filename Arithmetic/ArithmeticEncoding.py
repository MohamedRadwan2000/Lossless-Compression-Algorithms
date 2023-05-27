from decimal import Decimal
from decimal import getcontext
import decimal
import math

class ArithmeticEncoding:
    """
    ArithmeticEncoding is a class for building arithmetic encoding.
    """

    def __init__(self , message , precsion):
        getcontext().prec = precsion
        self.probability_table = self._get_probability_table(self._create_frequency_table(message))
        self.prefex_sum, self.probability_table_entity_precsion = ArithmeticEncoding.get_prefex_sum(self.probability_table)
        self._set_meta_data()

    def _set_meta_data(self):
        self.probability_table_entity_size = math.floor(math.log2(self.probability_table_entity_precsion))
        self.probability_table_size = len(self.probability_table)

    @staticmethod
    def get_prefex_sum(probability_table):
        prefex_sum = {}
        probability_table_entity_precsion = 0
        sum = Decimal(0.0)
        for key, value in probability_table.items():
            prefex_sum[key] = sum
            sum += value
            relative_difference = Decimal(sum - prefex_sum[key])
            # Determine the number of decimal places to round to
            decimal_places = -int(math.floor(relative_difference.log10()))
            # Round the difference to the determined decimal places
            difference = Decimal(round(relative_difference, decimal_places + 1))
            sum = prefex_sum[key] + difference
            probability_table[key] = difference
            probability_table_entity_precsion = max(len(difference.as_tuple().digits), probability_table_entity_precsion)
        probability_table[key] = Decimal(1.0) - prefex_sum[key]
        return prefex_sum, probability_table_entity_precsion
    
    def _get_probability_table(self, frequency_table):
        """
        Calculates the probability table out of the frequency table.
        """
        total_frequency = Decimal(sum(list(frequency_table.values())))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = Decimal(value)/total_frequency

        return probability_table
                

    def _process_stage_encode(self, stage_min, stage_max, curr_char):
        """
        Processing a stage in the encoding/decoding process.
        """
        stage_domain = stage_max - stage_min
        term_prob = Decimal(self.probability_table[curr_char])
        stage_min = Decimal(self.prefex_sum[curr_char]) * stage_domain + stage_min
        stage_max = term_prob * stage_domain + stage_min
            
        return stage_min, stage_max
    
    def _create_frequency_table(self, message):
        """
        Creates a frequency table from the message.
        """
        frequency_table = {}
        for char in message:
            frequency_table[char] = frequency_table.get(char, 0) + 1

        return frequency_table

    def encode(self, message):
        """
        Encodes a message.
        """

        #encoder = []

        start = Decimal(0.0)
        end = Decimal(1.0)

        for curr_char in (message):
            start, end = self._process_stage_encode(start, end, curr_char)

        return (start + end) / 2