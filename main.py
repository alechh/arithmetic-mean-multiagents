import time
import asyncio
import ast
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from random import randint
import SimpleAgent

NUMBER_OF_AGENTS = 5
NUMBER_OF_RECEIVED_NUMBERS = 0


class MyBehaviour(CyclicBehaviour):
    my_name = ""
    my_work_result = 0
    my_neighbours = []
    all_my_info = {}

    def __init__(self, my_name, my_neighbours):
        self.my_neighbours = my_neighbours
        self.my_name = my_name
        self.all_my_info = {self.my_name: -1}
        super().__init__()

    async def on_start(self):
        self.my_work_result = randint(-1000, 1000)
        self.all_my_info.update({self.my_name: self.my_work_result})
        await asyncio.sleep(5)

    async def run(self):
        for neighbour in self.my_neighbours:
            msg_s = Message(to=neighbour)
            msg_s.body = str(self.all_my_info)
            # print('\t' + str(self.my_name) + ' отправил сообщение ' + neighbour)
            await self.send(msg_s)

        if self.my_name == "1st069823@404.city":
            global NUMBER_OF_RECEIVED_NUMBERS
            if NUMBER_OF_RECEIVED_NUMBERS != len(self.all_my_info):
                NUMBER_OF_RECEIVED_NUMBERS += 1
                print(str(len(self.all_my_info)) + '/' + str(NUMBER_OF_AGENTS))

            if len(self.all_my_info) == NUMBER_OF_AGENTS:
                print('Result:\t' + str(sum(self.all_my_info.values()) / NUMBER_OF_AGENTS))
                for value in self.all_my_info.values():
                    print('\t' + str(value))
                print("Finished!")
                exit(0)

        msg = await self.receive(timeout=2)  # 5
        if msg:
            self.all_my_info.update(ast.literal_eval(msg.body))

        await asyncio.sleep(1)  # 3


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
