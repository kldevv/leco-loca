# Leco Loca ✨ - Running Your LeetCode Challenges Locally

## 💡 Description

An easy way to setup your Python local testing enivronment for LeetCode Weekly Contests as well as daily practices.

This is a command-line tool to help you keep track of the test cases and debug locally; You can also pre-generate your favorite code snippet by modifying and copying the `template` directory in no time.

It currently supports 3 most frequently encountered LeetCode pre-defined serializable classes: `TreeNode`, `ListNode`, and `Node`.

## 💡 Installation

It requires `pytest` to run the test sets, and some commonly used data structure libraries for Python. If you haven't already installed them, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

There are 2 shell scripts to be made executable `copy_contents.sh` and `pytest_and_clean.sh`:

```bash
chomd +x copy_contents.sh
chomd +x pytest_and_clean.sh
```

## 💡 Usage

Create a standalone directory for each LeetCode problem with the following commnad:

```bash
./copy_contents.sh template $DIR_NAME
```

Replace `$DIR_NAME` with the directory name you want to make; this will copy everything in the `template` directory to `$DIR_NAME` directory. Alternatively, you can do this manually.

Modify `template/solution.py` to fit your needs. Make sure not to change the structure of the folder, and to include `test_solution.py` , `pytest.ini`, `expected.txt`, and `input.txt` especially, unless you're absolutely sure what you're doing.

---

Copy and paste the input and expected output from your LeetCode question straight to `$DIR_NAME/input.txt` and `$DIR_NAME/output.txt` respectively. See `examples/*/input.txt` and `examples/*/output.txt` for real-world examples.

Yes, it is still done manually. I'll think of a better way to handle this.

---

Write your solution to `*/solution.py`, just as you would do in the LeetCode web-based editor. There is already a code snippet in the template, and you change it to whatever you like. Do not change the file name though.

---

Now the fun parts. There are 3 most commonly used rules to parse your submission (according to my experience). They are either ordered, unordered, or the problem itself is about designing a new class.

### 1. Ordered Output

The most commonly encountered type of questions. Simply run:

```bash
./pytest_and_clean.sh $DIR_NAME
```

It will launch the pytest, load your testing sets, and clean up the mess once it's done.

> _See `examples/2643` for ordered example. 🌱_

### 2. Unordered Ouput

Sometimes, the order of the output is irrelevant. It ususally goes as _"...If there are multiple answers, return any of them."_.

```bash
./pytest_and_clean.sh $DIR_NAME -u
```

By supplying the `-u` flag, your output will be recursivley sorted before asserting.

> _See `examples/2610` for unordered output example. 🌱_

### 3. Class Design

Less frequently, the problem is to design a class that does something. In this case, your solution class is not named `Solution` but something else.

```bash
./pytest_and_clean.sh $DIR_NAME -c
```

By supplying the `-c` flag, your input/output cases are treated differently. Specifically, each test case consist of 2 lines of input (methods and arguments) and 1 line of output.

> _See `examples/2642` for class design example. 🌱_

## 💡 Serialization

Problems involving tree and linked list nodes are everywhere in the LeetCode land. You seldom need to worry about it, unless your solution function takes `TreeNode`, `ListNode`, and `Node` as input, even so, in most cases, they're already taken care of; If it's `TreeNode` and the keyword argument is `root`, or `ListNode` and keyword argument is `head`, you're fine.

> _See `examples/2641` for TreeNode example. 🌱_

> _See `examples/725` for ListNode example. 🌱_

However, if it's `Node` and the keyword is `root`, go to `*/test_solution.py` and change the boolean literal of `TreeNode_INVOLVED` to `False` and `Node_INVOLVED` to `True`; they are located at the top of the test file.

> _See `examples/590` for Node example. 🌱_

In the unlikely event of the keyword is neither `root` or `head`, go to `*/test_solution.py` and change the string literals of `TreeNode_PARAMS`, `ListNode_PARAMS` and `Node_PARAMS` to match the keywords of your solution function signature.

In summary, the following pairs of variables combined give you the freedom to leverage the serialization of these classes:

(`TreeNode_INVOLVED`, `TreeNode_PARAMS`)
(`ListNode_INVOLVED`, `ListNode_PARAMS`)
(`Node_INVOLVED`, `Node_PARAMS`)

## 💡 Comments

-   `leco-loca` does not check for TLE.
-   I used ChatGPT to generate minimum amount of boilerplate code snippet.
-   See my LeetCode repo [leetcode-v3](https://github.com/kylab9527/leetcode-v3) to see the live usage of `leco-loca`
-   `eval` is used in the `test_solution.py` and the input sanitation is not conducted, please use `leco-loca` only for the purpose of solving LeetCode problem, and be aware of injection attacks.
