[`↞` Back to **README.md**](../README.md), [`↞` Back to **Korg.md**](Korg.md)

# Troubleshooting

## Caveats

Here are some important caveats to be aware of.

1. Korg is not good at handling comments in your LTL property `phi`.  Please just ommit any comments from the property!

2. Korg will misbehave if you declare a variable `bit b` anywhere in any of your models.  So, please don't do that.

3. Korg prints all the output from Spin every time it runs Spin.  I have not figured out how to suppress this.  So, please just ignore all that cruft in the tool's output.

3. Korg expects you to be honest when you craft your interface (`IO.txt`) file.  Do not lie about the interface of `Q`!

## Return Values

You can infer a lot from the value returned by Korg (the [exit status](https://en.wikipedia.org/wiki/Exit_status)).

| Exit Status | Meaning                                                                                          |
|-------------|:-------------------------------------------------------------------------------------------------|
| 0           | Success! :money_mouth_face:                                                                      |
| 1           | Invalid `max_attacks` argument :thumbsdown:                                                      |
| 2           | Couldn't negate `phi`, probablty because the file does not exist or is not accessible :eyes:     |
| 3           | `M || Q |/= phi`, so the threat model is *invalid*! :policewoman:                                |
| 4           | Invalid `IO.txt`, probably wrong file path or permissions or something. :ear:                    |
| 5           | Empty `IO.txt`.  In this case there is no possible attacker. :thinking:                          |
| 6           | No solution!  In other words, the daisy does not violate `phi`.  :mag:                           |
| -1          | No attackers found, even though the daisy worked.  (This really should never happen.) :confused: |