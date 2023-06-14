import math as ma
from csv import writer
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans



class sink:
    # constructor to initialize the sink
    def __init__(self):
        self.x = 0.25
        self.y = 0.1

sinky = sink()
# ---------------------------------------------------------------------------------------------
dummy = pow(10, -9)
ETX = 16.7 * dummy  # this is the energy dissipated on transmission of bit package
ERX = 36.1 * dummy  # this is the energy consumed at the time of recieving of the bit package
EDA = 5.0 * dummy
Emp = 1.97 * dummy  # this is the energy cnsumed at the time of bit amplification
lamb = 0.125
c = 299792458
d0 = 0.1
packets_to_CH = 0
r = 8000  # the total  number of transmission cycles or rounds
node = 8
dead_node = 0
packtosink = 0
packtoforwarder = 0
failed = 0
primelist = []
failed = 0
flags = 0
rounds = 1
dead = 0


# ----------------------------------------------------------------------------------------------
class node:
    # constructor to each node to initialize with standard values
    def __init__(self, weird, id, x, y, type):
        self.id = id
        self.E = 0.5
        self.type = type
        self.statusflag = 0
        self.x = x
        self.y = y
        self.humidity = 70
        self.waldo=weird

    def update_humidity(self):
        if self.waldo==1:
            self.humidity = self.humidity - (3.0 / 24)
        elif self.waldo==2:
            self.humidity = self.humidity - (3.5 / 24)
        elif self.waldo==3:
            self.humidity = self.humidity - (4.0 / 24)

    def replenish(self):
        self.humidity=self.humidity+35
        global_total=+35

    # now i shal define a function that updates the energy of each node after transmission is over in case the node is a a normal node
    def updating_in_case_normal(self):
        d = euclidean_distance(self, sinky)
        self.E = self.E - ((ETX) * (4000) + Emp * 3.38 * 4000 * (ma.pow(d, 3.38)))

    def updating_in_case_forwarder(self):
        d = euclidean_distance(self, sinky)
        self.E = self.E - ((ETX + ERX + EDA) * (4000) + Emp * 3.38 * 4000 * (ma.pow(d, 3.38)))


# ----------------------------------------------------------------------------------------------
def calcffE2(nody, sinky):
    distance = euclidean_distance(nody, sinky)
    if nody.E == 0.5:
        ff = 1 / (distance * nody.E * nody.E)
    else:
        de = 0.5 - nody.E  # dissipated energy
        ff = 1 / (distance * de * de)
    return ff


# ----------------------------------------------------------------------------------------------
def euclidean_distance(node1, node2):
    x1 = node1.x
    x2 = node2.x
    y1 = node1.y
    y2 = node2.y
    dist = ma.sqrt(ma.pow(x1 + x2, 2) + ma.pow(y1 + y2, 2))
    return dist


# ----------------------------------------------------------------------------------------------
def find_forwarder(normal_node_list, sinky):
    ff_list = []
    # fin=[]
    l = len(normal_node_list)
    for i in range(0, l):
        ff_list.append(calcffE2(normal_node_list[i], sinky))
    # req=sum(ff_list)
    # avg=req/l
    # for i in range(0,l):
    # fin.append(avg-ff_list[i])
    reqn = min(ff_list)
    for i in range(0, l):
        if reqn == ff_list[i]:
            index = i
    return normal_node_list[index]


# ----------------------------------------------------------------------------------------------
def nm(head, clustlist, sinky):
    lambo = []
    residue = 0
    pack = 0
    ans = find_forwarder(clustlist, sinky)
    num = len(clustlist)
    for i in range(0, num):
        if clustlist[i].id != ans.id:
                clustlist[i].updating_in_case_normal()
                residue = residue + clustlist[i].E
        ans.updating_in_case_forwarder()
        residue = residue + ans.E
    pack = pack + 1
    lambo.append(residue)
    lambo.append(0)
    lambo.append(pack)
    return lambo


