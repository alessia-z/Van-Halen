import SimpleITK as sitk
import os
import argparse

def moveIntoFolder(f, name, wdir):
    name = name.strip()
    name = name.replace(" ", "_")
    name = name.replace(",", "_")
    name = name.replace(".", "_")
    name = name.replace("/", "_")
    dest_folder = os.path.join(wdir, name)
    wdir_path = os.path.join(wdir, f)
    dest_path = os.path.join(dest_folder, f)
    os.makedirs(dest_folder, exist_ok=True)
    print(wdir_path, ' >> ', dest_path)
    os.rename(wdir_path, dest_path)


def organize_series(study_folder_path):
    '''
    Organize a DICOM study folder into series subfolders.
    WARNING: This happens in-place.
    Parameters:
    study_folder_path (string): path to DICOM study folder
    '''
    print('Reading... ', study_folder_path)
    # read all the files in the directory (just the metadata)
    for (root, dirs, files) in os.walk(study_folder_path):
        print('root', root)
        print('dirs', len(dirs))
        print('files', len(files))
        data_directory = root
        series_list = []
        desc_list = []
        # get all series id into a list
        for f in range(len(files)):
            print('file', f, '/', len(files))
            path = os.path.join(root, files[f])
            getImageSeriesId(path, series_list, desc_list)
        print('\n\n---------------------------\n\n')
        print(series_list, desc_list)
        print('\n')
        print(len(series_list), len(desc_list))
        print('\n\n---------------------------\n\n')
        # for each series found, get all files and move them into the same folder
        for n in range(len(series_list)):
            series_ID = series_list[n]
            description = desc_list[n]
            sorted_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
                data_directory, series_ID)
            print('series', series_ID, '\tdesc', description,'\tnumber of files', len(sorted_file_names))
            for file_path in sorted_file_names:
                f = os.path.basename(file_path)
                target_dir = os.path.dirname(file_path)
                moveIntoFolder(f, description, target_dir)


def getImageSeriesId(file_name, series_list, desc_list):
    print('Reading image...')
    # A file name that belongs to the series we want to read
    # Read the file's meta-information without reading bulk pixel data
    # print('Reading image...')
    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(file_name)
    try:
        file_reader.ReadImageInformation()
    except:
        print('ERROR while reading: ', file_name)
        print('SKIP file')
        return
    # Get the sorted file names, opens all files in the directory and reads the meta-information
    # without reading the bulk pixel data
    series_ID = file_reader.GetMetaData('0020|000e')
    description = file_reader.GetMetaData('0008|103e')
    # print('seriesId', series_ID, '\t\t descr', description)
    if series_ID not in series_list:
        series_list.append(series_ID)
        desc_list.append(description)
    return series_ID


def readImage(series_folder):
    for (root, dirs, files) in os.walk(series_folder):
        series_id = getImageSeriesId(os.path.join(root, files[0]), [], [])
    sorted_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
        series_folder, series_id)
    # Read the bulk pixel data
    input_image = sitk.ReadImage(sorted_file_names)
    return input_image

def dicom2nrrd(dcm_path, nrrd_path):
    print('Dicom to nrrd...')
    image = readImage(dcm_path)
    img_basename = os.path.basename(dcm_path)
    sitk.WriteImage(image, nrrd_path)
    return image

def gradient(nrrd_path, output_path):
    print("reading image")
    image= sitk.ReadImage(nrrd_path)
    print("new filter")
    foo = sitk.GradientMagnitudeRecursiveGaussianImageFilter()
    foo.SetSigma(0.5)
    print("run filter")
    result = foo.Execute(image)
    print("writing image")
    sitk.WriteImage(result, output_path)

def sigmoid(nrrd_path, output_path):
    print('reading image')
    image = sitk.ReadImage(nrrd_path)
    print("new filter")
    sigmoidfilter = sitk.SigmoidImageFilter()
    sigmoidfilter.SetOutputMinimum(10)
    sigmoidfilter.SetOutputMaximum(900)
    sigmoidfilter.SetAlpha(-100.0)
    sigmoidfilter.SetBeta(100.0)
    print("run filter")
    result = sigmoidfilter.Execute(image)
    print("writing image")
    sitk.WriteImage(result, output_path)


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







