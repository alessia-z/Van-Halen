import SimpleITK as sitk
import os
import argparse
from image_io import organize_series, dicom2nrrd
from preprocessing import gradient, sigmoid


if __name__ == "__main__":
    # init arg parser
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('--path_to_dicom', action='store',
                        help='percorso alla cartella dicom')
    parser.add_argument('--path_to_nrrd', action='store',
                        help='percorso al file nrrd')
    parser.add_argument('--organize_series', action='store_true', 
                        help='organizza lo studio in sottocartelle')
    parser.add_argument('--run_gradient', action='store_true', 
                        help='esegue il filtro di magn gradient')
    parser.add_argument('--output_path', action='store',
                        help='percorso al file di output')
    parser.add_argument('--run_sigmoid', action='store_true', 
                        help='esegue sigmoid filter')

    args = parser.parse_args()
    
    if (args.organize_series and args.path_to_dicom):
        organize_series(args.path_to_dicom)

    if (args.path_to_dicom and args.path_to_nrrd):
        dicom2nrrd(args.path_to_dicom, args.path_to_nrrd)

    if (args.run_gradient and args.path_to_nrrd and args.output_path):
        gradient(args.path_to_nrrd, args.output_path)
    
    if (args.run_sigmoid and args.path_to_nrrd and args.output_path):
        sigmoid(args.path_to_nrrd, args.output_path)







