# ==============================================================================
# File      : Characterize.py
# Author    : Max von Hippel and Cole Vick
# Authored  : 30 November 2019 - 13 March 2020
# Purpose   : Checks when models do or do not satisfy properties.  Also inter-
#             prets various outputs of Spin.
# How to run: This code is used by Korg.py, which is what you want to run.
# ==============================================================================

import subprocess
import sys
import os
from   glob            import glob
from   korg.Construct  import makeAttackTransferCheck
from   korg.printUtils import *

def nontrivialProps(P, Q, props):
    ret = set()
    for phi in props:
        # We assume this file does not yet exist
        tmpname = str(abs(hash(P + Q + phi))) + ".temporary.pml"
        if models(P, phi, Q, tmpname, True):
            ret.add(phi)
        else:
            print(makeRed(                 \
                phi                        \
                + " was not supported by " \
                + P + " || " + Q           \
                + " so cannot be attacked."))
        bigCleanUp(tmpname)
    return list(ret)

def testRemaining(attackPath, P, Q, props, comparing=False):
    if attackPath[-1] != "/":
        attackPath += "/"
    # Remove any trivial props
    props = nontrivialProps(P, Q, props)
    for attackerModel in glob(attackPath + "*.pml"):
        for phi in props:
            checkText = makeAttackTransferCheck(attackerModel, P, phi)
            newname = str(abs(int(hash(checkText)))) + ".pml"
            with open(newname, "w") as fw:
                fw.write(checkText)
            result = check(newname)
            if result == False:
                print(
                    ("" if comparing == False 
                        else 
                        makeBlue("[ comparing to " + P + " ]")) +
                    makeGreen(
                        str(attackerModel)                      + 
                        " is an attack with recovery against "  + 
                        str(phi)))
            os.remove(newname)


# Also adapted from RFCNLP code.
def bigCleanUp(cur_model_name):
    for file in glob("*.trail") + \
                glob("*tmp*")   + \
                glob("pan")     + \
                glob("*.pml")   + \
                glob("._n_i_p_s_"):
        if file != cur_model_name + ".pml" and \
           file != cur_model_name + "_CORRECT.pml":
            os.remove(file)

"""
Adapted from some logic in RFCNLP.
Deletes syntactically redundant attacks.
"""
def removeRedundant(attackPath):
    
    attacker_hashes = set()

    if attackPath[-1] != "/":
        attackPath += "/"
    
    for attacker in glob(attackPath + "*.pml"):
        attacker_body = ""
        l = 0
        with open(attacker, "r") as fr:
            for line in fr:
                if (l > 0):
                    attacker_body += "\n" + line
                l += 1
        attacker_hash = hash(attacker_body)
        
        if (attacker_hash in attacker_hashes):
            os.remove(attacker)
        
        else:
            attacker_hashes.add(attacker_hash)

'''
Given the path to a model containing one or more properties,
checks if that model violates one or more of those properties.

INPUT:
    modelFile - the string containing the path to the model file
OUTPUT:
    true iff modelFile runs successfully without acceptance cycles
    or violations else false
'''
def check(modelFile, maxDepth=60000):

    if maxDepth > 10000 * 20:
        print("maxDepth too large for any realistic run.  Edit the code if " \
            + "you actually really want to do this ... in Characterize.py.")
        return False

    args = "spin -run -a -DNOREDUCE -m" + str(maxDepth) + " -RS88 " + modelFile
    args = [a.strip() for a in args.split(" ")]
    args = [a for a in args if len(a) > 0]
    ret = None

    with open(os.devnull, 'w') as devnull:
        try:
            ret = subprocess.check_output(args, stderr=devnull)
            if sys.stdout.encoding != None:
                ret = ret.decode(sys.stdout.encoding).strip()
            else:
                ret = str(ret)
        except Exception as e:
            print("+++++++++ Problem in check() ++++++++++")
            print("---------------- ret ------------------")
            print(ret)
            print("--------------- exception -------------")
            print(e)
            print("----------------- model ---------------")
            try:
                with open(modelFile, "r") as fr:
                    print(fr.read())
            except Exception as e_inner:
                print(e_inner)
            print("+++++++++++++++++++++++++++++++++++++++")
            raise e

    if ret == None:
        return False

    if "depth too small" in ret:
        print("Search depth was too small at " \
             + str(maxDepth), \
             " doubling depth ...")
        return check(modelFile, maxDepth * 2)

    return not ("violated" in ret or "acceptance cycle" in ret)

