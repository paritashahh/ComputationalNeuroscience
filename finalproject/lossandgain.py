import numpy as np
import matplotlib.pyplot as plt
from corefunctions import random_offer, calc_bound, get_decision_points

gain_domain =[(0.20, 25), (0.25, 20), (0.33, 15), (0.50, 10)]
loss_domain = [(0.20, -25), (0.25, -20), (0.33, -15), (0.50, -10)]


# use difference equation to accumulate decision variable 
def calc_decision (prev_d_var, prob, offer, base, wself, wother, s):
    # randomly generate noise from a gaussian signal
    noise = np.random.normal(0, 0.1)
    # calculate new decision variable
    d_var = prev_d_var + (wself * ((prob * offer) + base)) + (wother * (s * (prob * offer) + base)) + noise
    return d_var

#get decisions 
def decision_making (decision_time, rdv, uboundlist, lboundlist, prob, offer, base, wself, wother, s):
    # initialize decision variable to 0
    d_var = 0
    # initialize time to 0
    t = 0
    #initialize bounds
    lowerbound = -b
    upperbound = b

    # while a decision hasn't been made, continue
    while lowerbound < d_var and d_var < upperbound:
        # add the amount of time it's taken while making a decision
        decision_time.append(t + NDT)
        # update the boundary based on the current time
        upperbound = calc_bound(b, t, d)
        lowerbound = -upperbound
        uboundlist.append(upperbound)
        lboundlist.append(lowerbound)
        # calculate the decision at this time
        d_var = calc_decision (d_var, prob, offer, base, wself, wother, s)
        # add the current decision variable to the list of decision variables
        rdv.append(d_var)
        t += 1
    # return the final decision variable, the total time it took (as a list), 
    # the list of decision variables, the list of upper and lower bounds, and the offer
    return d_var, decision_time, rdv, uboundlist, lboundlist


runtimes = [0, 0]

avg_accept = []
avg_rts = []
for i in range(len(gain_domain)):
    NDT = 868
    d_var = 0
    wself  = 0.006
    wother = 0.001
    b = 0.23
    d = 0.0046
    trials = []
    for m in range(NDT):
        trials.append(m)
    rdv = [0] * NDT
    uboundlist = [b] * NDT
    lboundlist = [-b] * NDT
    lowerbound = -b
    upperbound = b
    t = NDT
    offer = gain_domain[i][1]
    prob = gain_domain[i][0]
    base = -5
    s = 5
    avg_int1 = 0.
    avg_int2 = 0.

    for j in range(1000):
        d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, prob, offer, base, wself, wother, s)
        int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
        avg_int1 += (int1/1000)
        if int2 > 0:
            avg_int2 += 1

    avg_rts.append(avg_int1/1000)
    avg_accept.append(avg_int2/1000)

for i in range(len(avg_rts)):
    runtimes[0] += avg_rts[i] 
runtimes[0] / (len(avg_rts))

offers = ['A', 'B', 'C', 'D']

fig = plt.figure()
plt.bar(offers,avg_accept, color='gray')
plt.ylabel('Acceptance Rate')
plt.xlabel('Offer Type')
plt.title("Within-Subject Acceptance Likelihood in Gain Domain") 
plt.show()

fig = plt.figure()
plt.bar(offers,avg_rts, color='gray')
plt.ylabel('Response Time')
plt.xlabel('Offer Type')
plt.title("Within-Subject Response Time in Gain Domain") 
plt.show()

avg_accept = []
avg_rts = []

for i in range(len(loss_domain)):
    NDT = 868
    d_var = 0
    wself  = 0.006
    wother = 0.001
    b = 0.23
    d = 0.0046
    trials = []
    for m in range(NDT):
        trials.append(m)
    rdv = [0] * NDT
    uboundlist = [b] * NDT
    lboundlist = [-b] * NDT
    lowerbound = -b
    upperbound = b
    t = NDT
    offer = loss_domain[i][1]
    prob =loss_domain[i][0]
    base = 5
    s = 20
    avg_int1 = 0.
    avg_int2 = 0.

    for j in range(1000):
        d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, prob, offer, base, wself, wother, s)
        int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
        avg_int1 += (int1/1000)
        if int2 > 0:
            avg_int2 += 1

    avg_rts.append(avg_int1/1000)
    avg_accept.append(avg_int2/1000)

fig = plt.figure()
plt.bar(offers,avg_accept, color='gray')
plt.ylabel('Acceptance Rate')
plt.xlabel('Offer Type')
plt.title("Within-Subject Acceptance Likelihood in Loss Domain") 
plt.show()

fig = plt.figure()
plt.bar(offers,avg_rts, color='gray')
plt.ylabel('Response Time')
plt.xlabel('Offer Type')
plt.title("Within-Subject Response Time in Loss Domain") 
plt.show()


for i in range(len(avg_rts)):
    runtimes[1] += avg_rts[i] 
runtimes[1] / (len(avg_rts))

domain = ['Gain Domain', 'Loss Domain']
plt.bar(domain,runtimes, color=['gray', 'black'])
plt.ylabel('Model RT')
plt.xlabel('Domain')
plt.title("Model Implications for RT Differences") 
plt.show()

acceptance_rates = []
socialdiscount = []
for i in range(100):
    socialdiscount.append(i)

for q in range(100):
    avg_int2 = 0.
    for i in range(len(loss_domain)):
        NDT = 868
        d_var = 0
        wself  = 0.006
        wother = 0.001
        b = 0.23
        d = 0.0046
        trials = []
        for m in range(NDT):
            trials.append(m)
        rdv = [0] * NDT
        uboundlist = [b] * NDT
        lboundlist = [-b] * NDT
        lowerbound = -b
        upperbound = b
        t = NDT
        offer = gain_domain[i][1]
        prob = gain_domain[i][0]
        base = -5
        s = q
        avg_int1 = 0.

        for j in range(1000):
            d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, prob, offer, base, wself, wother, s)
            int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
            avg_int1 += (int1/1000.)
            if int2 > 0:
                avg_int2 += 1
    acceptance_rates.append(avg_int2 / (1000. * len(gain_domain)))


fig = plt.figure()
plt.plot(socialdiscount,acceptance_rates)
plt.ylabel('Average Acceptance Rate')
plt.xlabel('Social Discounting Factor')
plt.title("Average Acceptance Likelihood in Gain Domain as a Function of Social Distance") 
plt.show()


acceptance_rates = []
socialdiscount = []
for i in range(100):
    socialdiscount.append(i)

for q in range(100):
    avg_int2 = 0.
    for i in range(len(loss_domain)):
        NDT = 868
        d_var = 0
        wself  = 0.006
        wother = 0.001
        b = 0.23
        d = 0.0046
        trials = []
        for m in range(NDT):
            trials.append(m)
        rdv = [0] * NDT
        uboundlist = [b] * NDT
        lboundlist = [-b] * NDT
        lowerbound = -b
        upperbound = b
        t = NDT
        offer = loss_domain[i][1]
        prob = loss_domain[i][0]
        base = 5
        s = q
        avg_int1 = 0.

        for j in range(1000):
            d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, prob, offer, base, wself, wother, s)
            int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
            avg_int1 += (int1/1000.)
            if int2 > 0:
                avg_int2 += 1
    acceptance_rates.append(avg_int2 / (1000. * len(loss_domain)))


fig = plt.figure()
plt.plot(socialdiscount,acceptance_rates)
plt.ylabel('Average Acceptance Rate')
plt.xlabel('Social Discounting Factor')
plt.title("Average Acceptance Likelihood in Loss Domain as a Function of Social Distance") 
plt.show()


