def get_marker_index(data: str, marker_type: str = 'message') -> int:
    ''' Takes the signal data and the type of marker we are looking for,
    returns the index for where the maker type starts '''

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


if __name__ == "__main__":
    input_path = 'input.txt'
    with open(input_path, 'r') as f:
        data = f.read().splitlines()[0]

    # execute part 1
    part_1 = get_marker_index(data, marker_type='packet')
    part_1_msg = 'The packet marker is at signal location {index}'
    print(part_1_msg.format(index=part_1))

    # execute part 2
    part_2 = get_marker_index(data, marker_type='message')
    msg = 'The message marker is at signal location {index}'
    print(msg.format(index=part_2))
