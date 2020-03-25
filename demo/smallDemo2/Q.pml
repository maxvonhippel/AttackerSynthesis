active proctype Q() {
QZERO:
	if
	:: channel ? B; goto QONE;
	fi
QONE:
	if 
	:: channel ? A; goto QONE;
	fi
}