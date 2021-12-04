from spade.agent import Agent
from main import MyBehaviour


class SimpleAgent(Agent):
    my_agent_name = ""
    neighbors = []

    async def setup(self):
        b = MyBehaviour(self.my_agent_name, self.neighbors)
        self.add_behaviour(b)

    def __init__(self, name, password, neighbors):
        super(SimpleAgent, self).__init__(name, password)
        self.my_agent_name = name
        self.neighbors = neighbors
