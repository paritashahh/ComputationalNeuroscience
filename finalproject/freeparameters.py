from audioop import avg
from pickletools import bytes1
from random import random
from pyparsing.util import line
from operator import add

from corefunctions import get_line, get_intersection, count, get_decision_points
from corefunctions import calc_bound, random_offer, random_fixed_offers, add_jitter, calc_decision
from corefunctions import calc_relative_value, decision_making, get_decision_points

import numpy as np
import matplotlib.pyplot as plt
import itertools
#%% 

offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)]

weight_options = [-.045, -.003, -.0015, 0, .0015, .0003, .0045, .006, .0075, .009, .0105, .012, .0135]
NDT_options = [300, 500, 700, 900, 1100, 1300]
b_options =  [.04, .06, .08, .1, .12, .14, .16, .18, .2, .22, .24, .26, .28, .3, .32]
d_options = [0, .00005, .0001, .00025, .0005, .00075, .001, .005]
offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)] 


def model_dim_experiments():

    #sort list based on collapse rates
    combos = list(itertools.product(b_options, d_options))
    combos.sort(key=lambda a: a[1]) 

    # keep track of information across trials
    percent_error = []
    money_given = []
    
    generous_errors = 0
    generous_count = 0
    selfish_errors = 0
    selfish_count = 0

    # randomly generate their values for the parameter (constants for all trials)
    NDT = np.random.choice(NDT_options)
    wself = 0.006
    wother = 0.001

    for m in range(len(d_options)):
        
        #store values for same collapse rate but different threshold heights 
        thresholds_money = []
        thresholds_error = []
        
        for n in range(len(b_options)):
            # initiaize threshold height and collapse rate
            b = combos[(m*len(b_options))+n][0]
            d = combos[(m*len(b_options))+n][1]
            
            #initialize variable to keep track of money given over all trials by choosing generously
            avg_money = 0

            for i in range(1000):
                # get the offer at this time
                offer = random_offer(offer_type)
                pself, pother = add_jitter(offer)

                # initialize variables keeping track of decision vars,
                # trials, and barriers
                d_var = 0
                trials = []
                for k in range(NDT):
                    trials.append(k)
                rdv = [0] * NDT
                uboundlist = [b] * NDT
                lboundlist = [-b] * NDT

                # calculate decision and get the time at which decision is made
                d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother)
                int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)

                # calculate relative decision value
                relative_value = calc_relative_value(pself, pother, wself, wother)

                # if the decision is generous 
                if (offer[1] > offer[0] and int2 > 0) or (offer[0] > offer[1] and int2 <= 0):
                    # add money given to other to count
                    avg_money += offer[1]
                    # increment generous count
                    generous_count += 1
                    # if the decision is a generous ERROR then add to generous error count
                    # the option with the higher relative value is not chosen
                    if (relative_value < 0 and int2 > 0):
                        generous_errors +=1
                else:
                    # if decision is selfish then increment selfish count
                    selfish_count += 1
                    # if decision is a selfish ERROR then add to selfish error count
                    if (relative_value > 0 and int2 < 0):
                        selfish_errors +=1

                # clear variables for next trial
                lboundlist.clear()
                uboundlist.clear()
                trials.clear()
                rdv.clear()

            # calculate percent error and add to list
            thresholds_error.append(((generous_errors / generous_count) - (selfish_errors / selfish_count)))
            # add average money given over generous trials to list:
            thresholds_money.append(avg_money / 1000)

        percent_error.append(thresholds_error)
        money_given.append(thresholds_money)
    
    return percent_error, money_given

percent_error, money_given = model_dim_experiments()


# plot a color map using self weights as x axis, other weights as y axis, and percent error as z axis
fig, ax = plt.subplots()
cmap = ax.pcolormesh(b_options, d_options, percent_error, shading='gouraud', cmap = 'rainbow', vmin = (np.array(percent_error)).min(), vmax = (np.array(percent_error)).max())
ax.axis([0.10,0.30, 0, 0.001])
fig.colorbar(cmap, ax=ax)
plt.ylabel('Collapse Rate')
plt.xlabel('Threshold Height')
plt.title("Average % Errors G. vs. S.")
plt.show()

fig, ax = plt.subplots()
cm = ax.pcolormesh(b_options, d_options, money_given, shading='gouraud', cmap = 'rainbow', vmin = (np.array(money_given)).min(), vmax = (np.array(money_given)).max())
ax.axis([min(b_options), max(b_options), min(d_options), max(d_options)])
fig.colorbar(cm, ax=ax)
plt.ylabel('Collapse Rate')
plt.xlabel('Threshold Height')
plt.title("Average Generosity")
plt.show()

