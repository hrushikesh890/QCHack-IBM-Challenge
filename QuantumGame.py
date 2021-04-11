try:
  from qiskit import *
  from qiskit.visualization import *
except ImportError:
  print("installing qiskit...")
  !pip install --pre qiskit --quiet
  print("Finished installation")
  from qiskit import *
  from qiskit.visualization import *

import matplotlib.pyplot as plt
import numpy as np
import random
class QuantumGame():
  def __init__(self):
    self.playerList = []
    for i in range (0, 2):
      self.playerList.append(Player(pid = i, wallet = 500))
    self.cardbase1 = [0]*8
    self.cardbase2 = [0]*8
    self.deal_cards()
    self.number_of_qubit = 3
    self.rewardlist = self.define_award_list()
    

  def define_award_list(self):
    award_map = {} # {index: award}
    for i in range(2**self.number_of_qubit):
      award_map[i] = np.random.randint(-self.number_of_qubit, self.number_of_qubit)*100
    return award_map

  def decimalToBinary(self, n):
    temp = str(bin(n).replace("0b", ""))
    if len(temp)<self.number_of_qubit:
      temp = "0"*(self.number_of_qubit-len(temp))+temp
    return temp

  def print_map(self):
    map = {}  # {index: state}
    for i in range(2**self.number_of_qubit):
      map[i] = self.decimalToBinary(i)
    print("***** Award Map *****")
    print()
    print(" State  :  Chances")
    rep = int(2**self.number_of_qubit/8)
    for x in range(2**self.number_of_qubit):
      print((" "+"-"*(self.number_of_qubit+2)))
      print(f"| {map[x]} | :  ${self.rewardlist[x]}")
    print((" "+"-"*(self.number_of_qubit+2)))

  def get_input(self):
    p1 = input()
    return p1


  def deal_cards(self):
    for i in range(0, len(self.cardbase1)):
      if self.cardbase1[i] == 0:
        val = self.get_card()
        if val != -1:
          self.cardbase1[i] = val
        else:
          return False
      if self.cardbase2[i] == 0:
        val = self.get_card()
        if val != -1:
          self.cardbase2[i] = val
        else:
          return False
    return True

  def get_card(self):
    idx = np.random.randint(1, 6)
    return idx

  def get_reward(self, r_state):
    intstate = int(r_state, 2)
    return self.rewardlist[intstate]

  def isbankrupt(self, pid):
    if (self.playerList[pid].get_wallet() <= 0):
      return True
    else:
      return False

  def game_over(self):
    for i in range(0, 2):
      if self.isbankrupt(i):
        print("PLAYER " + str(i) + " has lost")
        return True
      else:
        return False

  def print_current_wallets(self):
    for i in range(len(self.playerList)):
      val = self.playerList[i].get_wallet()
      print("PLAYER " + str(i) + " has: " + str(val) + "$")

  def print_current_cards(self):
    print("PLAYER 1 CARDS: " + str(self.cardbase1))
    print("PLAYER 2 CARDS: " + str(self.cardbase2))

  def player_info(self):
    self.print_current_wallets()
    self.print_current_cards()

  def initial_info(self):
    print("=========================  WELCOME TO QUANTUM MONOPOLY GAME ================================")
    print()
    self.print_map()
    self.player_info()

  def player_choice(self, pid):
    print("===========================================================================================")
    print("Enter your choice as follows separated by spaces: Card index   Target  Target-Qubit")
    inp = self.get_input()
    inList = inp.split(" ")
    if (pid == 0):
      gate = self.cardbase1[int(inList[0])] - 1
      self.cardbase1[int(inList[0])] = 0
    else:
      gate = self.cardbase2[int(inList[0])] - 1
      self.cardbase2[int(inList[0])] = 0
    self.playerList[int(inList[1])].put_gate(gate, int(inList[2]))

  def display_circuits(self):
    for i in range(len(self.playerList)):
      self.playerList[i].display_circuit()

  def trigger_measurements(self):
    for i in range(len(self.playerList)):
      val = self.playerList[i].measurement()
      reward = self.get_reward(val)
      print("PLAYER " + str(i) + " Has reached loaction " + str(int(val, 2)) + " and has won " + str(reward))
      self.playerList[i].update_wallet(reward)
      self.playerList[i].reset_and_create(val)



  def begin_game(self):
    self.initial_info()
    while(not self.game_over()):
      for i in range(0, 1):
        self.print_current_cards()
        self.player_choice(0)
        self.player_choice(1)
        self.display_circuits()
        self.deal_cards()
        
      self.trigger_measurements()
      self.player_info()

    print("Thank You for Playing")





  


class Player():
  def __init__(self, pid, wallet):
    self.pid = pid
    self.wallet = wallet
    self.circ = QuantumCircuit(3,3)
    self.reset_and_create('000')

  def reset_and_create(self, start_state):
    qc = QuantumCircuit(3, 3)
    for i in range(len(start_state)):
      if (start_state[i] == "1"):
        qc.x(i)
    qc.barrier()
    for i in range(len(start_state)):
      qc.h(i)
    qc.barrier()
    self.circ = qc

  
  def get_wallet(self):
    return self.wallet
  
  def update_wallet(self, val):
    self.wallet += val

  def put_gate(self, gate, qubit):
    # 0=I, 1=X, 2=Y, 3=Z, 4=H
    if gate==1:
      self.circ.x(qubit)
    elif gate==2:
      self.circ.y(qubit)
    elif gate==3:
      self.circ.z(qubit)
    elif gate==4:
      self.circ.h(qubit)

  def measurement(self):
    for i in range(0, 3):
      self.circ.measure(i, i)
    backend = Aer.get_backend("qasm_simulator")
    job = execute(self.circ, backend, shots=1)
    result = job.result()
    counts = result.get_counts(self.circ)
    measured = list(counts.keys())[0]
    return (measured)

  def display_circuit(self):
    display(self.circ.draw())