# Multithreaded Common Crawl Iterator

This Python script will iterate over web archive files including wet.paths, wat.paths or warc.paths file from Common Crawl.

This is meant as a starting point and example. The output is pretty janky, you will probably want to silence the wget command and send the output to a file or database on a production situation, but again, this is a demonstration so don't use this in production without some changes.

## How it works.

The iterator.py script iterates over a warc, wet, or wat paths file and then iterates over the contents of the download (double loop).

The script reads each line from the warc.paths file, and appends the correct prefix.

Each file is unzipped.

The resulting file is then looped over and the url of each record in the file is printed.

You can use this as a starting point to iterate through an entire Common Crawl and extract the data. Using a processor with a high core count it is possible to process a lot of data fairly quickly. 

## Usage:

Clone the archive and cd to the main folder.

Change the `file_path` variable to match the path on your local computer of the warc.paths file.

Change the `download_dir` variable to match the path on your local computer where you want to store the warc files. This can be a temporary folder.

Run the iterator: `python3 ./iterator.py`

# commoncrawl_iterator
