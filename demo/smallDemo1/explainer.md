# Running the example
Run the following command: `python3 Korg.py --name='smallDemo1' --dir='./demo/smallDemo1/*'` in the top level directory.
Expect: Spin output in cli and output in `out/smallDemo1`
# P and Q
P and Q, written as NFAs below, are the two models that make up the network. Here Phi is the liveness property `F G ~ w`, meaning that the atomic propostition w will eventually always equal zero. P and Q satisfy this property, we reject any P and Q that do not satisfy phi at the outset. Notice that Q does not contain any reference to w or any other atomic propositions. 

# P Diagram
```                                           
                                              C?
                                           +------+
                                           |      |
                                           |      v
     +------------+                     +--+------+--+
     |            |         A!          |            |
     |     S0     +-------------------->+     S1     |
---->+   w = 1    |                     |    w = 0   |
     |            +<--------------------+            |
     |            |        B!           |            |
     +------------+                     +------------+
                
```

# Q Diagram
```
           B?
        +------>
        |      |
        |      v
     +--+------+--+                     +------------+
     |            |       A?, C!        |            |
     |            +-------------------->+            |
---->+     Q0     |                     |     Q1     |
     |            +<--------------------+            |
     |            |         C!          |            |
     +------------+                     +------------+

```

# Explanation

The goal of the tool at this point is to conform to the IO model of Q and violate phi without
changing P. The IO model of Q is currently: 

```
I: A,B
O: C
```

This means that Korg will generate a Daisy Automata that conforms to the given IO model. This Daisy Automata is now able to read any input that the original machine, Q, could. Once this Daisy has been constructed, Korg composes the Daisy with the original P and runs the composition in Spin to see if Spin can find a computation of the compostion that violates the original phi. If this is the case, we have found an attacker. We can build this attacker into a Promela model by reading the violating trace that Spin found and translating it into a NFA.  