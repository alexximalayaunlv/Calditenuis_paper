import os

# Directory containing the 53 FASTA files
directory_path = './'  # Use the path to your directory

# Initialize a set to store genome names that should be removed
genomes_to_remove = set()

# List to store the filenames
file_list = []

# Iterate through the files to find genomes with dashes
for filename in os.listdir(directory_path):
    if filename.endswith('.faa'):
        file_list.append(filename)
        with open(os.path.join(directory_path, filename), 'r') as file:
            for line in file:
                if line.startswith('>'):
                    genome_name = line[1:].strip()
                elif line.strip() == '-' * len(line.strip()):
                    genomes_to_remove.add(genome_name)

# Iterate through the files and create new files without genomes to remove
for filename in file_list:
    output_file = os.path.splitext(filename)[0] + "_filtered.faa"
    with open(os.path.join(directory_path, filename), 'r') as input_file, open(os.path.join(directory_path, output_file), 'w') as output_file:
        write_genome = True
        for line in input_file:
            if line.startswith('>'):
                genome_name = line[1:].strip()
                write_genome = genome_name not in genomes_to_remove
            if write_genome:
                output_file.write(line)

print("Filtered files have been created with consistently present genomes.")
