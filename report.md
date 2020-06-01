# Automated Test Case Generation
## Target selection
There are several considerations regarding the target selection of the application. 
1. Firsly, is the name of the target function. By default, the application is going to look for a function called **test_me** but this can be overridden with a command-line argument. The application takes the following arguments. Note that the order of these is important:
    * target_path - Path of the target file
    * method - Search type to perform. One of {"avm", "avm_ips", "avm_gs", "avm_ls", "hill_climb"}
    * target_function - Name of function to target. If its a string, then it should be the exact name of the function. If its `1` then it would target all functions in the given file
    * iterations - How many iterations to perform search for (applies to both AVM and HillClimb)
    * retries - How many retries to perform in AVM (starting with fresh values)  
2. Secondly, we need to select target statements in the function that we are going to attempt to execute. To do this, I perform a BFS-traversal on all nodes in the body of the function, creating two-way links between parents and children. While doing so, I keep track of any node that can influence the control flow of the function, i.e. **If, While** or **For**. Then, an iteration through these control flow nodes is performed whereas we recursively record the parents of each node until we reach the root of the function. This constitutes the expected execution path for each node.
3. Finally, we also take note of the number of arguments that the target function expects.

## AST Instrumentation
There are two main things that have to be performed during the instrumentation of the abstract syntax tree. Namely, we 'attach' a reference to a variable that keeps track of which control flow statements are executed (tracing) and we also add code to calculate branch distance for each available predicate.
The AST instrumentation is performed by recursively yielding nodes that are relevant to the branching of the tree. These are **FunctionDef, If** and **While**. Here is what happens in the handlers for these nodes:
 - **FunctionDef** - We check if the function matches the target function we are looking for. If yes, we add an additional argument that will be used to store the execution trace (as a list) of the function
 - **If** and **While** - If the node is our target node, we add a branch distance calculation based on the expected predicate output, i.e. *True* or *False*. Otherwise, we add a branch distance calculation that is instead always expected to evaluate as *True*. This is because if the target node is nested within other statements, they have to evaluate to *True* in order for the function execution to reach the target. Then, the variable that (after the function is executed) would hold the branch distance is appended to the tracing variable with the following properties: node name, branch distance, predicate result and line number.  

Finally, there is one more layer of instrumentation that has to be done. As the target functions can take positional arguments, and there is no way to pass an arbitrary number of arguments without putting them in container (such as a list or a dictionary), we need a way to call the target function with a list of generated arguments. To do that, I create a wrapper function (`def wrap_function(tree, args)`) that essentially results in the following (provided that our test function is called **test_me**):
```python
1. def wrapper(trace):
2.     # Imports from the target file would be loaded here
3.     def test_me(a, b, c, trace):
4.         # Function def
5.         # ...
6.     test_me(x, y, z, trace)
```
The way this is achieved is relatively simple. Given the already instrumented target file, we put it inside at the beginning of the body element of a container function. Then, we simply iterate over the generated arguments to create a function call with these fixed arguments and the trace variable.

