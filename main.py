import time
import asyncio
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import random
import SimpleAgent

NUMBER_OF_AGENTS = 5
COUNTER = 0
SENDING_FLAGS = [0, 0, 0, 0, 0]
PUZZLED_NUMBERS = [0, 0, 0, 0, 0]
LIST_PROM_RESULT = [0., 0., 0., 0., 0.]
NUMBER_OF_NEIGHBORS = [0, 0, 0, 0, 0]
HOW_MANY_MESSAGE_I_RECEIVE = [0, 0, 0, 0, 0]


class MyBehaviour(CyclicBehaviour):
    my_name = ""
    my_id = -1
    my_neighbors = []
    queue_for_sending = []

    def __init__(self, my_name, my_neighbors):
        self.my_neighbors = my_neighbors
        self.queue_for_sending = my_neighbors
        self.my_name = my_name
        self.my_id = int(self.my_name[0]) - 1
        global NUMBER_OF_NEIGHBORS
        NUMBER_OF_NEIGHBORS[self.my_id] = len(self.my_neighbors)

        super().__init__()

    def delete_neighbor_from_queue(self, whom):
        temp_queue = []
        for i in self.queue_for_sending:
            if i != whom:
                temp_queue.append(i)
        self.queue_for_sending = temp_queue

    def refresh_queue_for_sending(self):
        self.queue_for_sending = self.my_neighbors

    async def on_start(self):
        global PUZZLED_NUMBERS
        PUZZLED_NUMBERS[int(self.my_name[0]) - 1] = random.randint(-100, 100)
        print(str(self.my_name) + " " + str(PUZZLED_NUMBERS[int(self.my_name[0]) - 1]))

        await asyncio.sleep(10)  # 10

    async def run(self):
        global SENDING_FLAGS, PUZZLED_NUMBERS, COUNTER, LIST_PROM_RESULT

        if SENDING_FLAGS[self.my_id] == 0:  # if the agent has not sent the numbers yet

            for neighbor in self.queue_for_sending:
                random_double = random.random()
                if random_double < 0.95:  # random number in [0 ; 1]. If >= 0.95, there was a break in communication
                    msg_s = Message(to=neighbor)

                    # the agent's number is multiplied by the interference from the segment [0.95 ; 1.05]
                    msg_s.body = str(PUZZLED_NUMBERS[self.my_id] * random.uniform(0.95, 1.05))
                    await self.send(msg_s)

                    # Если мы отправили сообщение соседу, то убираем его из очереди на отправку
                    self.delete_neighbor_from_queue(neighbor)

            if len(self.queue_for_sending) == 0:
                SENDING_FLAGS[self.my_id] = 1
                self.refresh_queue_for_sending()

        if self.my_name == "1st069823@404.city" and COUNTER == 10:
            result = PUZZLED_NUMBERS[self.my_id]
            print('\033[32m')
            print('Result (iteration ' + str(COUNTER) + ') = ' + str(result))
            print('Agent results =')
            for i in PUZZLED_NUMBERS:
                print('\t' + str(i))
            print("Finish!")
            print('\033[0m')
            exit(0)

        msg = await self.receive(timeout=1)  # 5
        if msg:
            if self.my_name != msg.sender:
                global HOW_MANY_MESSAGE_I_RECEIVE
                HOW_MANY_MESSAGE_I_RECEIVE[self.my_id] += 1

                LIST_PROM_RESULT[self.my_id] += float(msg.body) / (len(self.my_neighbors) + 1)

        # print('SENDING_FLAGS ' + str(SENDING_FLAGS))
        # print('PUZZLED_NUMBERS ' + str(PUZZLED_NUMBERS))
        # print('LIST_FROM_RESULT ' + str(LIST_PROM_RESULT))
        # print('Counter = ' + str(COUNTER) + '\n')

        global NUMBER_OF_AGENTS
        global NUMBER_OF_NEIGHBORS
        if sum(SENDING_FLAGS) == NUMBER_OF_AGENTS and sum(HOW_MANY_MESSAGE_I_RECEIVE) == 10:
            SENDING_FLAGS = [0, 0, 0, 0, 0]
            HOW_MANY_MESSAGE_I_RECEIVE = [0, 0, 0, 0, 0]

            for i in range(NUMBER_OF_AGENTS):
                LIST_PROM_RESULT[i] += (float(PUZZLED_NUMBERS[i]) / (NUMBER_OF_NEIGHBORS[i] + 1))

                PUZZLED_NUMBERS[i] = LIST_PROM_RESULT[i]
            LIST_PROM_RESULT = [0, 0, 0, 0, 0]
            COUNTER += 1

        await asyncio.sleep(1)  # 10


if __name__ == "__main__":
    simple1 = SimpleAgent.SimpleAgent("1st069823@404.city", "12345678", ["3st069823@404.city", "5st069823@404.city"])
    simple2 = SimpleAgent.SimpleAgent("2st069823@404.city", "12345678",
                                      ["4st069823@404.city", "3st069823@404.city", "5st069823@404.city"])
    simple3 = SimpleAgent.SimpleAgent("3st069823@404.city", "12345678", ["1st069823@404.city", "2st069823@404.city"])
    simple4 = SimpleAgent.SimpleAgent("4st069823@404.city", "12345678", ["2st069823@404.city"])
    simple5 = SimpleAgent.SimpleAgent("5st069823@404.city", "12345678", ["1st069823@404.city", "2st069823@404.city"])

    simple1.start()
    time.sleep(1)
    simple2.start()
    time.sleep(1)
    simple3.start()
    time.sleep(1)
    simple4.start()
    time.sleep(1)
    simple5.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    simple1.stop()
    simple2.stop()
    simple3.stop()
    simple4.stop()
    simple5.stop()
