import os

def count_files(directory):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

directories = [
    "../public/jobs/pdfs",
    "../public/jobs/txts",
    "../public/jobs/JSONs_facts",
    "../public/jobs/JSONs_fits",
]

for directory in directories:
    num_files = count_files(directory)
    print(f"There are {num_files} files in {directory}")
