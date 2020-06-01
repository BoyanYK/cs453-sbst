# Implementation
## Target selection
There are several considerations regarding the target selection of the application. 
1. Firsly, is the name of the target function. By default, the application is going to look for a function called `test_me` but this can be overridden with a command-line argument. The application only targets a single function in a given test file as the way I understood the requirements (and looking at relevant questions in Slack) is that the function can call both other functions in the same file or in other files/libraries. Therefore, with the possible existence of a function that is not to be tested in the target file, the tool is only looking for a single target function by its name. 
2. Secondly, we need to select target statements in the function that we are going to attempt to execute. To do this, I perform a BFS-traversal on all nodes in the body of the function, creating two-way links between parents and children. While doing so, I keep track of any node that can influence the control flow of the function, i.e. `If, While or For`. Then, an iteration through these control flow nodes is performed whereas we recursively record the parents of each node until we reach the root of the function. This constitutes the expected execution path for each node.
3. Finally, we also take note of the number of arguments that the target function expects.

## AST Instrumentation
There are two main things that have to be performed during the instrumentation of the abstract syntax tree. Namely, we 'attach' a reference to a variable that keeps track of which control flow statements are executed (tracing) and we also add code to calculate branch distance for each available predicate.
The AST instrumentation is performed by recursively yielding nodes that are relevant to the branching of the tree. These are `FunctionDef, If and While`. Here is what happens in the handlers for these nodes:
 - **FunctionDef** - We check if the function matches the target function we are looking for. If yes, we add an additional argument that will be used to store the execution trace (as a list) of the function
 - **If** and **While** - If the node is our target node, we add a branch distance calculation based on the expected predicate output, i.e. *True* or *False*. Otherwise, we add a branch distance calculation that is instead always expected to evaluate as *True*. This is because if the target node is nested within other statements, they have to evaluate to *True* in order for the function execution to reach the target. Then, the variable that (after the function is executed) would hold the branch distance is appended to the tracing variable with the following properties: node name, branch distance, predicate result and line number.

## Fitness Function Calculation

## Search Methods
All search methods perform in the following rough outline
```
1. For target_node, path_to_node in target_function.targets()
2.    For target_state in [True, False]
3.      instrumented_tree = Instrumentation(target_node, state) 
4.      result = search(instrumented_tree, target, path)
```

# Talking points

- Something I realised for both AVM and HillClimbing is that in order to make them perform better, I should have checked whether or not the current target contains in itself previous targets and if yes, to use the value found from them as a start
- While searching, I keep track of checked inputs so that I can fetch the value rather than recompute
- New Normalisation function for when branch distance is too large - handles impossible to otherwise compute powers
- Sample 5 is definitely challenging because of the nesting of various requirements. Not only that, it could require more than one iteration of the AVM method in order to converge to a solution as all the input variables are highly dependent on each other.
- AVM resets with larger ranges for the random start values

Because this implementation is just looking at execution path and comparing it to the nesting of the target node, rather than using an actual dependency graph, there are cases where it would just get stuck without being able to minimize the fitness function. This means that search becomes essentially undirected and quickly is canceled (in case of AVM) because it doesn't converge. To that end, when executing retry attempts with AVM, the initialisation range of the initial values is increased. This added degree of randomness can lead the larger tolerances, specifically when it comes to nested problems, such as the one in sample5. Consider the following excerpt (some code ommitted for brevity)

```python
def test_me(a, b, c):
    d = 0
    if a > b + c:
        if b != c:
            d += 1
        else:
            d += 2
    if d > 0:
        #...
```

In this case, targetting the statement `if d > 0` becomes non-trivial when the search algorithm does not know that the values of `d` depend on the execution of the previous branch. While starting with the solution for one of the previous branches does alleviate this issue somewhat, it remains a problem where the values of `a,b,c` are relatively small. This is because by the time that `b` and `c` converge to each other, they are quite likely to become larger than `a` and negate the first `if` statement. However, when on the next retry of the **AVM** search, the initialisation range is increased, the tolerance for possible difference between `a` and `b+c` becomes larger and, by extension, there is a larger chance to find values that satisfy that condition.

# Critical Evaluation and Limitations

While I believe that the approaches taken are justified in the constraints of this coursework, I do definitely realize that there are significant shortcomings with most, if not all of them.

- Instrumenting the tree separately for every target takes time and is something that can probably be avoided
- Saving previously the results searched inputs will always be a trade-off between space and time complexity. In some cases, for example, where the evaluation of a function takes a long time, it would be more beneficial to have a lookup table. On the other hand, if computation is fast but the state space is very large (maybe a very large number of arguments, or a lot of 'needle in the haystack' predicates to cover) then it could be more beneficial to recompute results for inputs every time, rather than run the risk of running out of memory
- Because of the randomness of initial state generation when retrying to perform AVM, correctness of the program can't be guaranteed. In fact, there were multiple occasions where during my manual testing, running the `covgen.py` file would sometimes yield perfect results yet fail to find most solutions in the next run. An example can be seen here (no changes were made to the code between the two runs). Also note that the image was taken before the final formatting of the output:  
![sample_4](sample4_merge.png)
- Another disadvantage to my approach is that in case where a condition is unsatisfiable, for example this line in sample3 `while z > 0:` would never evaluate to `False` as the previous statements covers the case `z == 0` and z can never reach a negative value. However, as on every failed attempt with AVM, I effectively increase the number of new iterations to complete, it can take a very long time to exhaust all options and conclude that no value satisfies the equation. 
- Some of these solutions seem like good ways to tackle the problems given in the sample set of functions to test again but it is also likely I have not considered a wide enough range of cases and I imagine there would be more pitfalls. 
