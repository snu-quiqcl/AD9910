# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 15:34:13 2018

@author: iontrap
"""

data = data_exported

pulse_trigger_not_arrive_count = 0

arrival_time = []
PMT_arrival_time = []
pulse_arrival_time = []
filtered_case = []

for each in data:
    if each[3] == 100:
        arrival_time += each[0:3]
    elif each[3] == 200:
        PMT_arrival_time += each[0:3]
    elif each[3] == 300:
        pulse_arrival_time += each[0:3]
    elif each[3] == 10:
        pulse_trigger_not_arrive_count += 1
    elif each[3] == 45:
        filtered_case.append(each[0:3])
    else:
        print('Unknown signature:', each)


x = np.arange(len(arrival_time))
fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x, arrival_time)
axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output ')
axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (clocks)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x, PMT_arrival_time)
axs.set_title('Photon arrival time distribution w.r.t. stopwatch start')
axs.set_xlabel('Photon arrival time distribution w.r.t. stopwatch start (clocks)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x, pulse_arrival_time)
axs.set_title('Pulse picker trigger output time distribution w.r.t. stopwatch start')
axs.set_xlabel('Pulse picker trigger output time distribution w.r.t. stopwatch start (clocks)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

"""
a=np.array(filtered_case)
b=a.transpose()[2]



c={}
for each_data in filtered_case:
    if each_data[2] in c.keys():
        c[each_data[2]] += 1
    else:
        c[each_data[2]] = 1
plt.figure()
plt.bar(list(c.keys()), list(c.values()))


a={}
for each_data in PMT1_filtered_case:
    if each_data[1] in a.keys():
        a[each_data[1]] += 1
    else:
        a[each_data[1]] = 1
plt.figure()
plt.bar(list(a.keys()), list(a.values()))




plt.figure()
plt.plot(PMT_arrival_time)
plt.yscale('log')
plt.draw()

"""