# regular node: Node which for a given transmission cycle, just senses the data
#forwarder: node that is either cluster head or forwarder for a given cluster
import math as ma
from csv import writer
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
#Universal variables:
daily_usage_water_per_plant=3.5 #in mm
dummy = pow(10, -9)
ETX = 16.7 * dummy  # this is the energy dissipated on transmission of bit package
ERX = 36.1 * dummy  # this is the energy consumed at the time of recieving of the bit package
EDA = 5.0 * dummy
Emp = 1.97 * dummy  # this is the energy cnsumed at the time of bit amplification
lamb = 0.125
c = 299792458
d0 = 0.1
alive_node_list=[]
global_total=0 # global total of the water so far
global_residue=0

#creating classes for normal and base station nodes
class node:
    def __init__(self,normal_id,idee,x,y):
        self.energy=0.5
        self.humidity=70 #in mm
        self.id=idee
        self.id_normal=normal_id
        self.x_coor=x
        self.y_coor=y
        self.alive=1 #1-yes; 0-no

    def whats_my_energy(self):
        return self.energy

    def whats_my_humidity(self):
        return self.humidity

    def update_humidity(self):
        if self.id==1:
            self.humidity = self.humidity - (3.0 / 24)
        elif self.id==2:
            self.humidity = self.humidity - (3.5 / 24)
        elif self.id==3:
            self.humidity = self.humidity - (4.0 / 24)

    def replenish(self):
        self.humidity=self.humidity+35
        global_total=+35

    def x_coordinate(self):
        return self.x_coor

    def y_coordinate(self):
        return self.y_coor

    def status(self):
        return self.alive

    def ide(self):
        return self.id

    def updating_in_case_normal(self):
        d = euclidean_distance(self, bs)
        self.energy = self.energy - ((ETX) * (4000) + Emp * 3.38 * 4000 * (ma.pow(d, 3.38)))

    def updating_in_case_forwarder(self):
        d = euclidean_distance(self, bs)
        self.energy = self.energy - ((ETX + ERX + EDA) * (4000) + Emp * 3.38 * 4000 * (ma.pow(d, 3.38)))

class base_Station:  #we only need base station to get distance for energy equation calculations
    def __init__(self):
        self.x_coor=62.5
        self.y_coor=50
bs=base_Station(); # universal base station node
#initializing the nodes:

#To refresh all nodes at every new cycle
def new_cycle():
    x_coor_list=[12.5,62.5,112.5,37.5,87.5,12.5,62.5,112.5,37.5,87.5]
    y_coor_list=[87.5,87.5,87.5,62.5,62.5,37.5,37.5,37.5,12.5,12.5]
    id_list=[1,1,1,2,2,2,2,3,3,3]
    normal_ids=[1,2,3,4,5,6,7,8,9,10]
    for i in range(10):
        node_obj=node(normal_ids[i],id_list[i],x_coor_list[i],y_coor_list[i],)
        alive_node_list.append(node_obj)

def rejuvinate():
    for item in alive_node_list:
        item.energy=0.5

def calc_ffs_HC(aliv_node_list):
    master_list=[]
    for i in range(len(aliv_node_list)):
        z=aliv_node_list[i]
        data=[z.id_normal,z.x_coordinate(),z.y_coordinate(), z.whats_my_energy(),z.whats_my_humidity(),z.id]
        master_list.append(data)

    df = pd.DataFrame()
    df = df.append(master_list)
    df.columns = ['ID', 'x-coordinate', 'y-coordinate','Energy','current humidity', 'type']
    kobj = KMeans(init='k-means++', n_clusters=3, n_init=12)
    kobj.fit(df)
    lola = kobj.labels_
    df['Cluster Labels'] = lola
    lila = kobj.cluster_centers_
    lila1 = []
    for item in range(0, 3):
        lila1.append(int(lila[item][0]))
    nlen = len(aliv_node_list)
    clust1 = []
    clust2 = []
    clust3 = []

    for num in range(nlen):
        flag = list(df.iloc[num][:])
        if flag[6] == 0.0:
            ide = int(flag[0])
            req = aliv_node_list[ide - 1]
            clust1.append(req)

        elif flag[6] == 1.0:
            ide = int(flag[0])
            req = aliv_node_list[ide - 1]
            clust2.append(req)
        else:
            ide = int(flag[0])
            req = aliv_node_list[ide - 1]
            clust3.append(req)
    id0 = lila1[0]
    id1 = lila1[1]
    id3 = lila1[2]

    for item in aliv_node_list:
        if id0 == item.id_normal:
            clust_head_1 = node
        if id1 == item.id_normal:
            clust_head_2= node
        if id3 == item.id_normal:
            clust_head_3= node

    return_package=[clust_head_1,clust1, clust_head_2,clust2, clust_head_3,clust3 ]
    return return_package

