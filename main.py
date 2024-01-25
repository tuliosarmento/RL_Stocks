from gym import Env
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt
from uuid import uuid4
from utils import delete_duplicated_img

plt.style.use("fivethirtyeight")


class TradingEnv(Env):
    def __init__(self, data):
        self.observation_space = spaces.Dict(
            {
                "stock_value": spaces.Box(low=np.array([0]), high=np.array([500])),
                "last_day_delta": spaces.Box(low=np.array([-100]), high=np.array([100])),
                "last_day_high": spaces.Box(low=np.array([0]), high=np.array([500])),
                "last_day_low": spaces.Box(low=np.array([0]), high=np.array([500])),
                "last_day_closing": spaces.Box(low=np.array([0]), high=np.array([500])),
                # "annual_innovations": spaces.Box(low=np.array([0]), high=np.array([20])),
                # "sum_of_innovation_index": spaces.Box(low=np.array([0]), high=np.array([np.inf])),
                # "last_balance": spaces.Box(low=np.array([0]), high=np.array([np.inf])),
                "traded_volume": spaces.Box(low=np.array([0]), high=np.array([np.inf])),
            }
        )

        # self.action_space = spaces.MultiDiscrete([26 for i in range(10)])
        self.action_space = spaces.Discrete(26)

        # self.state = spaces.MultiDiscrete([0 for i in range(10)])
        self.state = 0
        self.is_in_market = False
        self.day_count = 0
        self.data = data
        self.last_buy = 0
        self.length = self.data['stock_value'].count()

        self.chart1_xvals = []
        self.chart1_yvals = []
        self.chart1_bar_yvals = []

    def _calculate_reward(self):
        #TODO Criar método de cálculo de recompensa, ponderando perdas.
        #     Provavelmente alguma abordagem com custo de oportunidade além da simples 'perda direta' de recursos.
        pass

    def step(self, action):
        self.state = action/100

        self.chart1_xvals.append(self.data['Date'].iloc[self.day_count])
        self.chart1_yvals.append(self.data['stock_value'].iloc[self.day_count])
        self.chart1_bar_yvals.append(self.state)

        current_value = self.data['stock_value'].iloc[self.day_count]
        step_reward = self.state * (self.data['Close'].iloc[self.day_count] - current_value)

        info = {}

        observation = self.data[['stock_value', 'last_day_delta', 'last_day_high', 'last_day_low', 'last_day_closing',
                                 'traded_volume']].iloc[self.day_count]
        self.day_count += 1

        if self.day_count < self.length:
            done = False
        else:
            done = True
            self.render()

        return observation, step_reward, done, info

    def render(self):
        fig, ax1 = plt.subplots()
        ax1.plot(self.chart1_xvals, self.chart1_yvals)
        ax2 = ax1.twinx()
        ax2.bar(self.chart1_xvals, self.chart1_bar_yvals, color='green')
        ax2.set_ylim(0, 1)
        ax1.set_ylim(0, 100)

        plt.savefig(f"plots/{uuid4()}.png")

    def reset(self):
        try:
            delete_duplicated_img()
        except IndexError:
            pass
        self.state = 0
        self.day_count = 0
        step_reward = 0
        done = False
        info = {}
        observation = self.observation_space.sample()
        self.chart1_xvals ,self.chart1_yvals, self.chart1_bar_yvals = [], [], []

        return observation

