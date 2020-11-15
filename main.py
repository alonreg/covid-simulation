import heapq
import numpy as np


class Event():
    def __init__(self, time, eventType):
        self.time = time  # event time
        self.eventType = eventType  # type of the event
        heapq.heappush(P, self)  # add the event to the events list

    def __lt__(self, event2):
        return self.time < event2.time


def get_curr_pace(curr_time):
    time_of_day = curr_time - \
        int(curr_time / (60 * 24)) * 24 * 60  # current time of day
    if (time_of_day >= 7*60 and time_of_day < 24*60):  # if it's daytime
        return 60
    else:  # if its night time
        return 30


curr_time = 0  # total time elapsed
P = []
T = 5*60  # 10*24*60  # simulation period ####################
A = 0  # state of the server
l_r = 0  # line for regular customers
l_vip = 0  # line for VIP customers
l_tests = 10  # no. of covid tests before laborant needs tp test
event_counter = 0
customer_counter = 0


first_event_time = np.random.exponential(
    60/get_curr_pace(curr_time))  # time for the first event
Event(first_event_time, "arriving")

while P:
    event = heapq.heappop(P)
    event_counter += 1
    curr_time = event.time

    if event.eventType == "self-test-finish":  # when laborant is done with self test
        print(customer_counter, 'laborant self tested at ', curr_time)
        covid_lottery = np.random.random(1)
        new_laborant_delay = 0
        if covid_lottery > 0.998:  # covid detected in laborant's test
            # driving time for new laborant to arrive
            print(event_counter, customer_counter,
                  "laborant has covid :-(", curr_time)
            new_laborant_delay = np.random.randint(15, 30)

        # calling next customer, after done with self-test
        if l_vip > 0:  # vip in line?
            l_vip -= 1
            # if laborant is covid-free, delay is 0
            Event(curr_time + np.random.exponential(0.5) +
                  new_laborant_delay, "leaving")
        elif l_r > 0:  # regular in line?
            l_r -= 1
            Event(curr_time + np.random.exponential(0.5) +
                  new_laborant_delay, "leaving")
        else:  # no one in line
            A = 0  # server is unoccupied

    elif event.eventType == "arriving":
        if curr_time < T:  # if time is inbound
            print(customer_counter, 'Customer arrived at ', curr_time)
            if A == 0:  # if server is free
                A = 1  # then serve
                Event(curr_time + np.random.exponential(0.5),
                      "leaving")  # end of service
            # if server isnt free, depends if costumer is a child (vip) -
            else:
                # random number to choose if costumer is vip
                vip_lottery = np.random.random(1)
                if vip_lottery <= 0.7:  # check type of customer
                    l_r += 1  # add to regular queue
                else:
                    l_vip += 1  # add to vip queue

            Event(curr_time+np.random.exponential(60/get_curr_pace(curr_time)),
                  "arriving")  # create the next arrivel, always
            customer_counter += 1

    elif event.eventType == "leaving":
        l_tests -= 1
        print("customer number", customer_counter, "until tests- ",
              l_tests,  'Customer left at ', curr_time)
        if l_tests == 0:  # in case the laborant has to test for covid
            l_tests = 10  # initalize num of tests until next laborant test
            Event(curr_time + 1, "self-test-finish")
        elif l_vip > 0:
            l_vip -= 1
            Event(curr_time + np.random.exponential(0.5), "leaving")
        elif l_r > 0:
            l_r -= 1
            Event(curr_time + np.random.exponential(0.5), "leaving")
        else:
            A = 0  # no one in line
