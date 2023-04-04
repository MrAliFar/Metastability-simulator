
class event:
    def __init__(self, _priority, _time, _type, _srvc, _agent):
        #### The priority of the event
        self.priority = _priority
        #### The time slot at which it has to be done, if possible
        self.time = _time
        #### The type of the event
        self.type = _type
        #### The service(s) to which the event belongs
        self.srvc = _srvc
        #### The agent(s) to which the event belongs
        self.agent = _agent



# Function to heapify the tree
def heapify(arr, n, i):
    # Find the largest among root, left child and right child
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[i].priority < arr[l].priority:
        largest = l

    if r < n and arr[largest].priority < arr[r].priority:
        largest = r

    # Swap and continue heapifying if root is not largest
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# Function to insert an element into the tree
def insert(array, newEvent):
    size = len(array)
    if size == 0:
        array.append(newEvent)
    else:
        array.append(newEvent)
        for i in range((size // 2) - 1, -1, -1):
            heapify(array, size, i)


# Function to delete an element from the tree
def deleteNode(array, event):
    size = len(array)
    i = 0
    for i in range(0, size):
        if event == array[i]:
            break

    array[i], array[size - 1] = array[size - 1], array[i]

    array.pop(len(array)-1)

    for i in range((len(array) // 2) - 1, -1, -1):
        heapify(array, len(array), i)



ev1 = event(5, 1, 1, 1, 2)
ev2 = event(5, 2, 1, 2, 2)
ev3 = event(5, 3, 2, 1, 4)
ev4 = event(5, 4, 2, 11, 4)
ev5 = event(5, 5, 2, 11, 4)

arr = []
insert(arr, ev1)
insert(arr, ev2)
insert(arr, ev3)
insert(arr, ev4)
insert(arr, ev5)

print(f"Array elements before deletion: {arr[0].time}, {arr[1].time}, {arr[2].time}, {arr[3].time}")

deleteNode(arr, ev3)

for i in range(len(arr)):
    print(f"Array elements after first deletion: {arr[i].time}")

deleteNode(arr, ev5)

for i in range(len(arr)):
    print(f"Array elements after second deletion: {arr[i].time}")


# arr = []

# insert(arr, 3)
# insert(arr, 3)
# insert(arr, 3)
# insert(arr, 1)
# insert(arr, 1)

# print ("Max-Heap array: " + str(arr))

# deleteNode(arr, 3)
# print("After deleting an element: " + str(arr))

# deleteNode(arr, 3)
# print("After deleting two elements: " + str(arr))