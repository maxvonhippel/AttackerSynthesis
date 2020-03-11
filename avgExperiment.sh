# for each experiment phi_n ...
for exp in 3 2 1; do
	# for each of (with recovery, without recovery) ...
	for b in True False; do
		# 10 times in a row ...
		for n in 1 2 3 4 5 6 7 8 9 10; do
			# Check how long it takes to solve this problem with n = 10.
			# ----------------------------------------------------------     
			# choose a name for this experiment                                                    
			name="experiment"$exp"_"$n; 
			# print the current experiment
			echo "\n\n~~~~~~~~~~~~~ EXPERIMENT :: "$name" ~~~~~~~~~~~~~~~\n\n";
			# do the current experiment and save output to a log
			(time python3 Gen3.py                                               
				--model=demo/TCP/TCP.pml                                        
				--phi="experiments/experiment"$exp".pml"                       
				--Q=demo/TCP/network.pml                                        
				--IO=demo/TCP/IO.txt                                            
				--max_attacks=10                                                
				--finite=$b                                                    
				--name=$name) &> "logs/"$name".txt";                          
		done;                                                                   
	done;                                                                       
done;