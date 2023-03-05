## Dekker algorithm implementation

The Dekker algorithm is used to prevent race conditions occurring when two processes need to concurrently access the same "Critical Section" within an application. A critical section (CR) of a codebase is shared piece of data, and if two processes are both trying to concurrently perform operations on that data, there is a chance that a race condition will occur.

The dekker algorithm works by using: - A turn indicator, which points to either one of the processes at a time. - Two process flags, which are set to indicate that either of the processes wishes to access the critical section

The three fundamental rules which govern this algorithm are: - A process can never enter the CR when the other processes flag is set to True. - If both processes flags are set to True at once, then the process whos turn it is NOT will set their flag to False, and wait for the other process to finish. - When a process finishes, it sets its own flag to False, and switches the turn to the other processes.

The turn indicator is necessary to avoid 'deadlock' situations whereby both processes want to access the CR at the same time and end up in an infinite lock, both waiting for the other process to finish. By defaulting to the binary turn indicator in instances where both processes are trying to gain access concurrently, there will always be an objective 'truth' to which process's turn it is.

## Usage

`python dekker.py <OPTIONAL> --debug`

Running this command without debug will fire through 200 randomly-delayed and threaded 'data manipulations', collecting the ops that are running along the way and validating that if those ops are carried out in the order they were added to the list of ops, you will end up with the same data structure at the end.

Running this in debug mode will slow things down significantly, and log out the various states after each time the CR is accessed. It will also help to demonstrate the turn/flag system.

### NB

This was created in 30 minutes out of curiosity after watching a single youtube video and is probably not a very good implementation. For more and better info on Dekker's algorithm, check out [wikipedia](https://en.wikipedia.org/wiki/Dekker%27s_algorithm)
