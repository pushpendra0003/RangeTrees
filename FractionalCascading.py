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
        self.next = None

class ListNode():
    def __init__(self) ->None:
        self.list=None
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
            # print(point.value)
            value = point.value[0]

        else:
            value = point.value[1]

    return value
        
def FindSplitNode(root, p_min , p_max, dim, enable ):
    
    splitnode = root

    while splitnode != None:
        node = splitnode.value

        if p_max < node:
            splitnode = splitnode.left

        elif p_min > node:
            splitnode = splitnode.right

        elif p_min <= node <= p_max :
            break

    return splitnode

def lower(frac:ListNode, x):
    if frac==None:
        return len(frac.list)
    low = 0
    high = len(frac.list)-1
    ans = len(frac.list)
    while low<=high :
        mid = (low+high)//2
        if(frac.list[mid].value>=x):
            ans = mid
            high=mid-1
        else:
            low=mid+1
    return ans


'''def SearchRangeTree1d (tree:Node,frac:ListNode,data,x1,x2,y1,y2,z1,z2):
    res=[]
    if(x1>x2):
        return []
    if(z1>z2):
        return []
    if(x1<=z1 and z2<=x2):
        return find_y(tree,frac,data,y1,y2)
    if(tree.isLeaf):
        if(x1<=x2 and x1<=tree.value<=x2 ):
            return find_y(tree,frac,data,y1,y2)
        else:
            return []
    if(tree.value<x1):
        res+=SearchRangeTree1d(tree.right,frac,data,x1,x2,y1,y2,z1,z2)
        return res
    elif(tree.value>=x2):
        res+=SearchRangeTree1d(tree.left,frac,data,x1,x2,y1,y2,z1,z2)
        return res
    res+=SearchRangeTree1d(tree.right,frac,data,tree.value,x2,y1,y2,tree.value,z2)
    res+=SearchRangeTree1d(tree.left,frac,data,x1,tree.value,y1,y2,z1,tree.value)
    return res'''

def find_y(frac:ListNode,y1,y2, yel:ListNodeNode):
    result=[]
    # print(frac.list[0].value)
    # print(yel.value)
    while(yel):
        if(y1<=yel.value<=y2):
            result.append(data[yel.index])
            yel=yel.next
        else:
            break
    return result


def SearchRangeTree1d (tree, x1, x2, y1, y2):
    '''
    Performs 2D range search
    Arguments:
        tree        : A Node in tree
        x1          : Starting range for x-coord
        x2          : Ending range for x-coord
        y1          : Starting range for y-coord
        y2          : Ending range for y-coord
        dimension   : specifies the dimension of range tree. By default 2
    Returns : Results from 2D search
    '''
    results = []
    splitnode = FindSplitNode(tree, x1, x2, 2, True)
    if (splitnode == None):
        return results
    yel = None
    if splitnode.assoc is not None:
        yel = splitnode.assoc.list[lower(splitnode.assoc, y1)]
    if yel is None:
        return results
    
    # print(splitnode.value)
    # print(yel.value)
    vl = splitnode.left 
    yel1 = yel.left
    # print(yel1.value)
    while ( vl != None ):
        # print("s", vl.value)
        if(vl.isLeaf) and withinRange((vl.value, vl.assoc.list[0].value), ((x1, x2), (y1, y2)), 2):
            results.append([vl.value, vl.assoc.list[0].value])

        if (x1 <= vl.value):
            if vl.right != None:
                # print(yel1.right.value)
                results += find_y(vl.right.assoc, y1, y2, yel1.right)
            vl = vl.left
            yel1 = yel1.left
        else:
            vl = vl.right
            yel1 = yel1.right

    vr = splitnode.right
    yel1 = yel.right
    while ( vr != None ):
        # print(vr.value)
        if ( x2 >= vr.value):
            if vr.left != None:
                results += find_y(vr.left.assoc, y1, y2, yel1.left)
            vr = vr.right
            yel1 = yel.right
        else:
            vr = vr.left
            yel1 = yel1.left
    
    return results

def ConstructRangeTree1d(data):

    data.sort(reverse = False, key=lambda x: x[0])
    # print(data)
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

def givenext(frac:ListNode):
    for i in range(0, len(frac.list)):
        if i+1<len(frac.list):
            frac.list[i].next = frac.list[i+1]
    return frac

def merge(yl:ListNode,yr:ListNode):
    lc = []
    rc = []
    for i in yl.list:
        temp = ListNodeNode(i.value)
        temp.index = i.index
        lc.append(temp)
    for i in yr.list:
        temp = ListNodeNode(i.value)
        temp.index = i.index
        rc.append(temp)
    y=ListNode()
    l = []
    
    if(yl != None):
        l = l+lc

    if(yr != None):
        l = l+rc

    if(len(l)==0):
        return None

    l.sort(reverse=False,key=lambda x:x.value)

    for i in l:

        if(yl):
            left_index=lower(yl, i.value)

            if(left_index>=len(yl.list)):
                i.left=None

            else:
                i.left=yl.list[left_index]
        else:
            i.left = None

        if(yr):
            right_index=lower(yr, i.value)

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
    y = givenext(y)
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

def Display(root:ListNode):

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
                if(i.left!=None):
                    print(i.left.value)
                if(i.right is not None):
                    print(i.right.value)
                print("a")
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
# print(data)
ynode = ConstructFrac(0, len(data)-1, data, node)
# Display(ynode)
print("Enter minimum value of x")
mnx = int(input())
print("Enter minimum value of y")
mny = int(input())
print("Enter maximum value of x")
mxx = int(input())
print("Enter maximum value of y")
mxy = int(input())
ans = SearchRangeTree1d(node, mnx, mxx, mny, mxy)


if mnx > mxx or mny > mxy:
    print("Invalid Argument")
elif not ans:
    print("No points found in the given range")
else:
    print("Points in given range:", ans)