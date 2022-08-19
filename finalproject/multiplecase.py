from pickletools import bytes1
from random import random
from pyparsing.util import line
#%% 
import numpy as np
import matplotlib.pyplot as plt
from corefunctions import get_line, get_intersection, count, get_decision_points

weight_options = [-.045, -.003, -.0015, 0, .0015, .0003, .0045, .006, .0075, .009, .0105, .012, .0135]
NDT_options = [300, 500, 700, 900, 1100, 1300]
barrier_options =  [.04, .06, .08, .1, .12, .14, .16, .18, .2, .22, .24, .26, .28, .3, .32]
b_options = [0, .00005, .0001, .00025, .0005, .00075, .001, .005]
offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)]

#free parameters aka parameters that will change based on experiments
#np.random.choice(NDT_options)
NDT = 868
wself = 0.006
wother = 0.001
b = 0.23
d = 0.00046


# calculate the upper barrier
def calc_bound (b, t):
    return b * np.exp(-t*d)
    
# pick a random offer from the list of offers
def random_offer ():
    random_val = np.random.randint(0, 9)
    pself = offer_type[random_val][0]
    pother  = offer_type[random_val][1]
    return pself, pother

# use difference equation to accumulate decision variable 
def calc_decision (prev_d_var, pself, pother, k):
    noise = np.random.normal(0, 0.1)
    # randomly pick a number between 1 AND 4
    self_jitter = np.random.randint(1, 5)
    # randomly choose either negative or positive
    self_jitter_sign = np.random.choice([-1, 1])
    self_jitter *= self_jitter_sign
    other_jitter = np.random.randint(1, 5)
    # randomly choose either negative or positive
    other_jitter_sign = np.random.choice([-1, 1])
    other_jitter *= other_jitter_sign
    d_var = prev_d_var + (wself * ((pself) - 50)) + (k * wother * ((pother) - 50)) + noise
    return d_var

def decision_making (decision_time, rdv, uboundlist, lboundlist, k):
    # initialize decision variable to 0
    d_var = 0
    # initialize time to 0
    t = 0
    #initialize bounds
    lowerbound = -b
    upperbound = b
    # select random offer from list of options
    pself, pother = random_offer()
    # while a decision hasn't been made, continue
    while lowerbound < d_var and d_var < upperbound:
        t += 1
        decision_time.append(t + NDT)
        upperbound = calc_bound(b, t)
        lowerbound = -upperbound
        uboundlist.append(upperbound)
        lboundlist.append(lowerbound)
        d_var = calc_decision (d_var, pself, pother, k)
        rdv.append(d_var)
    return d_var, decision_time, rdv, uboundlist, lboundlist, (pself, pother)


def experiments(k):
    offers_chosen = []
    offer_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    rts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    decisions = []
    # list to keep track of average selfishness [0] vs. generosity [1] 
    generosity = [0, 0]
    generousness = 0
    selfishness = 0
    for i in range(1000):
        # initialize variables keeping track of decision vars,
        # trials, and barriers
        trials = []
        for i in range(NDT):
            trials.append(i)
        rdv = [0] * NDT
        uboundlist = [b] * NDT
        lboundlist = [-b] * NDT

        # calculate decision and get the time at which decision is made
        d_var, trials, rdv, uboundlist, lboundlist, offer = decision_making(trials, rdv, uboundlist, lboundlist, k)
        int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)

        # add to count of offer
        offer_count[offer_type.index(offer)] += 1
        
        # keep track of response times and decisions made
        #rts.append(int1)
        decisions.append(int2)

        rts[offer_type.index(offer)] += int1

        # decide whether decision is generous or selfish
        if offer[0] < 50 and int2 > 0 or offer[0] > 50 and int2 < 0:
            generousness += 1
            generosity[1] += int1
        else:
            selfishness += 1
            generosity[0] += int1

        # if offer is accepted, add to list of offers chosen
        if (int2 > 0):
            offers_chosen.append(offer)
        
        # clear variables for next trial
        lboundlist.clear()
        uboundlist.clear()
        trials.clear()
        rdv.clear()

    # for all elements in rts, divide by 1000 to get average
    for i in range(len(rts)):
        rts[i] = rts[i] / (1000*1000)
    
    # for all elements in generosity, divide by 1000 to get average
    generosity[0] = (generosity[0] / selfishness) / 1000
    if generousness > 0:
        generosity[1] = (generosity[1] / generousness) / 1000
    else:
        generosity[1] = 0

    return rts, decisions, offers_chosen, generosity, offer_count

# convert a list of chosen offers to get frequency of each offer type (in order from A-I)
def chosen_to_frequency (offers_chosen, offer_count):
    freq = []
    for i in range(len(offer_type)):
        freq.append((count(offers_chosen, offer_type[i]))/offer_count[i])
    return freq

# convert a list of rts correspomding to each offer type to get average rt for each offer type
def rts_to_average (rts):
    avg = []
    for i in range(len(offer_type)):
        avg.append(np.mean(rts[i]))
    return avg

