import pickle
import matplotlib.pyplot as plt

with open('expResults/sarsa1.pickle', 'rt') as f:
    sarsa = pickle.load( f )

with open('expResults/Q1.pickle', 'rt') as f:
    q = pickle.load( f )

with open('expResults/sarsa01.pickle', 'rt') as f:
    sarsa01 = pickle.load( f )
with open('expResults/Q01.pickle', 'rt') as f:
    q01 = pickle.load( f )

f, axarr = plt.subplots( 2 )
l = 5000
axarr[0].plot(range(l), sarsa[:l], color='r', label="SARSA")
axarr[0].plot(range(l), q[:l], color='g', label="Q-learning")
axarr[0].set_title("Optimistic intial state action values ( 1.0 )")
axarr[0].set_ylabel("Average reward")
axarr[0].set_xlabel("Number of episodes experienced")
axarr[1].plot(range(l), sarsa01[:l], color='r', label="SARSA")
axarr[1].plot(range(l), q01[:l], color='g', label="Q-learning")
axarr[1].set_title("Optimistic intial state action values ( 0.01 )")
axarr[1].set_ylabel("Average reward")
axarr[1].set_xlabel("Number of episodes experienced")
axarr[0].legend( loc='best' )
axarr[1].legend( loc='best' )
plt.tight_layout()
plt.savefig('graphs/SARSAvsQ.png')
plt.show()

with open('expResults/sarsa01.pickle', 'rt') as f:
    symmetric = pickle.load( f )

with open('expResults/noSymmetry.pickle', 'rt') as f:
    noSymmetry = pickle.load( f )

with open('expResults/Q01.pickle', 'rt') as f:
    Qsymmetric = pickle.load( f )

with open('expResults/QnoSymmetry.pickle', 'rt') as f:
    QnoSymmetry = pickle.load( f )

f, axarr = plt.subplots( 2 )
axarr[0].plot(range(l), symmetric[:l], color='r', label="With symmetry")
axarr[0].plot(range(l), noSymmetry[:l], color='g', label="Without symmetry")
axarr[0].set_title("Effect of symmetry (SARSA algorithm)")
axarr[0].set_ylabel("Average reward")
axarr[0].set_xlabel("Number of episodes experienced")
axarr[1].plot(range(l), Qsymmetric[:l], color='r', label="With symmetry")
axarr[1].plot(range(l), QnoSymmetry[:l], color='g', label="Without symmetry")
axarr[1].set_title("Effect of symmetry (Q algorithm)")
axarr[1].set_ylabel("Average reward")
axarr[1].set_xlabel("Number of episodes experienced")
axarr[0].legend( loc='best' )
axarr[1].legend( loc='best' )
plt.tight_layout()
plt.savefig('graphs/Symmetry.png')
plt.show()
