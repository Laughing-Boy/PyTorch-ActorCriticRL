import torch
import torch.nn as nn
import torch.nn.functional as F

EPS = 0.0001

class Critic(nn.Module):

	def __init__(self, state_dim, action_dim):
		"""
		:param state_dim: Dimension of input state (int)
		:param action_dim: Dimension of input action (int)
		:return:
		"""
		super(Critic, self).__init__()

		self.state_dim = state_dim
		self.action_dim = action_dim

		self.fcs1 = nn.Linear(state_dim,128)
		self.fca1 = nn.Linear(action_dim,128)

		self.fc2 = nn.Linear(256,128)
		self.fc3 = nn.Linear(128,1)

	def forward(self, state, action):
		"""
		returns Value function Q(s,a) obtained from critic network
		:param state: Input state (Torch Variable : [n,state_dim] )
		:param action: Input Action (Torch Variable : [n,action_dim] )
		:return: Value function : Q(S,a) (Torch Variable : [n,1] )
		"""
		s1 = F.relu(self.fcs1(state))
		a1 = F.relu(self.fca1(action))
		x = torch.cat((s1,a1),dim=1)

		x = F.relu(self.fc2(x))
		x = self.fc3(x)

		return x


class Actor(nn.Module):

	def __init__(self, state_dim, action_dim, action_lim):
		"""
		:param state_dim: Dimension of input state (int)
		:param action_dim: Dimension of output action (int)
		:param action_lim: Used to limit action in [-action_lim,action_lim]
		:return:
		"""
		super(Actor, self).__init__()

		self.state_dim = state_dim
		self.action_dim = action_dim
		self.action_lim = action_lim

		self.fc1 = nn.Linear(state_dim,128)
		self.fc2 = nn.Linear(128,64)
		self.fc3 = nn.Linear(64,action_dim)

	def forward(self, state):
		"""
		returns policy function Pi(s) obtained from actor network
		this function is a gaussian prob distribution for all actions
		with mean lying in (-1,1) and sigma lying in (0,1)
		The sampled action can , then later be rescaled
		:param state: Input state (Torch Variable : [n,state_dim] )
		:return: Output action (Torch Variable: [n,action_dim] )
		"""
		x = F.relu(self.fc1(state))
		x = F.relu(self.fc2(x))
		action = F.tanh(self.fc3(x))

		action = action * self.action_lim

		return action



