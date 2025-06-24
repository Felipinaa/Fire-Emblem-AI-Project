from gymnasium.envs.registration import register

register(
    id="fe_ai_gym_env/GridWorld-v0",
    entry_point="fe_ai_gym_env.envs:GridWorldEnv",
)