rts, decisions, offers_chosen, generosity, offer_count = experiments(1)
freq = chosen_to_frequency(offers_chosen, offer_count)

offers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.6, 0.6])
ax.bar(offers,freq)
plt.ylabel('Acceptance Rate')
plt.xlabel('Offer Type')
plt.title("Within-Subject Acceptance Likelihood") 
plt.show()

fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.4, 0.4])
ax.bar(offers,rts_to_average(rts))
plt.ylabel('Response Time')
plt.xlabel('Offer Type')
plt.title("Within-Subject Response Time") 
plt.show()

behavior = ['Self Choice', 'Generous Choice']
plt.bar(behavior,generosity)
plt.ylabel('Model RT')
plt.xlabel('Behavior')
plt.title("Model Implications for RT Differences") 
plt.show()


offer_frequency = []
for i in range(9):
    offer_frequency.append(count(offers_chosen, i)/len(offers_chosen))



pre_d_var = 0
offers_chosen = []
rts = []
decisions = []

for i in range(100):
    print("this is at the beginning of the loop")
    print(pre_d_var)
    #singular case 
    NDT = 3
    d_var = 0
    wself  = 0.006
    wother = 0.001
    b = 0.23
    d = 0.00046
    trial = []
    for i in range(NDT):
        trial.append(i)
    rdv = [0] * NDT
    uboundlist = [b] * NDT
    lboundlist = [-b] * NDT
    lowerbound = -b
    upperbound = b
    t = NDT

    offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)]
    random_val = np.random.randint(0, 9)
    pself = offer_type[random_val][0]
    pother  = offer_type[random_val][1]

    while lowerbound < d_var and d_var < upperbound:
        trial.append(t)
        upperbound = b * np.exp(-t*d)
        lowerbound = -upperbound
        uboundlist.append(upperbound)
        lboundlist.append(lowerbound)
        noise = float(np.random.randn())
        d_var = pre_d_var + wself * (pself-50) + wother * (pother -50) + noise
        rdv.append(d_var)
        t += 1

    print("this is in the middle of the loop")
    pre_d_var = d_var
    print(pre_d_var)


    if d_var > 0:
        # dtrial = rdv.index(max(rdv))
        dtrial = len(rdv) - 1
        dx1 = dtrial
        dx2 = dtrial-1
        dy1 = d_var
        dy2 = rdv[dtrial-1]
        bx1 = dtrial
        bx2 = dtrial-1
        by1 = uboundlist[dtrial]
        by2 = uboundlist[dtrial-1]
    else:
        # dtrial = rdv.index(min(rdv))
        dtrial = len(rdv) - 1
        dx1 = dtrial
        dx2 = dtrial-1
        dy1 = d_var
        dy2 = rdv[dtrial-1]
        bx1 = dtrial
        bx2 = dtrial-1
        by1 = lboundlist[dtrial]
        by2 = lboundlist[dtrial-1]

    #get equation of a line from 2 points
    def get_line(x1, y1, x2, y2):
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return m, b

    #plot a line
    def plot_line(m, b):
        x = np.linspace(0, dtrial+5, 2)
        y = m * x + b
        plt.plot(x, y, 'r')

    dm, db = get_line(dx1, dy1, dx2, dy2)
    bm, bb = get_line(bx1, by1, bx2, by2)

    #get intersection point of two lines
    def get_intersection(m1, b1, m2, b2):
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        return x, y

    int1, int2 = get_intersection(dm, db, bm, bb)

    if (d_var > 0):
        offers_chosen.append(random_val)
    rts.append(int1)
    decisions.append(int2)
    lboundlist.clear()
    uboundlist.clear()
    trial.clear()
    rdv.clear()

# count occurances of an element in a list
def count(lst, element):
    return lst.count(element)

print(offers_chosen)

offer_frequency = []
for i in range(9):
    offer_frequency.append(count(offers_chosen, i)/len(offers_chosen))

print(offer_frequency)

offers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(offers,offer_frequency)
plt.show()
#print(offers_chosen)

#print(rts)

#print(decisions)



print(int1, int2)
print(dtrial, d_var)

plt.plot(trial, rdv)
plt.plot(trial, uboundlist, color = "#00008B")
plt.plot(trial, lboundlist, color = "#00008B")

plt.plot([0]*len(trial), "-", color = "grey")
plt.ylabel('RDV')
plt.xlabel('Time')
plt.title("DDM of Altruistic Behavior") 
plt.text(len(trial)-1,min(uboundlist)+1,'Accept')
plt.text(0,-1,'RDV = RDV + w($Self - $50) + w($Other-$50) + e')
plt.text(len(trial)-1,max(lboundlist)-1,'Reject')

# intersection of boundary and rdv
plt.vlines(x=int1, ymin=-int2, ymax=int2, colors='red', ls='--', lw=2, label='vline_single - partial height')
plt.text(len(trial)-1,int2, 'Choice', color='red')
plt.text(len(trial)-1,0, 'RT', color='red')
plt.scatter(int1, int2, color='red')
plt.show()

# %%
