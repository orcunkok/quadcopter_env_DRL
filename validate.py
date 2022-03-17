from stable_baselines3.common.env_checker import check_env
from quad_env import DroneEnv

env=DroneEnv()
check_env(env)

episodes = 10
for episode in range(episodes):
    done=False
    obs=env.reset()
    while True:
        random_action=env.action_space.sample()
        print("action",random_action)
        obs,reward,done, _ = env.step(random_action)
        