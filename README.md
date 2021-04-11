# QCHack-IBM-Challenge - Quantum Monopoly
Our team's submission for QCHack IBM challenege. A Quantum Monopoly game.

## QUANTUM MONOPOLY

### Participants
1. Hrushikesh Patil - hrushikesh.patil@stonybrook.edu
2. Yulun Wang - yulun.wang@stonybrook.edu
3. Rishikesh Gokhale - rishikesh.gokhale@stonybrook.edu
4. Charuta Pethe - charuta.pethe@stonybrook.edu
5. Brandonlee Santos - brandonlee.santos@stonybrook.edu

## Game Rules
Quantum Monopoly

Our team has created a fun game of quantum monopoly. 
Here the two players use the laws of quantum interference to bias the output of the quantum circuit with the help of quantum operation cards such that they land on the most favorable square (square with the highest reward). 
Beware though, your opponent also has the power to interfere in you circuit and make you less likely to win. 
This game is aimed at a gentle introduction to quantum computing and strategy.

**No of Players** - 2-4 players. (For demonstration purposes 2 players)

**Time Required** - Approx. 30 mins

### Objective of the game

The objective of the game is to introduce quantum computing concepts to high school students and beyond by the means of a fun game.
Prior knowledge of Quantum computing is not required to play. The in - game cards will explain each quantum operation to the players (planned feature).
In game objective of the players is to not go bankrupt. The game ends when only one player is left standing i.e. all other players are bankrupt.
Each players start with a fixed amount of dollars and the players navigate the quantum states earning or losing dollars till they hit zero or below zero dollars.

### Rules
#### Introduction
You are merchant who has entered the quantum country. Quantum country has many "states" which impose taxes. The rules of the country are simple and easy:

1. You can spend only one day at a any given quantum state.
2. You must always pay the tax of the quantum state.
3. If you cannot afford tax you are thrown out of the country.
4. You can only have 500$ once you enter the quantum country.
5. You become a quantum citizen if you reach 2500$.
6. There can be only one new quantum citizen, so if all other merchants drop out the last remaining merchant is automatically made quantum citizen.

Some quantum "states" are good for trade and you can make a profit after paying taxes and trading. Some quantum states are not good for trade and you may lose money in these states. The way of travelling between these cities is unique, through gateays called as the *Measurement GateWays*. This gateway is unique as it connects to all other quantum states with a twist
1. It will take you to any other quantum state with equal probability.
2. It can return you to the same state.
3. The measurement gate works only at a certain time of the day.
Fortunately for you, since you paid taxes, you are given portal stones which act of circuit of measurement gateway and can bias the measurement gateway. These portal stones must be given to a public employee one at a time. the public employee can then fix these on your gateway, or if you have been sneaky and intructed him otherwise, on you fellow merchants gateway to sabotage his travel plans. The quantum country mandates that a certain number of gates be used to trigger the measurement gate.

Armed with this info, you are now ready to travel and become a quantum citizen.
#### Rules
1. Each player is allocated 500$ at the beginning
2. Each player is dealt 8 different cards. Cards contain quantum operations of Paulis X, Y, Z and H. (More to be added soon!)
3. Each card is refreshed when used.
4. Players begin with their quantum states in equal superposition of all states.
5. Players then take turns placing their quantum cards by specifying, 1. The card to be used, 2. Whose circuit to be applied on (your's or opponent's) 3. Qubit to be applied on
6. After a fixed number of turns (8 in game however for demo purposes we may shorten it to 2) quantum measurement is triggered.
7. Quantum measuremnt will transport you to different state and depending on the state's reward your wallet will be deducted or awarded an amount.
8. If a player loses all the money, he/she is kicked out and the other player wins the game.
9. If any player reaches 2500 then he/she wins the game.

## Code Organization
We have two files QuantumGame.py and QuantumGame.ipynb. To run the game simply go 
'''
python QuantumGame.py
'''
You can also the ipynb file with jupyter notebook and run the code.

Please contact hrushikesh.patil@stonybrook.edu or yulun.wang@stonybrook.edu for further info
