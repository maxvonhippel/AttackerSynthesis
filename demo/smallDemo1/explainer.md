# P and Q
P and Q, written as NFAs below, are the two models that make up the network. Here phi is 
`F G ~ w`, meaning that the atomic propostition w will eventually always equal zero. P and 
Q satisfy this property, we reject any P and Q that do not satisfy phi at the outset. Notice that Q does not contain any reference to w or any other atomic propositions. 

```                                            ___
                            _______C?_______      |
                    A!     |                |     |
-->( P_0 { w=1 } )------>( P_1 { w=0 } )<---|     |
       ^                   |                      |> P
       |___________________|                      |
                 B!                               |
                                               ___|

      
     _B?_
    |    |    A?, C!                           ___
-->( Q_0   )----------->( Q_1  )--|               |
       ^                          |               |
       |__________________________|               |> Q
                C!                                |
                                               ___|
             phi := G F ~ w
```

# The Goal

The goal of the tool at this point is to conform to the IO model of Q and violate phi without
changing P. The IO model of Q is currently: 

```
I: A,B
O: C
```

This means that Korg will generate a Daisy Automata that conforms to the given IO model. This Daisy Automata is now able to read any input that the original machine, Q, could. Once this Daisy has been constructed, Korg composes the Daisy with the original P and runs the composition in Spin to see if Spin can find a computation of the compostion that violates the original phi. If this is the case, we have found an attacker. We can build this attacker into a Promela model by reading the violating trace that Spin found and translating it into a NFA.  