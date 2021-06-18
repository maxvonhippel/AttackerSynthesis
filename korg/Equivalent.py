"""
file       : Equivalent.py
author     : Max von Hippel
authored   : 16 June 2021
description: Checks if two attack executions are "basically the same".
             Entirely heuristic in nature.
"""
import os
import subprocess
import sys

from pathlib import Path

from korg.Characterize import check


# attacker Recvs X over C
# attacker Sents X over C
class trailLine:
    def __init__(self, event, msg, channel):
        self.event   = event
        self.msg     = msg
        self.channel = channel
        assert(event in { "Recv", "Sent" })

    def toString(self):
        return "Attacker "                                   + \
            ("received" if self.event == "Recv" else "send")  + \
            " " + self.msg + " over " + self.channel

def line_in_trail_is_a_trailLine(line):
    if not "(attacker:" in line:
        return False
    if "Sent" in line and line.strip()[-1] == ")" and "(" in line:
        return True
    if "Recv" in line and line.strip()[-1] == ")" and "(" in line:
        return True
    return False

def line_in_trail_to_trailLine(theLine):
    event = "Sent" if "Sent" in theLine else \
            "Recv" if "Recv" in theLine else \
            None
    remainder = theLine.split(event)
    msg = remainder[1].split()[0]
    channel = remainder[1].split("(")[1].split(")")[0]
    return trailLine(event, msg, channel)

def parseTrailToEventsPair(theTrail):
    interestingLines = []
    for l in theTrail.split("\n"):
        if line_in_trail_is_a_trailLine(l):
            print(line_in_trail_to_trailLine(l).toString())
        elif "acceptance cycle" in l.lower():
            print("------------ acceptance cycle -----------")

def determineAttackStrategy(attack, model, phi):
    newfilename = str(abs(hash(attack + model + phi))) + ".pml"
    while True:
        tmp = Path(newfilename)
        if not (tmp.is_file() or tmp.is_dir()):
            break
        newfilename = str(abs(hash(newfilename))) + ".pml"
    with open(newfilename, "w") as fw:
        with open(model, "r") as fr:
            fw.write(fr.read())
        fw.write("")
        with open(attack, "r") as fr:
            fw.write(fr.read())
        fw.write("")
        with open(phi, "r") as fr:
            fw.write(fr.read())
        fw.write("")
    check(newfilename)

    args = "spin -t0 -s -r " + newfilename
    args = [a.strip() for a in args.split(" ")]
    args = [a for a in args if len(a) > 0]
    
    output = subprocess.check_output(args)
    if sys.stdout.encoding != None:
        output = output.decode(sys.stdout.encoding)
    output = str(output).strip().replace("\\n", "\n")\
                                .replace("\\t", "\t")
    parseTrailToEventsPair(output)


# spin -run -a model.pml
# spin -t0 -s -r tmp.pml

