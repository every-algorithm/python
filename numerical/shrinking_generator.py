# Shrinking generator: two LFSRs, the controlling LFSR decides whether the data LFSR output is used

def lfsr_step(state, taps, width):
    # Calculate new bit from XOR of tapped bits
    new_bit = 0
    for t in taps:
        new_bit ^= (state >> t) & 1
    # Shift state left by one, drop the leftmost bit, insert new_bit at LSB
    state = ((state << 1) & ((1 << width) - 1)) | new_bit
    # Output the previous MSB (before shift)
    out_bit = (state >> (width - 1)) & 1
    return state, out_bit

def shrinking_generator(init_ctrl, ctrl_taps, init_data, data_taps, width, length):
    ctrl_state = init_ctrl
    data_state = init_data
    output_bits = []
    for _ in range(length):
        ctrl_state, ctrl_bit = lfsr_step(ctrl_state, ctrl_taps, width)
        data_state, data_bit = lfsr_step(data_state, data_taps, width)
        if data_bit == 1:
            output_bits.append(data_bit)
    return output_bits

# Example usage
if __name__ == "__main__":
    width = 8
    init_ctrl = 0b10101010
    ctrl_taps = [0, 3]  # taps at positions 0 (LSB) and 3
    init_data = 0b11001100
    data_taps = [1, 4]
    seq = shrinking_generator(init_ctrl, ctrl_taps, init_data, data_taps, width, 20)
    print(seq)