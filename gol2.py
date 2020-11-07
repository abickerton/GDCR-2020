#Import required library

import numpy as np
import matplotlib.pyplot as plt

import argparse
import time

#-------------------------------------------------------------------------
class Board(object):
   def __init__(self, size, seed = 'Random', update = 0.1):
      if seed == 'Random':
         self.state = np.random.randint(2, size = size)
      self.engine = Engine(self)
      self.iteration = 0
      self.update = update
   def animate(self):
      i = self.iteration
      im = None
      plt.title("Conway's Game of Life")
      while True:
         if i == 0:
            plt.ion()
            im = plt.imshow(self.state, vmin = 0, vmax = 2, cmap = plt.cm.gray)
         else:
            im.set_data(self.state)
         i += 1
         self.engine.applyRules()
         print('Life Cycle: {} Birth: {} Survive: {}'.format(i, self.engine.nBirth, self.engine.nSurvive))
         plt.pause(self.update)
         yield self

#-------------------------------------------------------------------------

class Engine(object):
   def __init__(self, board):
      self.state = board.state
   def countNeighbors(self):
      state = self.state
      n = (state[0:-2,0:-2] + state[0:-2,1:-1] + state[0:-2,2:] +
          state[1:-1,0:-2] + state[1:-1,2:] + state[2:,0:-2] +
          state[2:,1:-1] + state[2:,2:])
      return n
   def applyRules(self):
      n = self.countNeighbors()
      state = self.state
      birth = (n == 3) & (state[1:-1,1:-1] == 0)
      survive = ((n == 2) | (n == 3)) & (state[1:-1,1:-1] == 1)
      state[...] = 0
      state[1:-1,1:-1][birth | survive] = 1
      nBirth = np.sum(birth)
      self.nBirth = nBirth
      nSurvive = np.sum(survive)
      self.nSurvive = nSurvive
      return state

#-------------------------------------------------------------------------

def main():
   ap = argparse.ArgumentParser(add_help = False) # Intilialize Argument Parser
   ap.add_argument('-h', '--height', help = 'Board Height', default = 500)
   ap.add_argument('-w', '--width', help = 'Board Width', default = 500)
   args = vars(ap.parse_args()) # Gather Arguments
   bHeight = int(args['height'])
   bWidth = int(args['width'])
   board = Board((bHeight,bWidth), update=1)

   try :
      for _ in board.animate():
         pass   
   except KeyboardInterrupt:
      print("Exit")
      exit()

#-------------------------------------------------------------------------

if __name__ == '__main__':
   main()