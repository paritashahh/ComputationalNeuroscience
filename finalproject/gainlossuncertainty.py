import numpy as np
import matplotlib.pyplot as plt
from corefunctions import random_offer, calc_bound, get_decision_points

gain_domain =[(0.20, 25), (0.25, 20), (0.33, 15), (0.50, 10)]
loss_domain = [(0.20, -25), (0.25, -20), (0.33, -15), (0.50, -10)]


# use difference equation to accumulate decision variable 
def calc_decision (prev_d_var, p1, pself, p2, pother, wself, wother, base, s):
    # randomly generate noise from a gaussian signal
    noise = np.random.normal(0, 0.1)
    # calculate new decision variable
    d_var = prev_d_var + (wself * ((p1 * pself) + base)) + (wother * (s * (p2 * pother) + base)) + noise
    return d_var

#get decisions 
def decision_making (decision_time, rdv, uboundlist, lboundlist, p1, pself, p2, pother, wself, wother, base, s):
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
        d_var = calc_decision (d_var, p1, pself, p2, pother, wself, wother, base, s)
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
    p1 = gain_domain[i][0]
    p2 = gain_domain[i][0]
    pself = gain_domain[i][1]
    pother = gain_domain[i][1]
    base = -5
    s = 1
    avg_int1 = 0.
    avg_int2 = 0.

    for j in range(1000):
        d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, p1, pself, p2, pother, wself, wother, base, s)
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

print("Average Acceptance Rate in Gain:")
print(avg_accept)
fig = plt.figure()
plt.bar(offers,avg_accept, color='gray')
plt.ylabel('Acceptance Rate')
plt.xlabel('Offer Type')
plt.title("Within-Subject Acceptance Likelihood in Gain Domain") 
plt.savefig('gainacceptance.png', bbox_inches='tight')
plt.show()

print("Average RT in Gain:")
print(avg_rts)
fig = plt.figure()
plt.bar(offers,avg_rts, color='gray')
plt.ylabel('Response Time')
plt.xlabel('Offer Type')
plt.title("Within-Subject Response Time in Gain Domain") 
plt.savefig('gainrt.png', bbox_inches='tight')
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
    p1 = loss_domain[i][0]
    p2 = loss_domain[i][0]
    pself = loss_domain[i][1]
    pother = loss_domain[i][1]
    base = -5
    s = 1
    avg_int1 = 0.
    avg_int2 = 0.

    for j in range(1000):
        d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, p1, pself, p2, pother, wself, wother, base, s)
        int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
        avg_int1 += (int1/1000)
        if int2 > 0:
            avg_int2 += 1

    avg_rts.append(avg_int1/1000)
    avg_accept.append(avg_int2/1000)

print("Average Acceptance Rate in Loss:")
print(avg_accept)
fig = plt.figure()
plt.bar(offers,avg_accept, color='gray')
plt.ylabel('Acceptance Rate')
plt.xlabel('Offer Type')
plt.title("Within-Subject Acceptance Likelihood in Loss Domain")
plt.savefig('lossacceptance.png', bbox_inches='tight') 
plt.show()

print("Average RT in Loss:")
print(avg_rts)
fig = plt.figure()
plt.bar(offers,avg_rts, color='gray')
plt.ylabel('Response Time')
plt.xlabel('Offer Type')
plt.title("Within-Subject Response Time in Loss Domain") 
plt.savefig('lossrt.png', bbox_inches='tight') 
plt.show()


for i in range(len(avg_rts)):
    runtimes[1] += avg_rts[i] 
runtimes[1] / (len(avg_rts))

print("RT in Gain vs. Loss Domains")
print(runtimes)
domain = ['Gain Domain', 'Loss Domain']
plt.bar(domain,runtimes, color=['gray', 'black'])
plt.ylabel('Model RT')
plt.xlabel('Domain')
plt.title("Model Implications for RT Differences") 
plt.savefig('gainlossrts.png', bbox_inches='tight') 
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
        p1 = gain_domain[i][0]
        p2 = gain_domain[i][0]
        pself = gain_domain[i][1]
        pother = gain_domain[i][1]
        base = -5
        s = q
        avg_int1 = 0.

        for j in range(1000):
            d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, p1, pself, p2, pother, wself, wother, base, s)
            int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
            avg_int1 += (int1/1000.)
            if int2 > 0:
                avg_int2 += 1
    acceptance_rates.append(avg_int2 / (1000. * len(gain_domain)))


print("Acceptance Rate vs. Social Discount Gains")
print(acceptance_rates)
fig = plt.figure()
plt.plot(socialdiscount,acceptance_rates)
plt.ylabel('Average Acceptance Rate')
plt.xlabel('Social Distance Factor')
plt.title("Acceptance Likelihood in Gain Domain") 
plt.savefig('gainacceptancesocialdiscount.png', bbox_inches='tight') 
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
        p1 = loss_domain[i][0]
        p2 = loss_domain[i][0]
        pself = loss_domain[i][1]
        pother = loss_domain[i][1]
        base = 5
        s = q
        avg_int1 = 0.

        for j in range(1000):
            d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, p1, pself, p2, pother, wself, wother, base, s)
            int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
            avg_int1 += (int1/1000.)
            if int2 > 0:
                avg_int2 += 1
    acceptance_rates.append(avg_int2 / (1000. * len(loss_domain)))

print("Acceptance Rate vs. Social Discount Loss")
print(acceptance_rates)
fig = plt.figure()
plt.plot(socialdiscount,acceptance_rates)
plt.ylabel('Average Acceptance Rate')
plt.xlabel('Social Distance Factor')
plt.title("Acceptance Likelihood in Loss Domain") 
plt.savefig('lossacceptancesocialdiscount.png', bbox_inches='tight') 
plt.show()




