# P and Q 
P and Q are represented by the NFAs below. The Phi  is `G F w`, which can be read as always eventually `w = 1`. Just from looking at the diagrams below it should become apparant that this Phi might not be made true by P and Q. Study the diagrams and then read the explanation below. 
# P Diagram
```
                                         A!
                                      +------+
                                      |      |
                                      |      v
+------------+                     +--+------+--+
|            |                     |            |
|            |        A!, B!       |            |
|   W == 1   +-------------------->+   W == 0   |
|            |                     |            |
|            |                     |            |
+------------+                     +------------+

```
# Q Diagram
```
+------------+                     +------------+
|            |         B?          |            |
|            +-------------------->+            |
|     Q0     |                     |     Q1     |
|            +<--------------------+            |
|            |         A?          |            |
+------------+                     +------------+

         
```

# Explanation
This Phi cannot be made false given P and the IO interface of Q. The point of this example is to show the limits of the tool. Since the original Phi cannot be made true given P and Q, finding an attacker will be a trivial exercise because attackers typically invalidate a property that was once valid. 