import csv
import os
import bisect
class Node(object):

    """A node in a Range Tree."""

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
    #print(readCSV)
    return readCSV

def withinRange(point, range , check):

    '''
    Checks if the value of node is within the required range
    Arguments:
        point       : A point in tree
        range       : A list containing range to be checked with
        check       : specifies which option should be performed
    Returns :
        True if in range else False
    '''

    if check == 1:
        x = point
        if (x >= range[0][0]  and x <= range[0][1] ) :
            return True
        else:
            return False
    elif check == 2:
        x = point[0]
        y = point[1]
        #print(x, y)
        if (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) :
            return True
        else:
            return False
        
        
def getValue (point, enable, dim ):

    '''
    Reads the desired value from node
    Arguments:
        point       : A point in tree
        enable      : True when we need to read first coord of point when used as a helper function by 2D range search
        dimension   : specifies the dimension of range tree.
    Returns : value of node
    '''
    if dim == 1:
        value = point.value
    elif dim == 2:
        if enable:
            value = point.value[0]
        else:
            value = point.value[1]
    return value

        
def FindSplitNode(root, p_min , p_max, dim, enable ):
    '''
    Searches for a common node that splits the range
    Arguments:
        tree        : A Node in tree
        p_min       : Starting range 
        p_max       : Ending range 
        dimension   : specifies the dimension of range tree.
        enable      : True when we need to read first coord of point when used as a helper function by 2D range search
    Returns : A Node
    '''
    #print(dim, enable)
    splitnode = root
    while splitnode != None:
        node = getValue(splitnode, enable, dim)
        #print(node)
        if p_max < node:
            splitnode = splitnode.left
        elif p_min > node:
            splitnode = splitnode.right
        elif p_min <= node <= p_max :
            break
    return splitnode


def SearchRangeTree1d (tree, p1, p2, dim = 1, enable = True):
    '''
    Performs 1D range search
    Arguments:
        tree        : A Node in tree
        p1          : Starting range 
        p2          : Ending range 
        dimension   : specifies the dimension of range tree. By default 1
        enable      : True when we need to read first coord of point when used as a helper function by 2D range search
    Returns : list of result of range query
    '''
    #print("this", tree.value)
    nodes = []
    #print("AS")
    #print(tree)
    #print(enable, dim)
    splitnode = FindSplitNode(tree , p1, p2, dim, enable)
    # print("asqw")
    #print(dim, enable, getValue(splitnode, enable, dim))
    if splitnode == None:
        return nodes
    elif withinRange(getValue(splitnode, enable, dim) , [(p1, p2)], 1):
        print("appended", splitnode.value)
        nodes.append(splitnode.value)
    nodes += SearchRangeTree1d(splitnode.left, p1, p2, dim, enable)
    # print("Adsa")
    nodes += SearchRangeTree1d(splitnode.right, p1, p2, dim, enable)
    return nodes

def SearchRangeTree2d (tree, x1, x2, y1, y2, dim ):
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
    #print("split", splitnode.value)
    if (splitnode == None):
        return results
    if withinRange(splitnode.value, [[x1, x2], [y1, y2]], 2) :
        #print("sa")
        results.append(splitnode.value)

    vl = splitnode.left 
    while ( vl != None ):
        # print("as")
        #print("ycheck", vl.value)
        if withinRange(vl.value, [[x1, x2], [y1, y2]], 2):
            #print("appended")
            results.append(vl.value)
        if (x1 < vl.value[0]):
            #print("q")
            if vl.right != None:
                # print("Y")
                results += SearchRangeTree1d(vl.right.assoc, y1, y2, dim, False)
                # print("vb")
            vl = vl.left
        else:
            vl = vl.right
            #print(vl.value)

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
    '''
    Construct a 1 dimensional range tree

    Arguments:
        data         : The data to be stored in range tree
    Returns:
        Root node of the entire tree
    '''
    data.sort(reverse = False, key=lambda x: x[0])
    #print(data)
    if not data:
        return None
    if len(data) == 1:
        node = Node(data[0][0])
        node.isLeaf = True
    else:
        mid_val = (len(data)-1)//2
        node = Node(data[mid_val][0])
        node.left = ConstructRangeTree1d(data[:mid_val])
        node.right = ConstructRangeTree1d(data[mid_val+1:])
    #print("c", node.value)
    return node

def merge(yl:ListNode,yr:ListNode, val):
    #print("sad", val)
    y=ListNode()
    l = [ListNodeNode(val)]

    if(yl != None):
        l = l+yl.list
    if(yr != None):
        l = l+yr.list
    if(len(l)==0):
        return None
    #else:

        #for i in l:
           #print(i.value)
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
    #for i in y.list:
        #print(i.value)
    return y    

def ConstructFrac(l, r, data, node:Node):
    print("kins", l, r)
    if node==None:
        return None
    #else:
        #print("s", node.value)
    if l>r:
        #print("ad")
        return None
    if(l==r):
        n = ListNodeNode(data[l][1])
        #print(n.value)
        y = ListNode()
        y.list = [n]
        #print("sww", len(y.list))
        node.assoc = y
        #for i in y.list:
            #print(i.value)
        #print("Asd")
        return y

    mid = (r-l)//2
    #print("m", data[mid])
    y_l = ConstructFrac(l, mid-1, data, node.left)
    y_r = ConstructFrac(mid+1, r, data, node.right)
    #print("sad", data[mid][1])
    y = merge(y_l, y_r, data[mid][1])
    #print("done")
    node.assoc = y
    #for i in y.list:
        #print(i.value)
    return y

def InOrder(ynode:ListNode):
    if ynode==None:
        #print("Sd")
        return 
    else:
        InOrder(ynode.left)
        for i in ynode.list:
            print(i.value)
        print(" ")
        InOrder(ynode.right)

    return 

data = LoadData(2)
data.sort(reverse = False, key=lambda x:x[0])
#print(data)

node = ConstructRangeTree1d(data)
print(data)
ynode = ConstructFrac(0, len(data)-1, data, node)
#print("A")
InOrder(ynode)
#mnx = int(input())
#mny = int(input())
#mxx = int(input())
#mxy = int(input())
#ans = SearchRangeTree2d(node, mnx, mxx, mny, mxy, 2)


#print("points" , ans)