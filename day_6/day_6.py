def get_marker_index(data: str, marker_type='message') -> int:
    ''' Takes the signal data and the type of marker we are looking for,
    returns the index for where the maker type starts'''

    match marker_type:
        case 'message':
            search_window = 14
        case 'packet':
            search_window = 4
        case _:
            Exception('Unknown marker type')

    for i in range(len(data)):
        marker = data[i:i + search_window]
        # if there are any repeat characters in the window the test will fail
        if len(set(marker)) == search_window:
            return i + search_window


def test_packet_algorithm() -> bool:
    ''' Returns True is the packet algorithm works on the sampel data'''
    test_signals = ['bvwbjplbgvbhsrlpgdmjqwftvncz',
                    'nppdvjthqldpwncqszvftbrmjlhg',
                    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
                    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']
    test_answers = [5, 6, 10, 11]

    index = [get_marker_index(signal, marker_type='packet') for signal in test_signals]

    return index == test_answers


def test_message_algorithm() -> bool:
    ''' Returns True is the message algorithm works on the sampel data'''
    test_signals = ['mjqjpqmgbljsphdztnvjfqwrcgsmlb',
                    'bvwbjplbgvbhsrlpgdmjqwftvncz',
                    'nppdvjthqldpwncqszvftbrmjlhg',
                    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
                    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']
    test_answers = [19, 23, 23, 29, 26]

    index = [get_marker_index(signal, marker_type='message') for signal in test_signals]

    return index == test_answers


if __name__ == "__main__":
    input_path = 'input.txt'
    with open(input_path, 'r') as f:
        data = f.read().splitlines()[0]

    # execute part 1
    part_1 = get_marker_index(data, marker_type='packet')
    if test_packet_algorithm():
        part_1_msg = 'The algorithm for detecting the packet marker passes the message starts at signal location {index}'
        print(part_1_msg.format(index=part_1))
    else:
        part_1_msg = 'The algorithm for detecting the packet marker failed'
        print(part_1_msg)

    # execute part 2
    part_2 = get_marker_index(data, marker_type='message')
    if test_message_algorithm():
        msg = 'The algorithm for detecting the message marker passes the message starts at signal location {index}'
        print(msg.format(index=part_2))
    else:
        msg = 'The algorithm for detecting the packet marker failed'
        print(msg)