from pickletools import bytes1
from pyparsing.util import line
from corefunctions import get_line, get_intersection, count, divide_list
from corefunctions import get_decision_points, random_offer, calc_bound, decision_making
#%% 
import numpy as np
import matplotlib.pyplot as plt

offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)]

generousness = [0, 0]

avg_rts = []
avg_accept = []
gs_rts = []

avg_grt = 0.
avg_srt = 0.

for i in range(len(offer_type)):
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
    pself, pother = offer_type[i]
    avg_int1 = 0.
    avg_int2 = 0.

    for j in range(1000):
        d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother)
        int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
        avg_int1 += (int1/1000)
        if int2 > 0:
            avg_int2 += 1
        if pother > pself and int2 > 0 or pself > pother and int2 <= 0:
            avg_grt += int1
            generousness[0] += 1
        else:
            avg_srt += int1

    avg_rts.append(avg_int1/1000)
    avg_accept.append(avg_int2/1000)
generousness[0] = (generousness[0] / (1000 * 3))
gs_rts.append(avg_grt/(1000 * 1000 * 3))
gs_rts.append(avg_srt/(1000 * 1000 * 6))

offers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

behavior = ['Self Choice', 'Generous Choice']
plt.bar(behavior,gs_rts, color=['gray', 'black'])
plt.ylabel('Model RT')
plt.xlabel('Behavior')
plt.title("Model Implications for RT Differences (Gain Domain)") 
plt.show()


offer_type = [(-25, -75), (-25, -100), (-50, -10), (-50, -100), (-75, -10), (-75, -25), (-100, -10), (-100, -25), (-100, -50)]
pself, pother = random_offer(offer_type)


# use difference equation to accumulate decision variable 
def calc_decision (prev_d_var, pself, pother, wself, wother):
    # randomly generate noise from a gaussian signal
    noise = np.random.normal(0, 0.1)
    # calculate new decision variable
    d_var = prev_d_var + (wself * (pself + 50)) + (wother * (pother + 50)) + noise
    return d_var

#get decisions 
def ldecision_making (decision_time, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother):
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
        d_var = calc_decision (d_var, pself, pother, wself, wother)
        # add the current decision variable to the list of decision variables
        rdv.append(d_var)
        t += 1
    # return the final decision variable, the total time it took (as a list), 
    # the list of decision variables, the list of upper and lower bounds, and the offer
    return d_var, decision_time, rdv, uboundlist, lboundlist


avg_rts = []
avg_accept = []
gs_rts = []

avg_grt = 0.
avg_srt = 0.

for i in range(len(offer_type)):
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
    pself, pother = offer_type[i]
    avg_int1 = 0.
    avg_int2 = 0.

    for j in range(1000):
        d_var, trials, rdv, uboundlist, lboundlist = ldecision_making(trials, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother)
        int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)
        avg_int1 += (int1/1000)
        if int2 > 0:
            avg_int2 += 1
        if pother > pself and int2 > 0 or pself > pother and int2 <= 0:
            avg_grt += int1
            generousness[1] += 1
        else:
            avg_srt += int1

    avg_rts.append(avg_int1/1000.)
    avg_accept.append(avg_int2/1000.)
generousness[1] = (generousness[1] / (1000. * 6.))
gs_rts.append(avg_grt/(1000. * 1000. * 6.))
gs_rts.append(avg_srt/(1000. * 1000. * 3.))

behavior = ['Self Choice', 'Generous Choice']
plt.bar(behavior,gs_rts, color=['gray', 'black'])
plt.ylabel('Model RT')
plt.xlabel('Behavior')
plt.title("Model Implications for RT Differences (Loss Domain)") 
plt.show()


domain = ['Gain Domain', 'Loss Domain']
plt.bar(domain,generousness, color=['gray', 'black'])
plt.ylabel('Average Generosity')
plt.xlabel('Domain')
plt.title("Model Implications for Domain Speciic Generosity") 
plt.show()


