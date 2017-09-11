from __future__ import division
import gym
import numpy as np
import torch
from torch.autograd import Variable

import train
import buffer

# env = gym.make('BipedalWalker-v2')
env = gym.make('Pendulum-v0')

MAX_EPISODES = 1000
MAX_STEPS = 50
MAX_BUFFER = 256
MAX_TOTAL_REWARD = 300
S_DIM = env.observation_space.shape[0]
A_DIM = env.action_space.shape[0]
A_MAX = env.action_space.high[0]

print ' State Dimensions :- ', S_DIM
print ' Action Dimensions :- ', A_DIM
print ' Action Max :- ', A_MAX

ram = buffer.MemoryBuffer(MAX_BUFFER)
trainer = train.Trainer(S_DIM, A_DIM, ram)

for _ep in range(MAX_EPISODES):
	observation = env.reset()
	for r in range(MAX_STEPS):
		env.render()
		state = np.float32(observation)

		# get action based on observation, use exploration policy here
		action = trainer.get_exploration_action(state)
		rescaled_action = action*A_MAX
		rescaled_action = np.maximum(rescaled_action, -A_MAX * np.ones_like(rescaled_action))
		rescaled_action = np.minimum(rescaled_action, A_MAX * np.ones_like(rescaled_action))
		# print '---------------'
		# print rescaled_action
		new_observation, reward, done, info = env.step(rescaled_action)
		action = rescaled_action/A_MAX

		reward /= MAX_TOTAL_REWARD

		if done:
			new_state = None
		else:
			new_state = np.float32(new_observation)
			# push this exp in ram
			ram.add(state, action, reward, new_state)

		observation = new_observation

		# perform optimization
		trainer.optimize()
		if done:
			break

print 'Completed episodes'
