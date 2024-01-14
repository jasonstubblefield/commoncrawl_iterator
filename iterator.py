import os
import subprocess
import gzip
import threading
from queue import Queue
from warcio.archiveiterator import ArchiveIterator

# Function to process each file
def process_file(queue):
    while True:
        relative_path = queue.get()
        if relative_path is None:
            break

        full_url = f"https://data.commoncrawl.org/{relative_path}"
        gz_filename = os.path.join(download_dir, os.path.basename(relative_path))
        warc_filename = gz_filename.rstrip('.gz')

        # Download the file
        subprocess.run(['wget', '-O', gz_filename, full_url])
        print(f"Downloaded {full_url} to {gz_filename}")

        # Unzipping the file
        with gzip.open(gz_filename, 'rb') as gz_file:
            with open(warc_filename, 'wb') as warc_file:
                warc_file.write(gz_file.read())
        print(f"Unzipped {gz_filename} to {warc_filename}")

        # Iterating over the WARC file
        with open(warc_filename, 'rb') as warc_file:
            for record in ArchiveIterator(warc_file):
                print(record.rec_headers.get_header('WARC-Target-URI'))

        # Remove files
        os.remove(warc_filename)
        os.remove(gz_filename)
        print(f"Deleted files {warc_filename} and {gz_filename}")

        queue.task_done()

# Number of threads
num_threads = 4

# Queue to hold the paths
queue = Queue()

# File containing the paths
file_path = '/users/jasonstubblefield/downloads/wet_copy.paths'

# Directory to save the downloaded files
download_dir = os.path.expanduser('/users/jasonstubblefield/downloads/commoncrawl')

# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Start the threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=process_file, args=(queue,))
    thread.start()
    threads.append(thread)

# Enqueue paths
with open(file_path, 'r') as file:
    for line in file:
        queue.put(line.strip())

# Block until all tasks are done
queue.join()

# Stop the threads
for _ in range(num_threads):
    queue.put(None)
for thread in threads:
    thread.join()

print("Process completed.")
