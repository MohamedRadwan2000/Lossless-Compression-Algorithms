from decimal import Decimal
from decimal import getcontext
import math
from ArithmeticEncoding import ArithmeticEncoding

class ArithmeticDecoding:
    """
    ArithmeticEncoding is a class for building arithmetic encoding.
    """

    def __init__(self , probability_table , precsion):
        getcontext().prec = precsion
        self.probability_table = probability_table
        self.prefex_sum, _ = ArithmeticEncoding.get_prefex_sum(self.probability_table )


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
                

    def decode(self, encoded_msg, msg_length):
        """
        Decodes a message.
        """
        decoded_msg = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):

            msg_term, stage_min, stage_max = self._process_stage_decode(stage_min, stage_max, encoded_msg)
            decoded_msg.append(msg_term)

        return decoded_msg