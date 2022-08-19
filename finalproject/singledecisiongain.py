from pickletools import bytes1
from pyparsing.util import line
from corefunctions import get_line, get_intersection, count, divide_list
from corefunctions import decision_making, get_decision_points, random_offer, add_jitter
#%% 
import numpy as np
import matplotlib.pyplot as plt

offer_type = [(25, 75), (25, 100), (50, 10), (50, 100), (75, 10), (75, 25), (100, 10), (100, 25), (100, 50)]

avg_rts = []
avg_accept = []
gs_rts = []

avg_grt = 0.
avg_srt = 0.

for i in range(len(offer_type)):
    NDT = 868
    d_var = 0
    wself  = 0.004
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
        else:
            avg_srt += int1

    avg_rts.append(avg_int1/1000)
    avg_accept.append(avg_int2/1000)
gs_rts.append(avg_grt/(1000 * 1000 * 3))
gs_rts.append(avg_srt/(1000 * 1000 * 6))

offers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

fig = plt.figure()
plt.bar(offers,avg_accept, color='gray')
plt.ylabel('Acceptance Rate')
plt.xlabel('Offer Type')
plt.title("Within-Subject Acceptance Likelihood") 
plt.savefig('paperaccept.png', bbox_inches='tight') 
plt.show()

fig = plt.figure()
plt.bar(offers,avg_rts, color='gray')
plt.ylabel('Response Time')
plt.xlabel('Offer Type')
plt.title("Within-Subject Response Time") 
plt.savefig('paperrt.png', bbox_inches='tight') 
plt.show()

behavior = ['Self Choice', 'Generous Choice']
plt.bar(behavior,gs_rts, color=['gray', 'black'])
plt.ylabel('Model RT')
plt.xlabel('Behavior')
plt.title("Model Implications for RT Differences") 
plt.savefig('rtdiff.png', bbox_inches='tight') 
plt.show()


# one decision

#singular case 
NDT = 3
d_var = 0
wself  = 0.006
wother = 0.001
b = 7
d = 0.046
trials = []
for i in range(NDT):
  trials.append(i)
rdv = [0] * NDT
uboundlist = [b] * NDT
lboundlist = [-b] * NDT
lowerbound = -b
upperbound = b
t = NDT

offer = random_offer(offer_type)
pself, pother = add_jitter(offer)
d_var, trials, rdv, uboundlist, lboundlist = decision_making(trials, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother)
int1, int2 = get_decision_points(d_var, rdv, uboundlist, lboundlist)

ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)

plt.plot(trials, rdv)
plt.plot(trials, uboundlist, color = "#00008B")
plt.plot(trials, lboundlist, color = "#00008B")

plt.plot([0]*len(trials), "-", color = "grey")
plt.ylabel('RDV')
plt.xlabel('Time')
plt.title("DDM of Altruistic Behavior") 
plt.text(len(trials)-1,min(uboundlist)+1,'Accept')
plt.text(0,-1,'RDV = RDV + w(p1 * $Self - $50) + w(s(p2 * $Other) - $50) + e')
plt.text(len(trials)-1,max(lboundlist)-1,'Reject')

# intersection of boundary and rdv
plt.vlines(x=int1, ymin=-int2, ymax=int2, colors='red', ls='--', lw=2, label='vline_single - partial height')
plt.text(len(trials)-1,int2, 'Choice', color='red')
plt.text(len(trials)-1,0, 'RT', color='red')
plt.scatter(int1, int2, color='red')
plt.savefig('paperddm.png', bbox_inches='tight') 
plt.show()