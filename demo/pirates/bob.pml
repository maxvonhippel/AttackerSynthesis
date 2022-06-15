active proctype bob() {
FISHING:
    do
    /* When Bob sees Alice, he offers to trade. */
    :: bob2alice ! trading;
    /* If Alice says she is a pirate then Bob 
     * surrenders immediately.  He has a peaceful soul.
     */
    :: alice2bob ? pirate -> bob2alice ! white; 
    od
end:
}