def makeAllTrails(modelFile, numTrails=100):
    args = ""
    if numTrails <= 1:
        args = "spin -run -a -DNOREDUCE " + modelFile
    else:
        args = "spin -run -a -DNOREDUCE -e -c" + str(numTrails - 1) + " " + modelFile
    subprocess.run(args.split(" "))
    
'''
Given the paths to a model and a property, checks if that 
model makes true that property.

INPUT:
    model - the string containing the path to the model file
    phi   - the string containing the path to the ltl model file
    N     - the string containing the path to the N model file
    name  - where to save the intermediary model file to
OUTPUTS:
    true iff the model (model || phi || N) runs successfully without
    acceptance cycles or violations else false
'''
def models(model, phi, N, name, removeAfter=False):
    
    if None in { model, phi, N, name }:
        return False
    
    fmrLines = ""
    fNrLines = ""
    fprLines = ""
    
    with open(model, 'r') as fmr:
        fmrLines = fmr.read()

    with open(N, 'r') as fNr:
        fNrLines = fNr.read()

    with open(phi, 'r') as fpr:
        fprLines = fpr.read()

    with open(name, 'w') as fw:
        fw.write(fmrLines + "\n" + fNrLines + "\n" + fprLines)

    assert(os.path.isfile(name))

    ret = check(name)

    if removeAfter == True:
        os.remove(name)

    return ret

# Parses output of reading trail using Spin.
def parseTrail(trail_body, cycle_indicator=None):

    if cycle_indicator == None:
        cycle_indicator = "CYCLE"

    ret, i = [[], []], 0

    for line in trail_body.split("\n"):

        if "(daisy:" in line:

            # https://stackoverflow.com/a/29571669/1586231
            LL = line.rstrip("*")
            chan = LL[line.rfind("(")+1:-1]
            msg, evt = None, None
            
            if "Recv " in line:
            
                msg = LL[line.rfind("Recv ") + 5:].split()[0]
                evt = "?"
            
            if "Send" in line and msg == None and evt == None:
            
                msg = LL[line.rfind("Send ") + 5:].split()[0]
                evt = "!"

            if "Sent" in line and msg == None and evt == None:
            
                msg = LL[line.rfind("Sent ") + 5:].split()[0]
                evt = "!"
            
            if evt != None and msg != None:

                ret[i].append(chan + " " + evt + " " + msg)
        
        elif cycle_indicator in line:
            i = 1
    
    return ret

def parseAllTrails(cmds, with_recovery=False, debug=False, cycle_indicator=None):
    ret = []
    prov = []
    with open(os.devnull, 'w') as devnull:
        for cmd in cmds:
            output = subprocess.check_output(cmd, stderr=devnull)
            if sys.stdout.encoding != None:
                output = output.decode(sys.stdout.encoding)
            output = str(output).strip().replace("\\n", "\n")\
                                        .replace("\\t", "\t")
            parsed = parseTrail(output, cycle_indicator)
            ret.append(parsed)
            prov.append(cmd)
    return ret, prov

def attackType(A, E):
    # if A == 1 then E == 1
    # <=> not (A == 1 and E == 0)
    assert(not (A and not E))
    if A:
        return "A-attack"
    if E:
        return "E-attack"
    return "NOT AN ATTACK"

def characterizeAttacks(model, phi, with_recovery=True, name="run"):

    assert(os.path.isdir("out/" + name))

    nE, nA = 0, 0

    with open("out/" + name + "/log.txt", "w") as fw:

        if not (os.path.isdir("out/" + name + "/artifacts")):
            os.mkdir("out/" + name + "/artifacts")

        fw.write("model,A/E,with_recovery?\n")
        for attackModel in glob("out/" + name + "/attacker*.pml"):
            # is it a forall attack?
            attackName = os.path.basename(attackModel).replace(".pml", "")
            aName = "out/" + name + "/artifacts/" + attackName + "_A.pml"
            eName = "out/" + name + "/artifacts/" + attackName + "_E.pml"
            A = (models(model, "negated.pml", attackModel, aName) == True )
            E = (models(model, phi,           attackModel, eName) == False)
            if A:
                nA += 1
            elif E:
                nE += 1
            fw.write(",".join([ \
                attackModel, attackType(A, E), str(with_recovery)]) + "\n")
            
    return (nE, nA)