# Running the example
Run the following command: `python3 Korg.py --name='smallDemo3' --dir='./demo/smallDemo3/*'` in the top level directory.
Expect: Spin output in cli and output in `out/smallDemo3`
# P and Q 
P and Q are represented by the NFAs below. Phi is the safety propety `G w` or always `w = 1`. 

# P Diagram
```
      A!                                 B!
   +------+                           +------+
   |      |                           |      |
   |      v                           |      v
+--+------+--+                     +--+------+--+
|            |                     |            |
|            |          B!         |            |
|   W == 1   +-------------------->+   W == 0   |
|            |                     |            |
|            |                     |            |
+------------+                     +------------+
```

# Q Diagram
```
      A?
   +------+
   |      |
   |      v
+--+------+--+
|            |
|            |
|            |
|            |
|            |
+------------+
```

# Explanation
P || Q |= (always w == 1), where `||` is the compostion operator, because Q only accepts A's as inputs. However, the IO for Q is specified as accepting both A's and B's as inputs. This allows us to violate the property because the daisy that is generated from the IO may accept B's, which leads P into an unaccepting state. You may be asking yourself why the Daisy is allowed to generate connections with `B` given that the only connection that appears in the NFA is an `A`. This is because how we defined the IO alphabet of Q. If you look in `smallDemo3/IO.txt`, you'll see that both A and B are able to be inputs for the Daisy. Keeping Q's IO space larger is one way to allow more attacks agaisnt a given P. 