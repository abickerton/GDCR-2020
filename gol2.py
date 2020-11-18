#Import required library

import numpy as np
import matplotlib.pyplot as plt

import argparse
#-------------------------------------------------------------------------
class Board(object):
   def __init__(self, size, initialState):
      self.iteration = 0
      self.state = initialState

   # Examine the 8 neighbouring cells and return number occupied.
   def countNeighbors(self):
      state = self.state
      n = (state[0:-2,0:-2] + state[0:-2,1:-1] + state[0:-2,2:] +
          state[1:-1,0:-2] + state[1:-1,2:] + state[2:,0:-2] +
          state[2:,1:-1] + state[2:,2:])
      return n

   def interate(self):
      self.iteration += 1
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
      #print('Life Cycle: {} Birth: {} Survive: {}'.format(self.iteration, self.nBirth, self.nSurvive))
      return state

#-------------------------------------------------------------------------

def main():
   ap = argparse.ArgumentParser(add_help = False) # Intilialize Argument Parser
   ap.add_argument('-h', '--height', help = 'Board Height', default = 500)
   ap.add_argument('-w', '--width', help = 'Board Width', default = 500)
   ap.add_argument('-u', '--update', help = 'Update time', default = 0.5)
   args = vars(ap.parse_args()) # Gather Arguments
   
   bHeight = int(args['height'])
   bWidth = int(args['width'])  
   updateTime = float(args['update'])  

   # Init board with random state
   board = Board((bHeight,bWidth), initialState=np.random.randint(2, size = (bHeight,bWidth)))
   plt.title("Conway's Game of Life")
   plt.ion()
   boardview = plt.imshow(board.state, vmin = 0, vmax = 2, cmap = plt.cm.gray)
   plt.autoscale()
   
   # Game loop
   try :
      while True:
         boardview.set_data(board.interate())
         plt.pause(updateTime)
         
   except KeyboardInterrupt:
      exit()

#-------------------------------------------------------------------------

if __name__ == '__main__':
   main()
