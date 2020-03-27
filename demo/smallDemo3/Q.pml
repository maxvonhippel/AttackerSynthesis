active proctype Q() {
QZERO:
	if
	:: channel ? A; goto QZERO;
	fi
}