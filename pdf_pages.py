from PyPDF2 import PdfFileMerger,PdfFileReader, PdfFileWriter
import os
import logging
import argparse

def setup():
    '''
    Handles logging configuration, user input, and passed arguments to the propper function for PDF edits.
    '''

    #Set output logging level to display output of successful files.
    logging.getLogger().setLevel(logging.INFO)

    #Handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The file(s) to have operations performed on.")
    parser.add_argument("output", help="Path for desired output file(s).")
    parser.add_argument("-i", "--individual", help="Specify which files to merge in a sorted, comma seperated list.", action="store_true")
    parser.add_argument("-d", "--directory", help="Merge all PDFs in a single directory sorted alphabetically.", action="store_true")
    #parser.add_argument("-s", "--split", help="Specify an input file to split along with output file names and a page to split.", action="store_true")
    #parser.add_argument("-p", "--page", help="Integer page number to split the PDF at.", type=int)
    args = parser.parse_args()

    #Determine mode based on input arguments.
    #if not args.individual and not args.directory and not args.split:
    if not args.individual and not args.directory:
        logging.error('You must choose at least one mode.')
        SystemExit
    
    if args.individual:
        merge_individual(args.input, args.output)

    if args.directory:
        directory_merge(args.input, args.output)

    # if args.split:
    #     if args.page:
    #         logging.info("The PDF named \'" + args.input + "\' will be split at page " + str(args.page) + ".")
    #         split(args.input, args.output, args.page)
    #     else:
    #         logging.error("A page number (-p) is required to use the split function. Quitting.")
    #         SystemExit

def merge_individual(indv_input, indv_output):
    '''
    Takes in a comma seperated list of input files as well as an output file location to save the merged PDF to.
    '''

    merger = PdfFileMerger()

    #Create a list of input files
    if "," in indv_input:
        pdf_files = indv_input.split(',')
    else:
        logging.error("Multiple files seperated by a comma are required. Quitting.")
        SystemExit

    for input_file in pdf_files:
        merger.append(input_file)

    pdf_merge_output(merger, indv_output)

def directory_merge(dir_merge_input, dir_merge_output):
    '''
    Takes in a directory and merges any pdf files found inside alphabetically. Saves to the output file argument.
    '''
    
    merger = PdfFileMerger()

    sorted_files = []
    for item in os.listdir(dir_merge_input):
        if item.endswith('pdf'):
            sorted_files.append(item)

    sorted_files.sort()
    
    if len(sorted_files) > 1:
        for pdf in sorted_files:
            merger.append(pdf)
    else:
        logging.error("There were not enough files in the input directory to merge. Quitting.")
        SystemExit
    
    pdf_merge_output(merger, dir_merge_output)
    return

#TODO: Make a split function.
# def split(pdf_split_input, pdf_split_output, page_split):
#     '''
#     Takes in a single PDF and splits it into two at the specifed page numberPDFs saved to the location in the output argument with -1 and -2.
#     '''
#     pdf_to_split = open(pdf_split_input, 'rb')
#     pdf_reader = PdfFileReader(pdf_to_split)
#     pdf_writer = PdfFileWriter()

#     for i in range(0, page_split - 2):
#         pdf_writer.addPage(pdf_reader.getPage(i))

#     part_one = pdf_split_output.replace('.pdf', '-1.pdf')
#     pdf_write_output(pdf_writer, part_one)
    
#     for i in range(page_split - 1, pdf_reader.getNumPages() -1):
#         pdf_writer.addPage(pdf_reader.getPage(i))

#     part_two = pdf_split_output.replace('.pdf', '-2.pdf')
#     pdf_write_output(pdf_writer, part_two)
#     return

def pdf_merge_output(merger, output_file):
    '''
    Saves the processed PDF merge operations to the specified output file given the merger object.
    '''
    #Checks to make sure the output file is not overwritten
    if not os.path.exists(output_file):
        merger.write(output_file)
        merger.close()
        logging.info('The merged file \'' + output_file + '\' was created successfully.')
        return
    else:
        override = input('The output file \'' + output_file + '\' already exists. Overwrite this file? (Y/N): ')
        if override == 'Y' or override == 'y':
            merger.write(output_file)
            merger.close()
            logging.info('The merged file \'' + output_file + '\' was overwritten successfully.')
            return                
        else:
            logging.info('Merging cancelled by user.')
            SystemExit

def pdf_write_output(writer, writer_output_file):
    '''
    Outputs a PDF file to the specified path via the provided PDF writer object.
    '''
    if not os.path.exists(writer_output_file):
        write_output = open(writer_output_file, 'wb')
        writer.write(write_output)
        logging.info('The split file \'' + writer_output_file + '\' was created successfully.')
        write_output.close()
        return
    else:
        override = input('The output file \'' + writer_output_file + '\' already exists. Overwrite this file? (Y/N): ')
        if override == 'Y' or override == 'y':
            write_output = open(writer_output_file, 'wb')
            writer.write(write_output)
            logging.info('The split file \'' + writer_output_file + '\' was overwritten successfully.')
            write_output.close()
            return                
        else:
            logging.info('Merging cancelled by user.')
            SystemExit

setup()
