active proctype Q() {
QZERO:
	if
	:: channel ! C; goto QONE;
	:: channel ? A; goto QONE;
	:: channel ? B; goto QZERO;
	fi
QONE:
	if 
	:: channel ! C; goto QONE;
	fi
}