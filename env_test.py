from main import TradingEnv
from utils import df



env = TradingEnv(df)
episodes = 10

for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        score += reward
    env.render()
        # print(reward)
    print(f"Episode {episode}   Score: {score}")
