mtype = { white, royal, pirate, trading }

chan alice2bob = [0] of { mtype }
chan bob2alice = [0] of { mtype }

bool aliceRetired = false

active proctype alice() {
SCOPING:
    if
    /* When Alice is scoping for Bob, as soon as she
     * notices him, she immediately attacks, _regardless_
     * of what flags he waves.
     */
    :: bob2alice ? _ -> goto PIRATESTUFF;
    fi
PIRATESTUFF:
    /* When Alice attacks, she first hoists the pirate 
     * flag, to make it clear that she is, in fact, a big
     * scary pirate.
     */
    alice2bob ! pirate;
    if
    /* If Bob shows the white flag of surrender then Alice
     * takes his loot and then returns to the high sea to 
     * scope for another ship to plunder.
     */
    :: bob2alice ? white -> goto SCOPING;
    /* On the other hand, if Bob hoists the official colors of
     * Her Majesty's Royal Navy, then Alice will surrender,
     * because she knows that she is no match for the Royal
     * Navy in battle!
     */
    :: bob2alice ? royal -> goto end;
    fi
end:
    aliceRetired = true
}