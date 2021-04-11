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
        print("------------------------ The Map of Award ------------------------\n")
        print(" "*24+"| State  :  Chances |\n")
        rep = int(2**self.number_of_qubit/8)
        for x in range(2**self.number_of_qubit):
            print((" "*26+"-"*(self.number_of_qubit+2)))
            print(" "*25+f"| {map[x]} | :  ${self.rewardlist[x]}")
        print((" "*26+"-"*(self.number_of_qubit+2)))
        print("-----------------------------------------------------------------------")
  
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
        idx = np.random.randint(2, 6)
        return idx

    def get_reward(self, r_state):
        intstate = int(r_state, 2)
        return self.rewardlist[intstate]

    def isbankrupt(self, pid):
        if (self.playerList[pid].get_wallet() <= 0 or self.playerList[pid].get_wallet() >= 2500):
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
            print("==> PLAYER " + str(i) + " has: " + str(val) + "$")

    def card_dictionary(self,cardbase):
        card_dict = {"I":1, "X":2, "Y":3, "Z":4, "H":5}
        if type(cardbase[0])==int:
            cardletter = [list(card_dict.keys())[i-1] for i in cardbase]
        elif type(cardbase[0])==str:
            cardletter = [int(card_dict[i]) for i in cardbase]
        return cardletter

    def print_current_cards(self):  
        print("==> PLAYER 1 CARDS: " + str(self.card_dictionary(self.cardbase1)))
        print("==> PLAYER 2 CARDS: " + str(self.card_dictionary(self.cardbase2)))

    def player_info(self):
        self.print_current_wallets()
        self.print_current_cards()
    

    def initial_info(self):
        print("=========================  WELCOME TO QUANTUM MONOPOLY GAME ================================\n")
        print("Two players use the laws of quantum interference to bias the output of the quantum") 
        print("circuit with the help of quantum operation cards such that they land on the most ")
        print("favorable square (square with the highest reward). Beware though, your opponent also has") 
        print("the power to interfere in you circuit and make you less likely to win. This game is")
        print(" aimed at a gentle introduction to quantum computing and strategy.")
        print('\n * During the game, you can type in "stop" to end the game.\n')
        self.print_map()
    
 
    def player_choice(self, pid):
        print(f"--> It's Player {pid}'s turn:")
        print("Enter your choice as follows separated by spaces: Card index  Target-Player  Target-Qubit")
        inp = self.get_input()
        input_checker = False
        while input_checker==False:
            if inp=="stop":
                print("Game Stop.")
                break
                exit()
            try:
                pre_inList = inp.split(" ")
                inList = []
                inList.append(int(self.card_dictionary([pre_inList[0]])[0]))
                inList.append(int(pre_inList[1]))
                inList.append(int(pre_inList[2]))
                if pid ==0 and (inList[0] in self.cardbase1) and (inList[1] in [0,1]) and (inList[2] in [0,1,2]):
                    input_checker = True
                elif pid ==1 and (inList[0] in self.cardbase2) and (inList[1] in [0,1]) and (inList[2] in [0,1,2]):
                    input_checker = True
                else:
                    print("Wrong input format! Please double check your cardbase and re-enter your choice!")
                    inp = self.get_input()
            except: 
                print("Wrong input format! Please re-enter your choice, for example: X 0 1")
                inp = self.get_input()

        if (pid == 0):
            self.cardbase1.remove(int(inList[0]))
        else:
            self.cardbase2.remove(int(inList[0]))
        self.playerList[int(inList[1])].put_gate(int(inList[0]), int(inList[2]))

    def display_circuits(self):
        for i in range(len(self.playerList)):
            print(f"############# Player {i}'s circuit #############'")
            self.playerList[i].display_circuit()
            self.playerList[i].get_statevector()

    def trigger_measurements(self):
        print("************************************")
        print("Be careful! Measurement initiated!")
        print("Ooops! Your quantum state collapes!")
        for i in range(len(self.playerList)):
            val = self.playerList[i].measurement()
            reward = self.get_reward(val)
            if reward>0:
                print(f"PLAYER {i} jumped to location {str(int(val, 2))}: {val}. PLAYER {i} has won ${reward}!")
            elif reward<0:
                print(f"PLAYER {i} jumped to location {str(int(val, 2))}: {val}. PLAYER {i} has lost ${-reward}!")
            else:
                print(f"PLAYER {i} jumped to location {str(int(val, 2))}: {val}. Nothing happened!")
            self.playerList[i].update_wallet(reward)
            self.playerList[i].reset_and_create(val)
        print()
        
    def begin_game(self):
        self.initial_info()
        round = 1
        while(not self.game_over()):
            print(f"========================== No. {round} Round ==========================")
            self.player_info()
            self.player_choice(0)
            self.player_choice(1)
            print("----------------------------------------------------------------------------")
            self.display_circuits()
            self.deal_cards()
            self.trigger_measurements()
            round += 1
        print("Thank You for Playing!")

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
        # 1=I, 2=X, 3=Y, 4=Z, 5=H
        if gate==2:
            self.circ.x(qubit)
        elif gate==3:
            self.circ.y(qubit)
        elif gate==4:
            self.circ.z(qubit)
        elif gate==5:
            self.circ.h(qubit)
        self.circ.barrier()

    def measurement(self):
        for i in range(0, 3):
            self.circ.measure(i, i)
        backend = Aer.get_backend("qasm_simulator")
        job = execute(self.circ, backend, shots=1)
        result = job.result()
        counts = result.get_counts(self.circ)
        measured = list(counts.keys())[0]
        return (measured)
    
    def get_statevector(self):
        svsim = Aer.get_backend('statevector_simulator')
        qobj = assemble(self.circ)    
        result = svsim.run(qobj).result()
        out_state = result.get_statevector()
        print(f"You are now in the state: ({out_state[0]})|0> + ({out_state[1]})|1>\n")

    def display_circuit(self):
        display(self.circ.draw())


q = QuantumGame()
q.begin_game()