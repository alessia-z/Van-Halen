import SimpleITK as sitk
import os

def moveIntoFolder(f, name, wdir):
    '''
    Move files into specific folder
    ''' 
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