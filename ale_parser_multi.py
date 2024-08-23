# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 21:00:00 2024
Python 3.8.5
@author: Dengxun Lai (ref: ale_parser_0.3.pl from Luo et al., 2024)
Purpose: 
"""

import os
import sys

# Check if the command line argument is provided
if len(sys.argv) < 2:
    raise Exception("Usage: python ale_parser_multi.py <ALE_output_directory_path>")

# Open the directory for reading
ale_dir = sys.argv[1]
if not os.path.isdir(ale_dir):
    sys.exit(f"Can't open directory {ale_dir}")

# Process each file in the directory
# Create the output directory and extract unique ID (e.g., gene name) from the filename (used the first character divied by "_", change [0] when needed)
for file in os.listdir(ale_dir):
    if file.endswith(".ale.uml_rec"):
        UID = file.split('_')[0]
        
        # Create and open files for writing	
        with open(f"{ale_dir}/{UID}_species.tre", 'w') as species_tree_file, \
            open(f"{ale_dir}/{UID}_gene_family.events.count.txt", 'w') as events_count_file, \
            open(f"{ale_dir}/{UID}_gene_family.events.rate.txt", 'w') as event_rate_file, \
            open(f"{ale_dir}/{UID}_node.events.count.txt", 'w') as node_events_sta_file, \
            open(f"{ale_dir}/{UID}_node.hgt.txt", 'w') as node_hgt_file, \
            open(f"{ale_dir}/{UID}_node.dup.txt", 'w') as node_dup_file, \
            open(f"{ale_dir}/{UID}_node.loss.txt", 'w') as node_loss_file, \
            open(f"{ale_dir}/{UID}_node.ori.txt", 'w') as node_ori_file:

            # Write headers to the files
            events_count_file.write("Cluster\tDuplications\tTransfers\tLosses\tOriginations\n")
            event_rate_file.write("Cluster\tDuplications\tTransfers\tLosses\n")

            # Initialize variables
            species_tree = ""
            duplication = {}
            loss = {}
            transfer = {}
            origination = {}
            nodes = {}
            duplication_node = {}
            loss_node = {}
            origination_node = {}
            transfer_node = {}

            # Process the current file and a relaxed minimum frequency threshold of 0.3 was chose (modify as needed)
            with open(f"{ale_dir}/{file}", 'r') as infile:
                for line in infile:
                    if line.startswith("S:"):
                        species_tree = line.split()[1]
                    elif line.startswith("rate of	 Duplications"):
                        next_line = next(infile)
                        fields = next_line.split()
                        event_rate_file.write(f"{UID}\t{fields[1]}\t{fields[2]}\t{fields[3]}\n")
                    elif line.startswith("# of	 Duplications	Transfers	Losses	Originations"):
                        next_line = next(infile)
                        fields = next_line.split()
                        events_count_file.write(f"{UID}\t{fields[1]}\t{fields[2]}\t{fields[3]}\t{fields[4]}\n")
                    elif line.startswith("S_terminal") or line.startswith("S_internal"):
                        fields = line.strip().split()
                        node_name = fields[1].split('(')[0]
                        nodes[node_name] = True
                        if float(fields[2]) > 0.30:
                            duplication_node.setdefault(node_name, []).append(UID)
                            duplication[node_name] = duplication.get(node_name, 0) + float(fields[2])
                        if float(fields[3]) > 0.30:
                            transfer_node.setdefault(node_name, []).append(UID)
                            transfer[node_name] = transfer.get(node_name, 0) + float(fields[3])
                        if float(fields[4]) > 0.30:
                            loss_node.setdefault(node_name, []).append(UID)
                            loss[node_name] = loss.get(node_name, 0) + float(fields[4])
                        if float(fields[5]) > 0.30:
                            origination_node.setdefault(node_name, []).append(UID)
                            origination[node_name] = origination.get(node_name, 0) + float(fields[5])

            species_tree_file.write(species_tree)

            node_events_sta_file.write("Node\tDuplication\tTransfer\tLoss\tOrigination\n")
            for key in sorted(nodes.keys()):
                node_events_sta_file.write(f"{key}")
                if key in duplication:
                    node_events_sta_file.write(f"\t{duplication[key]}")
                    dups = ",".join(duplication_node[key])
                    node_dup_file.write(f"{key}\t{dups}\n")
                else:
                    node_events_sta_file.write("\t0")
                if key in transfer:
                    node_events_sta_file.write(f"\t{transfer[key]}")
                    hgts = ",".join(transfer_node[key])
                    node_hgt_file.write(f"{key}\t{hgts}\n")
                else:
                    node_events_sta_file.write("\t0")
                if key in loss:
                    node_events_sta_file.write(f"\t{loss[key]}")
                    losses = ",".join(loss_node[key])
                    node_loss_file.write(f"{key}\t{losses}\n")
                else:
                    node_events_sta_file.write("\t0")
                if key in origination:
                    node_events_sta_file.write(f"\t{origination[key]}")
                    specs = ",".join(origination_node[key])
                    node_spec_file.write(f"{key}\t{specs}\n")
                else:
                    node_events_sta_file.write("\t0")
                node_events_sta_file.write("\n")
