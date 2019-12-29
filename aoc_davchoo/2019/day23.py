from collections import deque
from itertools import cycle

from .intcode import load_program, IntCodeMachine


def create_network(program):
    program = load_program(program)

    network = [(IntCodeMachine(program, i), deque()) for i in range(50)]

    for computer, queue in network:
        computer.return_output = True

    return network


def send_packets(computer: IntCodeMachine, network, nat_packets):
    while not computer.waiting_input:
        dst_address = computer.run()
        x = computer.run()
        y = computer.run()
        if dst_address is None or x is None or y is None:
            break

        if dst_address == 255:
            nat_packets.append((x, y))
        else:
            network[dst_address][1].extend((x, y))


def receive_packets(computer: IntCodeMachine, queue: deque):
    if len(queue) > 0:
        computer.set_input(list(queue))
        queue.clear()
    else:
        computer.set_input(-1)


def solve_a(data):
    network = create_network(data)
    nat_packets = []

    for computer, queue in cycle(network):
        send_packets(computer, network, nat_packets)
        receive_packets(computer, queue)
        if len(nat_packets) > 0:
            x, y = nat_packets[0]
            return y

    return -1


def solve_b(data):
    network = create_network(data)

    nat_packets = []
    nat_y_values = set()

    while True:
        for computer, queue in network:
            send_packets(computer, network, nat_packets)
            receive_packets(computer, queue)

        for computer, queue in network:
            if computer.input[0] != -1 or len(queue) > 0:
                # Computer has packets in queue
                break
        else:
            if len(nat_packets) == 0:
                # First boot up of the network
                continue
            # All computers are idle
            x, y = nat_packets[-1]
            network[0][1].extend((x, y))
            if y in nat_y_values:
                return y
            else:
                nat_y_values.add(y)
