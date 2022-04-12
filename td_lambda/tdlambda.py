import numpy as np
from tensorflow import keras
from keras.layers import Dense
from keras import backend
import tensorflow as tf
import random as rand


class TDLambdaAgent:

    def __init__(self, state_shape, action_shape, initialise=True,
                 alpha = 0.001, lamb=0.9, epsilon=0.1,
                 net_layers=[64, 32, 16], memory_sze=1000000,
                 experience_replay=False,  batch_size=8):

        self.alpha = alpha
        self.lamb = lamb
        self.epsilon = epsilon
        self.net_layers = net_layers
        self.num_net_layers = len(self.net_layers)

        self.action_state = action_shape
        self.state_shape = state_shape
        self.batch_size = batch_size

        self.current_episode = []
        self.memory = []
        self.memory_size = memory_sze

        self.experience_replay = experience_replay

        self.net = self.build_neural_net(initialise)
        self.net.summary()
        return

    def build_neural_net(self, initialise):
        net = keras.Sequential()
        init = tf.keras.initializers.HeUniform()
        if initialise:
            net.add(Dense(units=self.net_layers[0],
                          activation='relu',
                          input_dim=self.state_shape,
                          use_bias=False,
                          kernel_initializer=init))
            for i in range(1, self.num_net_layers):
                net.add(Dense(units=self.net_layers[i],
                              activation='relu',
                              use_bias=False,
                              kernel_initializer=init))
            net.add(Dense(units=1, activation='linear'))
            net.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.alpha),
                        loss='mse',
                        metrics=['mse'])
        else:
            return None
        return net

    def choose_action(self, possible_actions, possible_after_states, random_action=False):
        # Taking random action
        if random_action or rand.uniform(0, 1) <= self.epsilon:
            return rand.choice(possible_actions)

        # Finding highest after_state value
        max_after_state_value = self.net(possible_after_states[0].reshape(1, self.state_shape))[0][0]
        action_choices = [possible_actions[0]]
        for i in range(1, len(possible_actions)):
            value = self.net(possible_after_states[i].reshape(1, self.state_shape))[0][0]
            action = possible_actions[i]
            if value == max_after_state_value:
                action_choices.append(action)
            elif value > max_after_state_value:
                max_after_state_value = value
                action_choices = [action]
        return rand.choice(action_choices)

    def learn(self):
        if self.experience_replay:
            episodes = rand.sample(self.memory, self.batch_size)
        else:
            episodes = [self.current_episode]

        for episode in episodes:
            num_steps = len(episode)

            last_trajectory = episode[-1]
            target = last_trajectory['reward']
            if not last_trajectory['terminal']:
                target += self.net(last_trajectory['next_state'].reshape(1, self.state_shape))
            else:
                target = tf.convert_to_tensor([[target]])

            # TD(0) Update
            self.net.fit(last_trajectory['state'].reshape(1, self.state_shape),
                         target.numpy())

            # TD(Lambda) note: here's the good stuff baby
            if num_steps > 1:
                target = target - self.net(last_trajectory['state'].reshape(1, self.state_shape))
                current_learning_rate = self.alpha
                t = num_steps - 2
                while t >= 0:
                    current_learning_rate *= self.lamb
                    backend.set_value(self.net.optimizer.learning_rate, current_learning_rate)
                    current_state = episode[t]['state']
                    current_target = target + self.net(current_state.reshape(1, self.state_shape))

                    self.net.fit(current_state.reshape(1, self.state_shape), current_target)
                    t -= 1
                backend.set_value(self.net.optimizer.learning_rate, self.alpha)
        return

    def reset_for_next_episode(self):
        if len(self.current_episode) > 0:
            self.memory.append(self.current_episode.copy())
        self.current_episode = []

        if len(self.memory) > self.memory_size:
            del self.memory[0]
        return

    def save_trajectory(self, state, action, reward, next_state, terminal):
        trajectory = {'state': state,
                      'action': action,
                      'reward': reward,
                      'next_state': next_state,
                      'terminal': terminal}

        self.current_episode.append(trajectory)
        return

    def set_epsilon(self, new_value):
        self.epsilon = new_value
        return
