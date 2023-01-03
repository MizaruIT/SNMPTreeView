from os import listdir
from os.path import isfile, join
import argparse
import mibdump as mibdump


def parserIntoJson(input_path, output_directory):
    onlyfiles = [join(input_path, f) for f in listdir(input_path) if isfile(join(input_path, f))]
    list_files_failed = []
    for idx, mib_file in enumerate(onlyfiles):
        print(f"File n° {idx}/{len(onlyfiles)} = {mib_file}")
        try:
            mibdump.parser(mib_file, input_path, output_directory)
        except:
            print(f"The parsing of the file: {mib_file} has failed.")
            list_files_failed.append(mib_file)
    print(f"The list of the files with failed parsing: {list_files_failed}")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser of MIBs files into JSON files')
    # parser.add_argument('-m', '--mib', type=str, help='Path to your directory where you have your MIBs files (ex: /home/Downloads/asn1)', required=True)
    parser.add_argument('-p', '--path', type=str, help='Path to the directory with the MIBs files to parse from ASN.1 format to JSON format (ex: /home/Downloads/asn1)', required=True)
    parser.add_argument('-d', '--dir', type=str, help='Path to the directory to output the results of the parsing (ex: /home/Downloads/json)', required=True)
    args = parser.parse_args()
    parserIntoJson(args.path, args.dir)