## Search Methods
### Techniques common to all methods
All search methods perform in the following rough outline
```python
1. for target_node, path_to_node in target_function.targets()
2.     for target_state in [True, False]
3.         instrumented_tree = Instrumentation(target_node, state) 
4.         result = search(instrumented_tree, target, path)
```
I implemented 4 search algorithms in total - Hill Climbing and AVM with Iterated Pattern Search, Geometric Search and Lattice Search, as per the pseudocode from [AVMf](http://eprints.whiterose.ac.uk/104204/1/c43.pdf):
![](avm.png)
Some common things across my implementation of all algorithms are:
* While searching through neighbouring values and trying to minimise the fitness function, I keep a lookup table of all explored inputs and their respective values. Then, every time I try an input (during that search iteration), instead of recomputing it, it is just fetched from the table.
* As some targets may be impossible to execute, a way has to be defined to stop the search at some point and return. The way this is done is by raising a custom exception. This exception operates under the idea that with the longer we are searching for a value that doesn't exist, the more the computation time for each attempt is going to increase. Therefore, if for any individual attempt, the time exceeds a given value (by default it is set to 10 seconds), a **TimeExceeded** exception is raised. Then, the handler of the exception would simply return that there is no response.
#### Fitness Function Calculation
As very large values in the predicates can lead to large **branch_distance** values, a math range error was not uncommon when calculating the fitness function. In order to solve that, I needed to decrease the value of the power that alpha is raised to. To do that, in those cases where **branch_distance** is too long, I take the logarithm of it. This results in the following fitness function (where AL is approach level and BD is branch distance):
$$
    fitness = \begin{cases}
        AL + (1 - 1.001^{-BD}), & \text{if } BD \leq 100 \\
        AL + (1 - 1.00001^{-\log{BD}}), & \text{if } BD > 100 \text{ or } 1.001^{-BD} \rightarrow \text{error} \\
        \end{cases}
$$
The reason behind choosing this particular second case of the function is that it grows relatively slowly with the increase of BD and it is also always larger than 1. This is important as we want to make sure that once we switch to the regular normalization, the valuer returned by that would always be smaller than the logarithm one. This is required as dropping to a low BD means we are quite close to the answer and we do not want to end up having a larger fitness function once this switch happens.
### Method specific implementations
#### Hill-Climbing
The implemented version of Hill Climbing is virtually the same as the generic implementation, with two differences:
* In an attempt to exit out of local minima $k$ we have a value that keeps track of how many iterations have been made without successfully reducing the value of the fitness function. Then, for the next iteration, instead of expanding to a neighbour $x+1$ and $x-1$ we instead look at $x+k$ and $x-k$. The value of $k$ is bounded by the number of iterations given by the user.  
* When extending to neighbour states, we consider all possible combinations. For example:
    ```python
    start_state = [x, y]
    neighbours = [[x - k, y - k], [x - k, y], [x - k, y + k],
                [x, y - k], [x, y], [x, y + k],
                [x + k, y - k], [x + k, y], [x + k, y + k]]
    ```
#### AVM
* For every successfully achieved target, I save the result in a lookup table like **(target, target_state) -> value**. Then, when iterating over the subsequent target, instead of starting of with random values, I take the value of the last successfully processed target. This way, especially with nested targets, we can directly start from a point that is some way down the branch, rather than trying to penetrate from the root.
* By default, AVM is initialised with a vector of values between -10 and 10. However, sometimes the neighbours of these inputs can lead to fitness values that are not changing. To circumvent this, if the method fails to find a solution, it would try again with the starting range multiplied by 10. This step is then repeated based on how many retry attempts the user has specified.   
Because this implementation is just looking at execution path and comparing it to the nesting of the target node, rather than using an actual dependency graph, there are cases where it would just get stuck without being able to minimize the fitness function. This means that search becomes essentially undirected and quickly is canceled (in case of AVM) because it doesn't converge. To that end, when executing retry attempts with AVM, the initialisation range of the initial values is increased. This added degree of randomness can lead the larger tolerances, specifically when it comes to nested problems, such as the one in *sample5*. Consider the following excerpt (some code ommitted for brevity).

    ```python
    1. def test_me(a, b, c):
    2.     d = 0
    3.     if a > b + c:
    4.         if b != c:
    5.             d += 1
    6.         else:
    7.             d += 2
    8.     if d > 0:
    9.         #...
    ```
    In this case, targetting the statement *if d > 0* becomes non-trivial when the search algorithm does not know that the values of **d** depend on the execution of the previous branch. While starting with the solution for one of the previous branches does alleviate this issue somewhat, it remains a problem where the values of **a,b,c** are relatively small. This is because by the time that **b** and **c** converge to each other, they are quite likely to become larger than **a** and negate the first **if** statement. However, when on the next retry of the **AVM** search, the initialisation range is increased, the tolerance for possible difference between **a** and **b+c** becomes larger and, by extension, there is a larger chance to find values that satisfy that condition.
* Similar to the **TimeExceeded** exception, AVM has a custom exception to stop the execution if a target has been found. The need for it arises because of the way that AVM is performed. Inputs are tested and the fitness values are compared with other inputs' but we do not always perform a check whether the condition has indeed been satisfied. Instead of adding a boolean flag and a lot of **If** statements to check its value, I decided to instead simply raise a **AnswerFound** exception if at the point of calculating the fitness of an input it is shown that the input meets the requirements of the target. The handler of this exception returns the found input.
* By default, if no specific AVM approach has been chosen, the program will attempt to run all of the aforementioned actions with each of AVM-IPS, AVM-GS, AVM-LS if an answer has not been found.

# Critical Evaluation and Limitations

While I believe that the approaches taken are justified in the constraints of this coursework, I do definitely realize that there are significant shortcomings with most, if not all of them.

- Instrumenting the tree separately for every target takes time and is something that can probably be avoided
- Saving previously the results searched inputs will always be a trade-off between space and time complexity. In some cases, for example, where the evaluation of a function takes a long time, it would be more beneficial to have a lookup table. On the other hand, if computation is fast but the state space is very large (maybe a very large number of arguments, or a lot of 'needle in the haystack' predicates to cover) then it could be more beneficial to recompute results for inputs every time, rather than run the risk of running out of memory
- Because of the randomness of initial state generation when retrying to perform AVM, correctness of the program can't be guaranteed. In fact, there were multiple occasions where during my manual testing, running the **covgen.py** file would sometimes yield perfect results yet fail to find most solutions in the next run. An example can be seen here (no changes were made to the code between the two runs). Also note that the image was taken before the final formatting of the output:  
![sample_4](sample4_merge.png)
- Another disadvantage to my approach is that in case where a condition is unsatisfiable, for example this line in sample3 **while z > 0:** would never evaluate to **False** as the previous statements covers the case **z == 0** and z can never reach a negative value. However, as on every failed attempt with AVM, I effectively increase the number of new iterations to complete, it can take a very long time to exhaust all options and conclude that no value satisfies the equation. 
- Some of these solutions seem like good ways to tackle the problems given in the sample set of functions to test again but it is also likely I have not considered a wide enough range of cases and I imagine there would be more pitfalls. 
- Due to time constraints and a desire to improve performance, code quality significantly degraded in the last couple of days. While it is not necessarily bad per se, it is not something I would consider of good enough quality to be used as a tool. However, this is easy, albeit slightly time-consuming to fix. 

# Conclusion
Overall, I found this assignment very challenging but also extremely stimulating and interesting to work on. I believe that I tried a lot of cool things and while some would likely be naive, it was still enjoyable to them out.
I do regret being so focused on trying to execute the body of a control flow node, forgetting that it is not always necessary, which cost me almost 2 weeks. I would have liked to be able to run a *benchmark* of sorts comparing the coverage and states checked of the different search algorithms, with and without the additions I made to them. Furthermore, while the current way of calculating approach level may not be perfect, I think it could be tuned to handle Control Dependency as well. 