# ----------------------------------------------------------------------------------------------
def appendrow(list_of_elem):
    # Open file in append mode
    with open('idebforIDEB.csv', 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

# ----------------------------------------------------------------------------------------------
for num in range(2, 5000):
    if all(num % i != 0 for i in range(2, num)):
        primelist.append(num)
x_list = [0.4, 0.3, 0.5, 0.3, 0.5, 0.37, 0.45, 0.7, 0.1]
y_list = [0.9, 0.1, 0.3, 0.55, 0.55, 0.75, 0.9, 0.8, 0.8]
type_list = [1, 1, 1, 1, 1, 2, 2, 1, 1]
id_list = [1, 2, 3, 4, 5, 8, 9, 6, 7]
waldo_list=[1,1,1,2,2,2,2,3,3,3]
node_list = []
for i in range(0, 9):
    new_node = node(waldo_list[i],id_list[i], x_list[i], y_list[i], type_list[i])
    node_list.append(new_node)
# ----------------------------------------------------------------------------------------------
writable_content = []
# ----------------------------------------------------------------------------------------------
global_total=6377.999999999994
d=5131
while(node_list):
    d=d+1
    total_residue = 0
    onerow = []
    df = pd.DataFrame()
    free = []
    for node in node_list:
        if (node.humidity<=35):
            water_added=70-node.humidity
            node.humidity=70
            global_total=global_total+water_added
        node.update_humidity()

    for node in node_list:
        data = []
        data.append(node.id)
        data.append(node.E)
        data.append(node.x)
        data.append(node.y)
        data.append(node.type)
        free.append(data)

    df = df.append(free)
    df.columns = ['ID', 'Energy', 'x-coordinate', 'y-coordinate', 'type']
    kobj = KMeans(init='k-means++', n_clusters=3, n_init=12)
    kobj.fit(df)
    lola = kobj.labels_
    df['Cluster Labels'] = lola
    lila = kobj.cluster_centers_
    lila1 = []
    for item in range(0, 3):
        lila1.append(int(lila[item][0]))
    nlen = len(node_list)
    clust1 = []
    clust2 = []
    clust3 = []

    for num in range(0, 9):
        flag = list(df.iloc[num][:])
        if flag[5] == 0.0:
            ide = int(flag[0])
            req = node_list[ide - 1]
            clust1.append(req)

        elif flag[5] == 1.0:
            ide = int(flag[0])
            req = node_list[ide - 1]
            clust2.append(req)
        else:
            ide = int(flag[0])
            req = node_list[ide - 1]
            clust3.append(req)
    id0 = lila1[0]
    id1 = lila1[1]
    id3 = lila1[2]
    for node in node_list:
        if id0 == node.id:
            require = node
        if id1 == node.id:
            rec = node
        if id3 == node.id:
            re = node

    if require.E <= 0.1:
        lambo = nm(require, clust1, sinky)
        total_residue = total_residue + lambo[0]
        failed = failed + lambo[1]
        packtosink = packtosink + lambo[2]
    else:
        len1 = len(clust1)
        for i in range(0, len1):
            if clust1[i].id != lila1[0]:
                if flags in primelist:
                    clust1[i].updating_in_case_normal()
                    failed = failed + 1
                    total_residue = total_residue + clust1[i].E
                    flags = flags + 1
                else:
                    clust1[i].updating_in_case_normal()
                    packtoforwarder = packtoforwarder + 1
                    total_residue = total_residue + clust1[i].E
            else:
                clust1[i].updating_in_case_forwarder()
                total_residue = total_residue + clust1[i].E
            packtosink = packtosink + 1
    if rec.E <= 0.1:
        lambo = nm(rec, clust2, sinky)
        total_residue = total_residue + lambo[0]
        failed = failed + lambo[1]
        packtosink = packtosink + lambo[2]
    else:
        len2 = len(clust2)
        for i in range(0, len2):
            if clust2[i].id != lila1[1]:
                if flags in primelist:
                    clust2[i].updating_in_case_normal()
                    failed = failed + 1
                    total_residue = total_residue + clust2[i].E
                    flags = flags + 1
                else:
                    clust2[i].updating_in_case_normal()
                    packtoforwarder = packtoforwarder + 1
                    total_residue = total_residue + clust2[i].E
            else:
                clust2[i].updating_in_case_forwarder()
                total_residue = total_residue + clust2[i].E
                packtosink = packtosink + 1
    if re.E <= 0.1:
        lambo = nm(rec, clust3, sinky)
        total_residue = total_residue + lambo[0]
        failed = failed + lambo[1]
        packtosink = packtosink + lambo[2]
    else:
        len3 = len(clust3)
        for i in range(0, len3):
            if clust3[i].id != lila1[2]:
                if flags in primelist:
                    clust3[i].updating_in_case_normal()
                    failed = failed + 1
                    total_residue = total_residue + clust3[i].E
                    flags = flags + 1
                else:
                    clust3[i].updating_in_case_normal()
                    packtoforwarder = packtoforwarder + 1
                    total_residue = total_residue + clust3[i].E
            else:
                clust2[i].updating_in_case_forwarder()
                total_residue = total_residue + clust3[i].E
                packtosink = packtosink + 1

    new_list = clust1 + clust2 + clust3
    for node in new_list:
        if node.E <= 0:
            new_list.remove(node)
            dead = dead + 1


    rounds = rounds + 1
    flags = flags + 1

    writable = [d, packtosink, failed, total_residue, dead, global_total]
    appendrow(writable)


