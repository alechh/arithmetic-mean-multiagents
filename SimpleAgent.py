from spade.agent import Agent
from main import MyBehaviour


class SimpleAgent(Agent):
    my_agent_name = ""
    neighbours = []

    async def setup(self):
        b = MyBehaviour(self.my_agent_name, self.neighbours)
        self.add_behaviour(b)

    def __init__(self, name, password, neighbours):
        super(SimpleAgent, self).__init__(name, password)
        self.my_agent_name = name
        self.neighbours = neighbours
