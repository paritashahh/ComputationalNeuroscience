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


weight_options = [-.045, -.003, -.0015, 0, .0015, .0003, .0045, .006, .0075, .009, .0105, .012, .0135]
NDT_options = [300, 500, 700, 900, 1100, 1300]
b_options =  [.04, .06, .08, .1, .12, .14, .16, .18, .2, .22, .24, .26, .28, .3, .32]
d_options = [0, .00005, .0001, .00025, .0005, .00075, .001, .005]
offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)] 

#free parameters aka parameters that will change based on experiments
#np.random.choice(NDT_options)
NDT = 868
wself = 0.006
wother = 0.001
b = 0.23
d = 0.00046

combinations = list(itertools.product(weight_options, weight_options))
combinations.sort(key=lambda a: a[1]) 
print(combinations)

def model_err_experiments():

    # randomly generate their values for the parameter (constants for all trials)
    NDT = np.random.choice(NDT_options)
    b = np.random.choice(b_options)
    d = np.random.choice(d_options)

    # keep track of information across trials
    percent_error = []
    money_given = []

    for q in range (len(weight_options)):
        
        error_rows = []
        money_rows = []
        
        for p in range(len(weight_options)):

            wself = combinations[(q*len(weight_options))+p][0]
            wother = combinations[(q*len(weight_options))+p][1]

            avg_money = 0

            generous_errors = 0
            generous_count = 0
            selfish_errors = 0
            selfish_count = 0
        
            for i in range(len(offer_type)):

                # get the offer at this time
                offer = offer_type[i]
                pself, pother = add_jitter(offer)

                # initialize variables keeping track of decision vars,
                # trials, and barriers
                trials = []
                for i in range(NDT):
                    trials.append(i)
                rdv = [0] * NDT
                uboundlist = [b] * NDT
                lboundlist = [-b] * NDT

                # calculate decision and get the time at which decision is made
                d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother)
                int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)

                # calculate relative decision value
                relative_value = calc_relative_value(pself, pother, wself, wother)

                # keep track of whether the decision was an error
                if relative_value < 0 and int2 > 0 or relative_value > 0 and int2 < 0:
                    if pother > pself and int2 > 0 or pself > pother and int2 <= 0:
                        generous_errors += 1
                    else:
                        selfish_errors += 1
                    
                # decide whether decision is generous or selfish
                if pother > pself and int2 > 0 or pself > pother and int2 <= 0:
                    # add money given to other for generous choices
                    avg_money += 50 - offer[1]
                    generous_count += 1

                else:
                    selfish_count += 1
                
                # clear variables for next trial
                lboundlist.clear()
                uboundlist.clear()
                trials.clear()
                rdv.clear()

            # calculate percent error and add to list
            if generous_errors > 0 and selfish_errors > 0:
                print(generous_errors/generous_count - selfish_errors / (selfish_count))
                error_rows.append(generous_errors/generous_count - selfish_errors / (selfish_count))
            else:
                error_rows.append(0)
            
            # add average money given over generous trials to list:
            if generous_count > 0:
                money_rows.append(avg_money / generous_count)
            else:
                money_rows.append(0)
        
        percent_error.append(error_rows)
        money_given.append(money_rows)
    
    return percent_error, money_given


percent_error, money_given = model_err_experiments()

def many_trials():
    percent_error, money_given = model_err_experiments()
    for i in range(100):
        percent_error1, money_given1 = model_err_experiments()
        percent_error = np.array(percent_error) + np.array(percent_error1)
        money_given = np.array(money_given) + np.array(money_given1)
    percent_error = percent_error/ 100
    money_given = money_given / 100
    return percent_error, money_given 

#percent_error, money_given = many_trials()

# Generate data for the plot
x = np.linspace(-0.002, 0.012, 13)
y = np.linspace(-0.005, 0.012, 13)

# plot a color map using self weights as x axis, other weights as y axis, and percent error as z axis
fig, ax = plt.subplots()
cmap = ax.pcolormesh(weight_options, weight_options, percent_error, shading='gouraud', cmap = 'rainbow', vmin = min(min(percent_error)), vmax = max(max(percent_error)))
ax.axis([x.min(), x.max(), y.min(), y.max()])
fig.colorbar(cmap, ax=ax)
plt.ylabel('Other Weight')
plt.xlabel('Self Weight')
plt.title("Average % Errors G. vs. S.") 
plt.show()

#correct graph for money given
fig, ax = plt.subplots()
cm = ax.pcolormesh(weight_options, weight_options, money_given, shading='gouraud', cmap = 'rainbow', vmin = min(min(money_given)), vmax = max(max(money_given)))
ax.axis([x.min(), x.max(), y.min(), y.max()])
fig.colorbar(cm, ax=ax)
plt.ylabel('Other Weight')
plt.xlabel('Self Weight')
plt.title("Average Generosity") 
plt.show()


fig, ax = plt.subplots()
cm = ax.pcolormesh([1,2], [5,6,7], [[1,2], [9,0], [12, 13]], cmap = 'rainbow', vmin = 0, vmax = 13)
fig.colorbar(cm)
plt.ylabel('Collapse Rate')
plt.xlabel('Threshold Height')
plt.title("Average Generosity")
plt.show()

#first element x each of the second elements will be the the first element of each of the lists

#b_options, d_options, 

#a list of lists, where first element of every list is the amount of money given for threshold height#1 x all of the collapse rates 

# each list within the lists should be for all x values and the same collapse rate [[for collapse rate+1, all threshold heights], [for collapse rate #2, all threshold heights] ]
# so iterate through and make lists of lists for each collapse rate

#should have a total of 8 lists, each with 15 elements 
