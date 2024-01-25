from stable_baselines3 import A2C
from stable_baselines3.common.evaluation import evaluate_policy
from main import TradingEnv
from utils import df
from glob import glob

files = glob("initi*.zip")
env = TradingEnv(df)

if len(files) > 0:
    model = A2C.load("initialtest.zip", env, device="cuda", verbose=True)
else:
    model = A2C("MultiInputPolicy", env, device="cuda", verbose=True)

TIMESTEPS = 10000

for i in range(1, 10):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="A2C")
    model.save("initialtest")
