import csv
import os
import bisect
from queue import Queue

class Node(object):

    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.isLeaf = False
        self.assoc = None

class ListNodeNode(object):
    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.index = None

class ListNode():
    def __init__(self) ->None:
        self.list=[]
        self.left=None
        self.right=None
        self.isleaf=None


def LoadData(dim):

    if dim == 2:
        with open("Data.csv") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            readCSV = list(readCSV)

            for i in range(0, len(readCSV)):
                for j in range(0, 2):
                    readCSV[i][j] = eval(readCSV[i][j])

    else:
        with open("Data1.csv") as csvfile:
            readCSV = csv.reader(csvfile)
            readCSV = list(readCSV)

            for i in range(0, len(readCSV)):
                readCSV[i] = eval(readCSV[i][0])

    return readCSV

def withinRange(point, range , check):

    if check == 1:
        x = point

        if (x >= range[0][0]  and x <= range[0][1] ) :
            return True
        
        else:
            return False
        
    elif check == 2:
        x = point[0]
        y = point[1]

        if (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) :
            return True
        
        else:
            return False
        
def getValue (point, enable, dim ):

    if dim == 1:
        value = point.value

    elif dim == 2:

        if enable:
            value = point.value[0]

        else:
            value = point.value[1]

    return value
        
def FindSplitNode(root, p_min , p_max, dim, enable ):
    
    splitnode = root

    while splitnode != None:
        node = getValue(splitnode, enable, dim)

        if p_max < node:
            splitnode = splitnode.left

        elif p_min > node:
            splitnode = splitnode.right

        elif p_min <= node <= p_max :
            break

    return splitnode

def SearchRangeTree1d (tree:Node,frac:ListNode,data,x1,x2,y1,y2,z1,z2):
    res=[]
    if(x1>x2):
        return []
    if(z1>z2):
        return []
    if(x1<=z1 and z2<=x2):
        print("gandu")
        return find_y(tree,frac,data,y1,y2)
    if(tree.isLeaf):
        if(x1<=x2 and x1<=tree.value<=x2 ):
            return find_y(tree,frac,data,y1,y2)
        else:
            return []
    if(tree.value<x1):
        res+=SearchRangeTree1d(tree.right,frac,data,x1,x2,y1,y2,z1,z2)
        return res
    elif(tree.value>x2):
        res+=SearchRangeTree1d(tree.left,frac,data,x1,x2,y1,y2,z1,z2)
        return res
    res+=SearchRangeTree1d(tree.right,frac,data,tree.value,x2,y1,y2,tree.value,z2)
    res+=SearchRangeTree1d(tree.left,frac,data,x1,tree.value,y1,y2,z1,tree.value)
    return res

def find_y(tree,frac,data,y1,y2):
    result=[]
    l_y=tree.assoc
    i=0
    while(i<len(l_y.list)):
        if(y1<=l_y.list[i].value<=y2):
            result.append(data[l_y.list[i].index])
            i+=1
        else:
            break
    return result


def SearchRangeTree2d (tree:Node,frac:ListNode,x1, x2, y1, y2, dim ):
    
    results = []
    splitnode = FindSplitNode(tree,x1, x2, 2, True)

    if (splitnode == None):

        return results
    
    

    vl = splitnode.left 

    while ( vl != None ):

        if withinRange(vl.value, [[x1, x2], [y1, y2]], 2):
            results.append(vl.value)

        if (x1 < vl.value[0]):
            if vl.right != None:
                results += SearchRangeTree1d(vl.right.assoc, y1, y2, dim, False)

            vl = vl.left

        else:
            vl = vl.right
            
    vr = splitnode.right

    while ( vr != None ):

        if withinRange(vr.value, [(x1, x2), (y1, y2)], 2):
            results.append(vr.value)

        if ( x2 > vr.value[0] ):
            if vr.left != None:
                results += SearchRangeTree1d(vr.left.assoc, y1, y2, dim, False)

            vr = vr.right

        else:
            vr = vr.left
    
    return results

def ConstructRangeTree1d(data):

    data.sort(reverse = False, key=lambda x: x[0])

    if not data:
        return None
    
    if len(data) == 1:
        node = Node(data[0][0])
        node.isLeaf = True

    else:
        mid_val = (len(data)-1)//2
        node = Node(data[mid_val][0])
        node.left = ConstructRangeTree1d(data[:mid_val+1])
        node.right = ConstructRangeTree1d(data[mid_val+1:])

    return node

def merge(yl:ListNode,yr:ListNode):
    y=ListNode()
    l = []
    
    if(yl != None):
        l = l+yl.list

    if(yr != None):
        l = l+yr.list

    if(len(l)==0):
        return None

    l.sort(reverse=False,key=lambda x:x.value)

    for i in l:

        if(yl):
            left_index=bisect.bisect_left(yl.list, i.value, lo=0, hi=len(yl.list),key=lambda x:x.value)

            if(left_index>=len(yl.list)):
                i.left=None

            else:
                i.left=yl.list[left_index]
        else:
            i.left = None

        if(yr):
            right_index=bisect.bisect_left(yr.list, i.value, lo=0, hi=len(yr.list),key=lambda x:x.value)

            if(right_index>=len(yr.list)):
                i.right=None

            else:
                i.right=yr.list[right_index]

        else:
            i.right = None

        if(i.left==None and i.right==None):
            i.isleaf=True

        else:
            i.isleaf=False

    y.list=l
    y.left=yl
    y.right=yr

    if((y.left ==  None) and (y.right == None)):
        y.isleaf=  True

    else:
        y.isleaf = False

    return y    

def ConstructFrac(l, r, data, node:Node):

    if node==None:
        return None

    if l>r:
        return None
    
    if(l==r):
        n = ListNodeNode(data[l][1])
        # print(l)
        y = ListNode()
        y.list = [n]
        n.index = l
        node.assoc = y
        return y

    mid = (r+l)//2
    y_l = ConstructFrac(l, mid, data, node.left)
    y_r = ConstructFrac(mid+1, r, data, node.right)
    y = merge(y_l, y_r)
    node.assoc = y
    return y

# def Display(root:ListNode):

    if root is None:
        return
    
    queue = []
    queue.append(root)
    current_level = 1

    while queue:
        level_size = len(queue)
        print(f"Level {current_level}:", end=" ")
        print()

        for _ in range(level_size):
            node = queue.pop(0)

            for i in node.list:
                print(f"{i.value} {i.index}")
            print()

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        current_level += 1
        print()

data = LoadData(2)
data.sort(reverse = False, key=lambda x:x[0])
node = ConstructRangeTree1d(data)
print(data)
ynode = ConstructFrac(0, len(data)-1, data, node)
# Display(ynode)
mnx = int(input())
mny = int(input())
mxx = int(input())
mxy = int(input())
ans = SearchRangeTree1d(node,ynode, data, mnx, mxx, mny, mxy, -100000, 100000)


print("points",ans)
