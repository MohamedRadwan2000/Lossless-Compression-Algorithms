from decimal import Decimal
from decimal import getcontext
import decimal

class ArithmeticEncoding:
    """
    ArithmeticEncoding is a class for building arithmetic encoding.
    """

    def __init__(self , message):
        getcontext().prec = 16
        self.probability_table = self._get_probability_table(self._create_frequency_table(message))

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

    def _process_stage(self, stage_min, stage_max):
        """
        Processing a stage in the encoding/decoding process.
        """
        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(self.probability_table.items())):
            term = list(self.probability_table.keys())[term_idx]
            term_prob = Decimal(self.probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs
    
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

        encoder = []

        start = Decimal(0.0)
        end = Decimal(1.0)

        for curr_char in (message):
            stage_probs = self._process_stage(start, end)

            start = stage_probs[curr_char][0]
            end = stage_probs[curr_char][1]

            encoder.append(stage_probs)

        stage_probs = self._process_stage(start, end)
        encoder.append(stage_probs)

        encoded_msg = self._get_encoded_value(encoder)

        return encoder, encoded_msg

    def decode(self, encoded_msg, msg_length):
        """
        Decodes a message.
        """

        decoder = []
        decoded_msg = ""

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):
            stage_probs = self._process_stage(stage_min, stage_max)

            for msg_term, value in stage_probs.items():
                if encoded_msg >= value[0] and encoded_msg <= value[1]:
                    break

            decoded_msg = decoded_msg + msg_term
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            decoder.append(stage_probs)

        stage_probs = self._process_stage(stage_min, stage_max)
        decoder.append(stage_probs)

        return decoder, decoded_msg