import SimpleITK as sitk
import os
import argparse
import itk
from image_io import organize_series, dicom2nrrd
from preprocessing import gradient, sigmoid, hough_transform, connected_threshold, erode_filter, connected_threshold2, dilate_filter, histogram, subtraction, build_surface, smooth_surface

if __name__ == "__main__":
    # init arg parser
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('--path_to_dicom', action='store',
                        help='percorso alla cartella dicom')
    parser.add_argument('--path_to_nrrd', action='store',
                        help='percorso al file nrrd')
    parser.add_argument('--path_to_nrrd2', action='store',
                        help='percorso al file nrrd 2')
    parser.add_argument('--path_to_vtk', action='store',
                        help='percorso al file vtk')
    parser.add_argument('--organize_series', action='store_true', 
                        help='organizza lo studio in sottocartelle')
    parser.add_argument('--run_gradient', action='store_true', 
                        help='esegue il filtro di magn gradient')
    parser.add_argument('--output_path', action='store',
                        help='percorso al file di output')
    parser.add_argument('--run_sigmoid', action='store_true', 
                        help='esegue sigmoid filter')
    parser.add_argument('--run_hough_transform', action='store_true', 
                        help='esegue hough transform')
    parser.add_argument('--run_connected_threshold', action='store_true', 
                        help='esegue connected threshold')
    parser.add_argument('--run_erode_filter', action = 'store_true', 
                         help= 'esegue erode filter')
    parser.add_argument('--run_connected_threshold2', action='store_true', 
                        help='esegue il secondo connected threshold')
    parser.add_argument('--run_dilate_filter', action = 'store_true', 
                         help= 'esegue dilate filter')
    parser.add_argument('--run_histogram', action = 'store_true', 
                         help= 'istogramma')
    parser.add_argument('--run_subtraction', action = 'store_true', 
                         help= 'sottrazione tra le due maschere')
    parser.add_argument('--build_surface', action = 'store_true', 
                         help= 'crea 3D')
    parser.add_argument('--smooth_surface', action = 'store_true', 
                         help= 'smussa la superficie')

    args = parser.parse_args()
    
    if (args.organize_series and args.path_to_dicom):
        organize_series(args.path_to_dicom)

    if (args.path_to_dicom and args.path_to_nrrd):
        dicom2nrrd(args.path_to_dicom, args.path_to_nrrd)

    if (args.run_gradient and args.path_to_nrrd and args.output_path):
        gradient(args.path_to_nrrd, args.output_path)
    
    if (args.run_sigmoid and args.path_to_nrrd and args.output_path):
        sigmoid(args.path_to_nrrd, args.output_path)

    if (args.run_hough_transform and args.path_to_nrrd and args.output_path):
        hough_transform(args.path_to_nrrd, args.output_path) #center =
        #connected_threshold(args.path_to_nrrd, center)
    
    if (args.run_connected_threshold and args.path_to_nrrd and args.output_path):
        connected_threshold(args.path_to_nrrd, args.output_path)
    
    if (args.run_erode_filter and args.path_to_nrrd and args.output_path):
        erode_filter(args.path_to_nrrd, args.output_path)
    
    if (args.run_connected_threshold2 and args.path_to_nrrd and args.output_path):
        connected_threshold2(args.path_to_nrrd, args.output_path)

    if (args.run_dilate_filter and args.path_to_nrrd and args.output_path):
        dilate_filter(args.path_to_nrrd, args.output_path)

    if (args.run_histogram and args.path_to_nrrd):
        histogram(args.path_to_nrrd)
 
    if (args.run_subtraction and args.path_to_nrrd and args.path_to_nrrd2 and args.output_path):
        subtraction(args.path_to_nrrd, args.path_to_nrrd2, args.output_path)

    if (args.build_surface and args.path_to_nrrd):
        build_surface(args.path_to_nrrd)

    if (args.smooth_surface and args.path_to_vtk and args.output_path):
        smooth_surface(args.path_to_vtk, args.output_path)

    