def only_alive(all_node_list):
    final_list=[]
    for i in range(len(all_node_list)):
        if all_node_list[i].energy>0:
            final_list.append(all_node_list[i])
    return final_list

def calcffE2(current, bs):
    distance = euclidean_distance(current, bs)
    if current.energy == 0.5:
        ff = 1 / (distance * current.energy * current.energy)
    else:
        de = 0.5 - current.energy  # dissipated energy
        ff = 1 / (distance * de * de)
    return ff

def euclidean_distance(node1, node2):
    x1 = node1.x_coor
    x2 = node2.x_coor
    y1 = node1.y_coor
    y2 = node2.y_coor
    dist = ma.sqrt(ma.pow(x1 + x2, 2) + ma.pow(y1 + y2, 2))
    return dist

def find_forwarder(normal_node_list, bs):
    ff_list = []
    l = len(normal_node_list)
    for i in range(0, l):
        ff_list.append(calcffE2(normal_node_list[i], bs))

    reqn = min(ff_list)
    for i in range(0, l):
        if reqn == ff_list[i]:
            index = i
    return normal_node_list[index]

def nm(clustlist, bs):
    lambo = []
    residue = 0
    pack = 0
    ans = find_forwarder(clustlist, bs)
    num = len(clustlist)
    for i in range(num):
        if clustlist[i].id_normal != ans.id_normal:
            clustlist[i].updating_in_case_normal()
            residue = residue + clustlist[i].energy
    ans.updating_in_case_forwarder()
    residue = residue + ans.energy
    return residue

def appendrow(list_of_elem):
    # Open file in append mode
    with open('agricode_sim.csv', 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)



## Driver Code
recharged=0
current_dead_nodes=0
new_cycle()
i=0
for i in range(14281):
    interim1=0
    interim2=0
    interim3=0
    hourly_time_stamp=i
    currently_alive=only_alive(alive_node_list)
    if (len(currently_alive)<=0):
        rejuvinate()
        recharged=recharged+1
    current_dead_nodes=10-len(currently_alive)

    for node in currently_alive:
        if (node.humidity<=35):
            water_added=70-node.humidity
            node.humidity=70
            global_total=global_total+water_added
        node.update_humidity()

    answer=calc_ffs_HC(currently_alive)

    if (answer[0].energy<=0.1):
        interim1=nm(answer[1],bs)

    else:
        len1 = len(answer[1])
        for i in range(0, len1):
            if answer[1][i].id_normal != answer[0].id_normal:
                answer[1][i].updating_in_case_normal()
                interim1 = interim1 + answer[1][i].energy
            else:
                answer[1][i].updating_in_case_forwarder()
                interim1 = interim1 + answer[1][i].energy



    if (answer[2].energy<=0.1):
        interim2=nm(answer[3],bs)

    else:
        len2 = len(answer[3])
        for i in range(0, len2):
            if answer[3][i].id_normal != answer[2].id_normal:
                answer[3][i].updating_in_case_normal()
                interim2 = interim2 + answer[3][i].energy
            else:
                answer[3][i].updating_in_case_forwarder()
                interim2 = interim2 + answer[3][i].energy

    if (answer[4].energy<=0.1):
        interim3=nm(answer[5],bs)
    else:
        len3 = len(answer[5])
        for i in range(0, len3):
            if answer[5][i].id_normal != answer[4].id_normal:
                answer[5][i].updating_in_case_normal()
                interim3 = interim3 + answer[5][i].energy
            else:
                answer[5][i].updating_in_case_forwarder()
                interim3 = interim3 + answer[5][i].energy

    global_residue=interim1+interim2+interim3
    writable=[global_residue,i+1,global_total, current_dead_nodes, recharged]
    appendrow(writable)


