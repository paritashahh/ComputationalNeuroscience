import numpy as np
import matplotlib.pyplot as plt

########################## list-related functions ##########################
#get equation of a line from 2 points
def get_line(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b

#get intersection point of two lines
def get_intersection(m1, b1, m2, b2):
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return x, y

# count occurances of an element in a list
def count(lst, element):
    return lst.count(element)

#divide all elemtns of list by a single number
def divide_list(list, num):
    new_list = []
    for i in list:
        new_list.append(i/num)
    return new_list

###############################################################################

########################## random-offer functions ##########################

# pick a random offer from the list of offers
def random_offer (offer_type):
    random_val = np.random.randint(0, len(offer_type))
    pself = offer_type[random_val][0]
    pother  = offer_type[random_val][1]
    return pself, pother

# add jitter to the offer value to avoid habituation
def add_jitter (offer):

    # add jitter to offer choices to avoid habituation
    self_jitter = np.random.randint(1, 5)
    other_jitter = np.random.randint(1, 5)

    if (offer[0] == 100):
        self_jitter = self_jitter * -1
    else:
        self_jitter *= np.random.choice([-1, 1])

    if (offer[1] == 100):
        other_jitter = other_jitter * -1
    else:
        other_jitter *= np.random.choice([-1, 1])

    return offer[0] + self_jitter, offer[1] + other_jitter  

# pick a random offer from the list of offers and add jittered value
def random_offer_with_jitter (offer_type):
    random_val = np.random.randint(0, len(offer_type))
    pself = offer_type[random_val][0]
    pother  = offer_type[random_val][1]
    
    # add jitter to offer choices to avoid habituation
    self_jitter = np.random.randint(1, 5)
    other_jitter = np.random.randint(1, 5)

    if (pself == 100):
        self_jitter = self_jitter * -1
    else:
        self_jitter *= np.random.choice([-1, 1])

    if (pother == 100):
        other_jitter = other_jitter * -1
    else:
        other_jitter *= np.random.choice([-1, 1])

    return pself + self_jitter, pother + other_jitter    

# randomly shuffle offers so that each offer will be presented 20 times in different orders
def random_fixed_offers(offer_type):
    offers = offer_type
    order = []
    for i in range(20):
        np.random.shuffle(offers)
        # add all the offers to the order list
        for j in range(len(offers)):
            order.append(offers[j])
    return order


########################## core-calculation functions ##########################

# calculate the upper barrier
def calc_bound (b, t, d):
    return b * np.exp(-t*d)

# use difference equation to accumulate decision variable 
def calc_decision (prev_d_var, pself, pother, wself, wother):
    # randomly generate noise from a gaussian signal
    noise = np.random.normal(0, 0.1)
    # calculate new decision variable
    d_var = prev_d_var + (wself * (pself - 50)) + (wother * (pother - 50)) + noise
    return d_var

# use difference equation to accumulate decision variable 
def calc_decision_with_familiarity (prev_d_var, pself, pother, wself, wother, k):
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

# calculate the relative value of the offer
def calc_relative_value (pself, pother, wself, wother):
    rv = (wself * (pself - 50)) + (wother * (pother - 50))
    return rv

#get decisions 
def decision_making (decision_time, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother):
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

#get decisions 
def decision_making_with_familiarity (decision_time, rdv, uboundlist, lboundlist, b, d, NDT, pself, pother, wself, wother, k):
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

# get the decision time and the rdv values (int1, int2)
def get_decision_points (d_var, rdv, uboundlist, lboundlist):
    # time at which the decision happens
    dx1 = len(rdv) - 1
    # decision variable at the time of decision
    dx2 = dx1 - 1
    dy1 = d_var
    dy2 = rdv[dx2]
    # boundary at the time of decision
    if d_var > 0:
        by1 = uboundlist[dx1]
        by2 = uboundlist[dx2]
    else:
        by1 = lboundlist[dx1]
        by2 = lboundlist[dx2]

    # get slope of decision line
    dm, db = get_line(dx1, dy1, dx2, dy2)
    # get slope of boundary line
    bm, bb = get_line(dx1, by1, dx2, by2)

    # get intersection point of decision and boundary lines
    int1, int2 = get_intersection(dm, db, bm, bb)
    return int1, int2

########################## social-discounting factor ##########################

#function to calculate social discount rate
# v is the discounted value of the reward
def calc_social_discount_rate(bigV, s, N):
    # calculate the social discount rate
    return(bigV / (1 + s * N))

#losses have a lmabda which means it's weighed more
#if lamba > 1 and less if lamba < 1
