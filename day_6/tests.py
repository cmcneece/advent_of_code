import unittest
from day_6 import get_marker_index


class TestSignalMethods(unittest.TestCase):

    def test_packet_algorithm(self):
        ''' Returns True is the packet algorithm works on the sampel data'''
        test_signals = ['bvwbjplbgvbhsrlpgdmjqwftvncz',
                        'nppdvjthqldpwncqszvftbrmjlhg',
                        'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
                        'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']
        test_answers = [5, 6, 10, 11]

        index = [get_marker_index(signal, marker_type='packet') for signal in test_signals]

        self.assertEqual(test_answers, index)

    def test_message_algorithm(self):
        ''' Returns True is the packet algorithm works on the sampel data'''
        test_signals = ['mjqjpqmgbljsphdztnvjfqwrcgsmlb',
                        'bvwbjplbgvbhsrlpgdmjqwftvncz',
                        'nppdvjthqldpwncqszvftbrmjlhg',
                        'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
                        'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']
        test_answers = [19, 23, 23, 29, 26]

        index = [get_marker_index(signal, marker_type='message') for signal in test_signals]

        self.assertEqual(test_answers, index)


if __name__ == '__main__':
    unittest.main()
