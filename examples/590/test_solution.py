from typing import List, Any, Iterable, Union, Set, Callable, Optional
from functools import wraps
from collections import deque

import pytest

import solution

TreeNode_INVOLVED = False
TreeNode_PARAMS = {'root'}

ListNode_INVOLVED = True
ListNode_PARAMS = {'head'}

Node_INVOLVED = True
Node_PARAMS = {'root'}

'''
CLASS
'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children


'''
SERIALIZATION
DESERIALIZATION
'''
def serialize_leetcode_list_node(head: Optional[ListNode]) -> List[Union[int, None]]:
    """
    Serialize a linked list into a list of integers and None values in LeetCode-style.

    Args:
        head (ListNode): The head of the linked list.

    Returns:
        List[Union[int, None]]: The serialized linked list.
    """
    serialized = []
    current = head
    while current:
        serialized.append(current.val)
        current = current.next
    return serialized

def deserialize_leetcode_tree_node(data: List[Union[int, None]]) -> Optional[TreeNode]:
    """
    Deserializes a LeetCode-style tree input into a TreeNode structure.
    
    Args:
        data (List[Union[int, None]]): A list of integers and None values representing a level-order traversal of a binary tree.
    
    Returns:
        TreeNode: The root of the deserialized binary tree, or None if the input list is empty or contains only None values.
    """
    if not data or data[0] is None:
        return None

    root = TreeNode(data[0])
    queue = deque([root])
    index = 1

    while queue and index < len(data):
        current = queue.popleft()

        if data[index] is not None:
            current.left = TreeNode(data[index])
            queue.append(current.left)
        index += 1

        if index < len(data) and data[index] is not None:
            current.right = TreeNode(data[index])
            queue.append(current.right)
        index += 1

    return root

def serialize_leetcode_tree_node(root: Optional[TreeNode]) -> List[Union[int, None]]:
    """
    Serializes a TreeNode structure into a LeetCode-style tree input.
    
    Args:
        root (TreeNode): The root of the binary tree to be serialized.
    
    Returns:
        List[Union[int, None]]: A list of integers and None values representing a level-order traversal of the input binary tree.
    """
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        current = queue.popleft()

        if current:
            result.append(current.val)
            queue.append(current.left)
            queue.append(current.right)
        else:
            result.append(None)

    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()

    return result

def deserialize_leetcode_list_node(data: Optional[List[Union[int, None]]]) -> ListNode:
    """
    Deserialize a list of integers and None values into a linked list in LeetCode-style.

    Args:
        data (List[Union[int, None]]): The serialized linked list.

    Returns:
        ListNode: The deserialized linked list.
    """
    if not data:
        return None
    nodes = deque(ListNode(val=val) if val is not None else None for val in data)
    head = nodes.popleft()
    current = head
    while nodes:
        node = nodes.popleft()
        current.next = node
        current = node
    return head

def serialize_leetcode_node(root: Optional[Node]) -> List[Union[int, None]]:
    """Serializes an n-ary tree to a list of Union[int, None].
    
    Args:
        root (Optional[Node]): The root node of the n-ary tree.
        
    Returns:
        List[Union[int, None]]: The serialized list representation of the n-ary tree.
    """
    if root is None:
        return []

    def preorder_traversal(node: Node, result: List[Union[int, None]]) -> None:
        if node is None:
            return

        result.append(node.val)

        for child in node.children:
            preorder_traversal(child, result)

        result.append(None)

    result = []
    preorder_traversal(root, result)
    return result

def deserialize_leetcode_node(data: List[Union[int, None]]) -> Optional[Node]:
    """Deserializes a list of Union[int, None] to an n-ary tree.
    
    Args:
        data (List[Union[int, None]]): The serialized list representation of the n-ary tree.
        
    Returns:
        Optional[Node]: The root node of the deserialized n-ary tree.
    """
    data = deque(data)
    root, _ = Node(data.popleft()), data.popleft()

    queue = deque([root])
    while queue:
        node = queue.popleft()

        while data and data[0] != None:
            child = Node(data.popleft())
            if node.children == None:
                node.children = []
            node.children.append(child)
            queue.append(child)
        
        if data:
            data.popleft()

    return root

'''
DECOR
'''
def tree_node_serialization(deserialize_input_params: Optional[Set[str]] = {'root'}, enabled: bool = False) -> Callable[..., List[Union[int, None]]]:
    """
    Decorator to convert a LeetCode-style serialized tree_adaptor input into a deserialized tree before calling the target function,
    and to convert the target function's output into a serialized tree.
    
    Args:
        deserialize_input_params (Optional[Set[str]]): A set of parameter names to deserialize from the input kwargs.
            If None, no parameters will be deserialized.
            Default is {'root'}.

    Returns:
        A wrapped function that takes serialized tree inputs and returns serialized tree outputs.
    """
    
    def decorator(func: Callable[..., TreeNode]) -> Callable[..., List[Union[int, None]]]:
        if enabled:
            @wraps(func)
            def wrapper(*args, **kwargs) -> List[Union[int, None]]:
                for k in deserialize_input_params:
                    if k in kwargs:
                        kwargs[k] = deserialize_leetcode_tree_node(kwargs[k])

                result = func(*args, **kwargs)

                def serialize_tree_node(result):
                    if isinstance(result, Optional[TreeNode]):
                        return serialize_leetcode_tree_node(result)
                    elif isinstance(result, tuple):
                        return tuple(serialize_tree_node(v) for v in result)
                    elif isinstance(result, list):
                        return [serialize_tree_node(v) for v in result]
                    elif isinstance(result, set):
                        return set(serialize_tree_node(v) for v in result)
                    else:
                        return result
                return serialize_tree_node(result)
            
            return wrapper
        else:
            return func

    return decorator

def list_node_serialization(deserialize_input_params: Union[Set[str], List[str], None] = {'head'}, enabled: bool = False) -> Callable[..., List[Union[int, None]]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., List[Union[int, None]]]:
        if enabled:
            @wraps(func)
            def wrapper(*args, **kwargs) -> List[Union[int, None]]:
                for k in deserialize_input_params:
                    if k in kwargs:
                        kwargs[k] = deserialize_leetcode_list_node(kwargs[k])

                result = func(*args, **kwargs)

                def serialize_linked_lists(result):
                    if isinstance(result, Optional[ListNode]):
                        return serialize_leetcode_list_node(result)
                    elif isinstance(result, tuple):
                        return tuple(serialize_linked_lists(v) for v in result)
                    elif isinstance(result, list):
                        return [serialize_linked_lists(v) for v in result]
                    elif isinstance(result, set):
                        return set(serialize_linked_lists(v) for v in result)
                    else:
                        return result
                return serialize_linked_lists(result)
            return wrapper
        else:
            return func
        
    return decorator

def node_serialization(deserialize_input_params: Union[Set[str], List[str], None] = {'root'}, enabled: bool = False) -> Callable[..., List[Union[int, None]]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., List[Union[int, None]]]:
        if enabled:
            @wraps(func)
            def wrapper(*args, **kwargs) -> List[Union[int, None]]:
                for k in deserialize_input_params:
                    if k in kwargs:
                        kwargs[k] = deserialize_leetcode_node(kwargs[k])

                result = func(*args, **kwargs)

                def serialize_tree(result):
                    if isinstance(result, Optional[Node]):
                        return serialize_leetcode_node(result)
                    elif isinstance(result, tuple):
                        return tuple(serialize_tree(v) for v in result)
                    elif isinstance(result, list):
                        return [serialize_tree(v) for v in result]
                    elif isinstance(result, set):
                        return set(serialize_tree(v) for v in result)
                    else:
                        return result
                        
                return serialize_tree(result)
            return wrapper
        else:
            return func
        
    return decorator

def serialization(func):
    @node_serialization(deserialize_input_params=Node_PARAMS, enabled=Node_INVOLVED)
    @tree_node_serialization(deserialize_input_params=TreeNode_PARAMS, enabled=TreeNode_INVOLVED)
    @list_node_serialization(deserialize_input_params=ListNode_PARAMS, enabled=ListNode_INVOLVED)
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

'''
UTILS
'''
def recursive_sorted(arr: List[Any]) -> List[Any]:
    """
    Sorts a list of lists recursively.
    
    Args:
        arr: A list of any types and/or sub-lists.
    
    Returns:
        A sorted list of any types and/or sub-lists.
    """
    if isinstance(arr, Iterable) and all(isinstance(x, type(arr[0])) for x in arr):
        print(type(arr))
        for i in range(len(arr)):
                arr[i] = recursive_sorted(arr[i])
        return sorted(arr)
    return arr

def pop_by_two(cases):
    return [cases[i:i+2] for i in range(0, len(cases), 2)]


'''
================================================
DATA
================================================
'''
INPUT_CASES_PATH = r'./input.txt'
EXPECTED_CASES_PATH = r'./expected.txt'

def read_cases(path: str) -> List[str]:
    cases = []
    with open(path, 'r') as f:
        for line in f:
            cases.append(line.strip().replace('\n', '').replace('null', 'None'))
    return cases

input_cases = read_cases(INPUT_CASES_PATH)
expected_cases = read_cases(EXPECTED_CASES_PATH)


'''
================================================
TEST
================================================
'''
@pytest.mark.ordered
@pytest.mark.unordered
def test_target_function_exist_and_unique():
    obj = solution.Solution()
    public_functions = [x for x in dir(obj) if '__' not in x]
    assert len(public_functions) == 1

@pytest.mark.ordered
@pytest.mark.unordered
def test_number_of_test_case_match():
    assert len(expected_cases) == len(input_cases)

@pytest.mark.ordered
@pytest.mark.parametrize("input_case, expected_case", zip(input_cases, expected_cases))
def test_ordered_output(input_case, expected_case):
    obj = solution.Solution()
    method_name = [x for x in dir(obj) if '__' not in x][0]

    output = eval(f'serialization(obj.{method_name})({input_case})')
    expected = eval(expected_case)
    
    assert output == expected

@pytest.mark.unordered
@pytest.mark.parametrize("input_case, expected_case", zip(input_cases, expected_cases))
def test_unordered_output(input_case, expected_case):
    obj = solution.Solution()
    method_name = [x for x in dir(obj) if '__' not in x][0]
    output = recursive_sorted(eval(f'serialization(obj.{method_name})({input_case})'))
    expected = recursive_sorted(eval(expected_case))
    
    assert output == expected

@pytest.mark.class_design
def test_number_of_class_design_test_case_match():
    assert len(expected_cases) == len(input_cases) // 2

@pytest.mark.class_design
@pytest.mark.parametrize("input_case, expected_case", zip(pop_by_two(input_cases), expected_cases))
def test_design_class_output(input_case, expected_case):
    sigs, args = map(eval, input_case)

    class_name = sigs[0]
    init_args = args[0]

    obj = eval(f'solution.{class_name}(*init_args)')

    expected_case = eval(expected_case)

    for (method_name, method_args), expected in zip(zip(sigs[1:], args[1:]), expected_case[1:]):
        output = eval(f'obj.{method_name}(*method_args)')
        assert output == expected
