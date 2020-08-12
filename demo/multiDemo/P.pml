/* file       : P.pml
 * author     : Max von Hippel
 * authored   : 10 August 2020
 * description: tool for developing / testing the distributed
 *              attacker synthesis problem solution.
 */

mtype = { a, b, c, d };

bool bad = false;

chan q02p = [0] of { mtype };
chan q12p = [0] of { mtype };
chan q22p = [0] of { mtype };

chan p2q0 = [0] of { mtype };
chan p2q1 = [0] of { mtype };
chan p2q2 = [0] of { mtype };


active proctype p() {
	q02p ? a; /* get "a" from q0   */
	p2q0 ! a; /* respond "a" to q0 */ 
	q12p ? b; /* get "b" from q1   */
	p2q1 ! b; /* respond "b" to q1 */
	q22p ? c; /* get "c" from q2   */
	p2q2 ! c; /* respond "c" to q2 */
	bad = true;
}