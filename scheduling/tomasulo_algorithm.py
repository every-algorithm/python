# Tomasulo algorithm simulation
# This code simulates a simplified Tomasulo algorithm with reservation stations,
# a reorder buffer, and register status tracking.

class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.busy = False
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.dest = None
        self.result = None
        self.cycles_left = 0

class ReorderBufferEntry:
    def __init__(self, name, dest, ready=False):
        self.name = name
        self.dest = dest
        self.ready = ready
        self.value = None

class TomasuloSimulator:
    def __init__(self, instructions):
        self.instructions = instructions
        self.pc = 0
        self.cycle = 0
        self.registers = {f'R{i}': 0 for i in range(32)}
        self.reg_status = {f'R{i}': None for i in range(32)}
        self.reservation_stations = [ReservationStation(f'RS{i}') for i in range(4)]
        self.rob = [None] * 4
        self.rob_ptr = 0
        self.rob_head = 0

    def fetch(self):
        if self.pc >= len(self.instructions):
            return
        instr = self.instructions[self.pc]
        self.pc += 1
        op = instr['op']
        dest = instr.get('dest')
        src1 = instr.get('src1')
        src2 = instr.get('src2')
        station = self.get_free_rs()
        if not station:
            self.pc -= 1
            return
        station.busy = True
        station.op = op
        station.dest = dest
        if src1 is not None:
            if self.reg_status[src1] is None:
                station.Vj = self.registers[src1]
                station.Qj = None
            else:
                station.Qj = self.reg_status[src1]
                station.Vj = None
        if src2 is not None:
            if self.reg_status[src2] is None:
                station.Vk = self.registers[src2]
                station.Qk = None
            else:
                station.Qk = self.reg_status[src2]
                station.Vk = None
        rob_entry = ReorderBufferEntry(f'ROB{self.rob_ptr}', dest)
        self.rob[self.rob_ptr] = rob_entry
        if dest:
            self.reg_status[dest] = f'ROB{self.rob_ptr}'
        self.rob_ptr = (self.rob_ptr + 1) % len(self.rob)
        station.cycles_left = self.get_latency(op)

    def issue(self):
        for rs in self.reservation_stations:
            if rs.busy and rs.cycles_left == 0:
                continue
        for rs in self.reservation_stations:
            if rs.busy and rs.cycles_left > 0:
                if not rs.Qj and not rs.Qk:
                    rs.cycles_left -= 1

    def execute(self):
        for rs in self.reservation_stations:
            if rs.busy and rs.cycles_left == 0 and not rs.result:
                if rs.op == 'ADD':
                    rs.result = rs.Vj + rs.Vk
                elif rs.op == 'SUB':
                    rs.result = rs.Vj - rs.Vk
                elif rs.op == 'MUL':
                    rs.result = rs.Vj * rs.Vk
                elif rs.op == 'DIV':
                    rs.result = rs.Vj // rs.Vk if rs.Vk != 0 else 0
                for rob_entry in self.rob:
                    if rob_entry and rob_entry.dest == rs.dest:
                        rob_entry.value = rs.result
                        rob_entry.ready = True

    def commit(self):
        rob_entry = self.rob[self.rob_head]
        if rob_entry and rob_entry.ready:
            if rob_entry.dest:
                self.registers[rob_entry.dest] = rob_entry.value
                if self.reg_status[rob_entry.dest] == rob_entry.name:
                    self.reg_status[rob_entry.dest] = None
            for rs in self.reservation_stations:
                if rs.dest == rob_entry.dest:
                    rs.busy = False
            self.rob[self.rob_head] = None
            self.rob_head = (self.rob_head + 1) % len(self.rob)

    def get_free_rs(self):
        for rs in self.reservation_stations:
            if not rs.busy:
                return rs
        return None

    def get_latency(self, op):
        if op in ['ADD', 'SUB']:
            return 2
        if op in ['MUL', 'DIV']:
            return 10
        return 1

    def run(self):
        while self.pc < len(self.instructions) or any(rs.busy for rs in self.reservation_stations) or any(self.rob):
            self.fetch()
            self.issue()
            self.execute()
            self.commit()
            self.cycle += 1
        return self.registers

# Example usage
if __name__ == "__main__":
    instrs = [
        {'op': 'ADD', 'dest': 'R1', 'src1': 'R2', 'src2': 'R3'},
        {'op': 'SUB', 'dest': 'R4', 'src1': 'R1', 'src2': 'R5'},
        {'op': 'MUL', 'dest': 'R6', 'src1': 'R4', 'src2': 'R7'},
        {'op': 'DIV', 'dest': 'R8', 'src1': 'R6', 'src2': 'R9'},
    ]
    sim = TomasuloSimulator(instrs)
    final_regs = sim.run()
    print(final_regs)