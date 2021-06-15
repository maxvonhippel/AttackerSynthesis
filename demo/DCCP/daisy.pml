active proctype daisy() {
	do
	:: AtoN ? DCCP_REQUEST; 
	:: AtoN ? DCCP_RESPONSE; 
	:: AtoN ? DCCP_DATA; 
	:: AtoN ? DCCP_ACK; 
	:: AtoN ? DCCP_DATAACK; 
	:: AtoN ? DCCP_CLOSEREQ; 
	:: AtoN ? DCCP_CLOSE; 
	:: AtoN ? DCCP_RESET;
	:: AtoN ? DCCP_SYNC;
	:: AtoN ? DCCP_SYNCACK;
	//
	:: BtoN ? DCCP_REQUEST; 
	:: BtoN ? DCCP_RESPONSE; 
	:: BtoN ? DCCP_DATA; 
	:: BtoN ? DCCP_ACK; 
	:: BtoN ? DCCP_DATAACK; 
	:: BtoN ? DCCP_CLOSEREQ; 
	:: BtoN ? DCCP_CLOSE; 
	:: BtoN ? DCCP_RESET;
	:: BtoN ? DCCP_SYNC;
	:: BtoN ? DCCP_SYNCACK;
	//
	:: NtoB ! DCCP_REQUEST; 
	:: NtoB ! DCCP_RESPONSE; 
	:: NtoB ! DCCP_DATA; 
	:: NtoB ! DCCP_ACK; 
	:: NtoB ! DCCP_DATAACK; 
	:: NtoB ! DCCP_CLOSEREQ; 
	:: NtoB ! DCCP_CLOSE; 
	:: NtoB ! DCCP_RESET;
	:: NtoB ! DCCP_SYNC;
	:: NtoB ! DCCP_SYNCACK;
	//
	:: NtoA ! DCCP_REQUEST; 
	:: NtoA ! DCCP_RESPONSE; 
	:: NtoA ! DCCP_DATA; 
	:: NtoA ! DCCP_ACK; 
	:: NtoA ! DCCP_DATAACK; 
	:: NtoA ! DCCP_CLOSEREQ; 
	:: NtoA ! DCCP_CLOSE; 
	:: NtoA ! DCCP_RESET;
	:: NtoA ! DCCP_SYNC;
	:: NtoA ! DCCP_SYNCACK;
	od
}