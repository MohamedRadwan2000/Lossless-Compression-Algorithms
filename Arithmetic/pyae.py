from decimal import Decimal
from decimal import getcontext
import decimal

class ArithmeticEncoding:
    """
    ArithmeticEncoding is a class for building arithmetic encoding.
    """

    def __init__(self , message , precsion):
        getcontext().prec = precsion
        self.probability_table = self._get_probability_table(self._create_frequency_table(message))
        self.prefex_sum = self._get_prefex_sum()

    def _get_prefex_sum(self):
        prefex_sum = {}
        sum = 0.0
        for key, value in self.probability_table.items():
            prefex_sum[key] = sum
            sum += value
        return prefex_sum
    
    def _get_probability_table(self, frequency_table):
        """
        Calculates the probability table out of the frequency table.
        """
        total_frequency = sum(list(frequency_table.values()))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = (value/total_frequency)

        return probability_table

    def _get_encoded_value(self, encoder):
        """
        After encoding the entire message, this method returns the single value that represents the entire message.
        """
        last_stage = list(encoder[-1].values())
        last_stage_values = []
        for sublist in last_stage:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)

        return (last_stage_min + last_stage_max)/2

    def _process_stage_decode(self, stage_min, stage_max, encoded_msg):
        """
        Processing a stage in the encoding/decoding process.
        """
        
        stage_domain = stage_max - stage_min

        for msg_term, value in self.probability_table.items():
            term_prob = Decimal(value)
            start = Decimal(self.prefex_sum[msg_term]) * stage_domain + stage_min
            end = term_prob * stage_domain + start
            if encoded_msg >= start and encoded_msg <= end:
                return msg_term, start, end
                

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

            #encoder.append(stage_probs)

        #stage_probs = self._process_stage(start, end)
        #encoder.append(stage_probs)

        #encoded_msg = self._get_encoded_value(encoder)

        return (start + end) / 2

    def decode(self, encoded_msg, msg_length):
        """
        Decodes a message.
        """

        decoder = []
        decoded_msg = ""

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):

            msg_term, stage_min, stage_max = self._process_stage_decode(stage_min, stage_max, encoded_msg)
            decoded_msg = decoded_msg + msg_term

        return decoded_msg