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
P || Q |= (always w == 1) because Q only accepts A's as inputs. However, the IO for Q is specified as accepting both A's and B's as inputs. This allows us to violate the property because the daisy that is generated from the IO may accept B's, which leads P into an unaccepting state. 