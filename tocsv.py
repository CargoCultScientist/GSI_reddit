# This Python script is designed to convert a .zst file (Zstandard compressed file) to a .csv (comma-separated values) file. 
# It is specifically tailored for handling large datasets that are commonly found in data analysis tasks. 
# The script takes three command-line arguments: the input file (a .zst file), the output file (a .csv file), and a list of fields to be extracted from the JSON objects in the .zst file.
# The script uses the logging module to log information and errors, which is helpful for monitoring the progress and diagnosing issues during processing.
# Errors like JSON decoding issues or missing keys in the JSON objects are logged, and processing continues.
# This script is particularly useful in data analysis scenarios where large datasets are compressed for storage efficiency and need to be converted into a more accessible format like CSV for analysis.

# call this like:
# python to_csv.py wallstreetbets_submissions.zst wallstreetbets_submissions.csv author,selftext,title

import zstandard # zstandard library to decompress the .zst file. It reads the compressed data, decompresses it, and processes it in chunks.
import os
import json # Each line in the decompressed data is expected to be a JSON object. The script extracts specified fields from these JSON objects.
import sys
import csv
from datetime import datetime
import logging.handlers


log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

# This function reads chunks of the compressed file, attempting to decode them into a string.
def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)

# Opens the .zst file and processes it in chunks. Each chunk is split into lines, and each line (presumably a JSON object) is yielded for processing.
def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)
			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line, file_handle.tell()

			buffer = lines[-1]
		reader.close()

# main block: 
# Handles command-line arguments, sets up the CSV writer, and iterates over lines from read_lines_zst. 
# For each line, it attempts to parse it as JSON, extract the desired fields, and write them to the CSV file. 
# It logs progress and handles errors like JSON decode errors or missing keys.

if __name__ == "__main__":
	input_file_path = sys.argv[1]
	output_file_path = sys.argv[2]
	fields = sys.argv[3].split(",")

	file_size = os.stat(input_file_path).st_size
	file_lines = 0
	file_bytes_processed = 0
	line = None
	created = None
	bad_lines = 0
	output_file = open(output_file_path, "w", encoding='utf-8', newline="")
	writer = csv.writer(output_file)
	writer.writerow(fields)
	try:
		for line, file_bytes_processed in read_lines_zst(input_file_path):
			try:
				obj = json.loads(line)
				output_obj = []
				for field in fields:
					output_obj.append(str(obj[field]).encode("utf-8", errors='replace').decode())
				writer.writerow(output_obj)

				created = datetime.utcfromtimestamp(int(obj['created_utc']))
			except json.JSONDecodeError as err:
				bad_lines += 1
			file_lines += 1
			if file_lines % 100000 == 0:
				log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {file_lines:,} : {bad_lines:,} : {(file_bytes_processed / file_size) * 100:.0f}%")
	except KeyError as err:
		log.info(f"Object has no key: {err}")
		log.info(line)
	except Exception as err:
		log.info(err)
		log.info(line)

	output_file.close()
	log.info(f"Complete : {file_lines:,} : {bad_lines:,}")
