import csv
import os
    
class Node(object):

    """A node in a Range Tree."""

    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.isLeaf = False
        self.assoc = None

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
    data.sort()
    #print(data)
    if not data:
        return None
    if len(data) == 1:
        node = Node(data[0])
        node.isLeaf = True
    else:
        mid_val = len(data)//2
        node = Node(data[mid_val])
        node.left = ConstructRangeTree1d(data[:mid_val])
        node.right = ConstructRangeTree1d(data[mid_val+1:])
    return node

def ConstructRangeTree2d(data, enable=True):
    '''
    Construct a 2 dimensional range tree

    Arguments:
        data         : The data to be stored in range tree
        enable       : to toggle whether to build the xtree or ytree
    Returns:
        Root node of the entire tree
    '''
    data.sort(reverse = False, key=lambda x: x[0])
    #print(data)
    if not data:
        return None
    if len(data) == 1:
        node = Node(data[0])
        node.isLeaf = True
    else:
        mid_val = len(data)//2
        node = Node(data[mid_val])  # node.value = (x,y)
        node.left = ConstructRangeTree2d(data[:mid_val], enable)
        node.right = ConstructRangeTree2d(data[mid_val+1:], enable)
    if enable:
        node.assoc = ConstructRangeTree2d( sorted(data, key=lambda x: x[1]), enable=False)
    return node

#date1, date2,  param1=None, x1=None, x2=None, dimension=1):
    '''
    Handles all function calls

    Arguments:
        Countries   : A country name from the drop down list. String data type.
        date1       : Starting date for range query
        date2       : Ending date for range query
        param1      : The first column number to be read from the excel file . By default is None else should be a valid integer value
        x1          : Starting value for range query related to param1. By default is None
        x2          : Ending value for range query related to param1. By default is None
        dimension   : specifies the dimension of range tree. By default 1

    Returns : None
    ''' 
dim = int(input("Dimension of the data: "))
data = LoadData(dim)

#print(data)

if dim == 1:
    node = ConstructRangeTree1d(data)
    mn = int(input("Give Min Value: "))
    mx = int(input("Give Max Value: "))
    ans = SearchRangeTree1d(node, mn, mx, 1, True)
else:
    node = ConstructRangeTree2d(data)
    mnx = int(input())
    mny = int(input())
    mxx = int(input())
    mxy = int(input())
    ans = SearchRangeTree2d(node, mnx, mxx, mny, mxy, dim)

print("points" , ans)
    
    



