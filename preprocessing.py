import SimpleITK as sitk
import itk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import vtk



def gradient(nrrd_path, output_path):
    print("reading image")
    image= sitk.ReadImage(nrrd_path)
    print("new filter")
    foo = sitk.GradientMagnitudeRecursiveGaussianImageFilter()
    foo.SetSigma(0.5)
    print("run filter")
    result = foo.Execute(image)
    print("writing image")
    sitk.WriteImage(result, output_path, True)

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
    sitk.WriteImage(result, output_path, True)

def hough_transform(nrrd_path, output_path):
    print ('reading image')
    image = sitk.ReadImage(nrrd_path)
    arr = sitk.GetArrayFromImage(image)
    image2d = arr[647,:,:]
    print('creating the slice')
    
    newimage= sitk.GetImageFromArray(image2d)
    print(newimage)
    sitk.WriteImage(newimage, output_path, True)
    
    inputImage = itk.imread(output_path)

    sitk.WriteImage(newimage, output_path)
    InputImageType = itk.Image[itk.F, 2]
    OutputImageType = itk.Image[itk.SS, 2]

    castImageFilter = itk.CastImageFilter[InputImageType, OutputImageType].New()
    castImageFilter.SetInput(inputImage)

    houghfilter = itk.HoughTransform2DCirclesImageFilter.New()
    houghfilter.SetInput(castImageFilter.GetOutput())
    houghfilter.SetNumberOfCircles(1)
    houghfilter.SetMinimumRadius(5.0)
    houghfilter.SetMaximumRadius(10.0)
    print("RUN FILTER")
    houghfilter.Update()
    circles = houghfilter.GetCircles()
    print(circles.size())
    center = circles[0].GetCenterInObjectSpace()
    print(center)
    #return center


def connected_threshold(nrrd_path, output_path):
    #reader = sitk.ImageFileReader()
    #reader.SetFileName(nrrd_path)
    #reader.ReadImageInformation()
    #spacing = reader.GetSpacing()
    #origin = reader.GetOrigin()
    #direction = reader.GetDirection()
    #print(direction)
    #print(spacing)
    #print(origin)
    #center=(255, 345)    
    
    #x = origin[0] + direction[0]*center[0]*spacing[0] + direction[3]*center[1]*spacing[1]
    #y = origin[1] + direction[1]*center[0]*spacing[0] + direction[4]*center[1]*spacing[1]
    #z = origin[2]
    seed1 = [275, 336, 1222]
    seed2 = [273, 269, 647]
    #seed[0] = x
    #seed[1] = y
    #seed[2] = z
    #print(seed)

    image = sitk.ReadImage(nrrd_path)
    segmentationfilter = sitk.ConnectedThresholdImageFilter()
    segmentationfilter.SetLower(200)
    segmentationfilter.SetUpper(800)
    segmentationfilter.SetReplaceValue(1)
    segmentationfilter.AddSeed(seed1)
    segmentationfilter.AddSeed(seed2)
    print('run filter')
    result = segmentationfilter.Execute(image)
    print (segmentationfilter.GetSeedList())
    print('writing image')
    sitk.WriteImage(result, output_path, True)

def erode_filter (nrrd_path, output_path):
    print('reading image')
    image = sitk.ReadImage(nrrd_path)
    erodefilter = sitk.BinaryErodeImageFilter()
    erodefilter.SetKernelRadius(3)
    erodefilter.SetForegroundValue(1)
    erodefilter.SetBackgroundValue(0)
    print('run filter')
    result = erodefilter.Execute(image)
    print('writing image')
    sitk.WriteImage(result, output_path, True)

def connected_threshold2(nrrd_path, output_path):
    seed1 = [275, 336, 1222]
    seed2 = [273, 269, 647]
    print('reading image')
    image = sitk.ReadImage(nrrd_path)
    segmentationfilter = sitk.ConnectedThresholdImageFilter()
    segmentationfilter.SetLower(1)
    segmentationfilter.SetUpper(1)
    segmentationfilter.SetReplaceValue(1)
    segmentationfilter.AddSeed(seed1)
    segmentationfilter.AddSeed(seed2)
    print('run filter')
    result = segmentationfilter.Execute(image)
    print('writing image')
    sitk.WriteImage(result, output_path, True)

def dilate_filter(nrrd_path, output_path):
    print('reading image')
    image = sitk.ReadImage(nrrd_path)
    dilatefilter = sitk.BinaryDilateImageFilter()
    dilatefilter.SetKernelRadius(3)
    dilatefilter.SetForegroundValue(1)
    dilatefilter.SetBackgroundValue(0)
    print('run filter')
    result = dilatefilter.Execute(image)
    print('writing image')
    sitk.WriteImage(result, output_path, True)


def histogram(nrrd_path):
    image = sitk.ReadImage(nrrd_path)
    result = sitk.GetArrayFromImage(image)
    print(type(result))
    print(result.shape)
    plt.figure('historgram')
    result = result.flatten()
    n, bins, patches = plt.hist(result, bins=256, range= (1,result.max()), facecolor='red', alpha=0.75, histtype = 'step')
    plt.show()

def subtraction(nrrd_path, nrrd_path2, output_path):
    print('reading images')
    image1 = sitk.ReadImage(nrrd_path)
    image2 = sitk.ReadImage(nrrd_path2)
    result = sitk.Subtract(image1, image2)
    print('writing image')
    sitk.WriteImage(result, output_path, True)

def build_surface(nrrd_path):
    '''
    Generate a surface 3D file from image mask
    Params:
    segmentation_id : id of the segmentation object
    '''
   
    # read image mask
    image = itk.imread(nrrd_path)
    # initialize imageType and meshType
    imageType = itk.Image[itk.UC,3].New()
    meshType = itk.Mesh[itk.D,3].New()
    # Setup marching cubes filter
    mcubes = itk.BinaryMask3DMeshSource[imageType, meshType].New()
    mcubes.SetInput(image)
    mcubes.SetObjectValue(1)
    # Create temporarary file with .vtk and .stl file extensions
    temp_vtk = './surface.vtk'
    temp_stl =  './surface.stl'
    # Write surface model to file
    writer = itk.MeshFileWriter[meshType].New()
    writer.SetFileName(temp_vtk)
    writer.SetInput(mcubes.GetOutput())
    writer.Update()
    #Read with vtk, smooth and overwrite
    smooth_surface(temp_vtk, temp_stl)


def smooth_surface(vtk_path, output_path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtk_path)
    reader.Update()

    if (reader.GetOutput().GetNumberOfPoints() == 0):
        print('WARNING: nothing to smooth for', vtk_path)
        return 
    
    smoothingIterations = 50
    passBand = 0.05
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(reader.GetOutputPort())
    smoother.SetNumberOfIterations(smoothingIterations)
    smoother.SetPassBand(passBand)
    smoother.Update()

    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(smoother.GetOutput())
    decimate.SetTargetReduction(0.8)
    decimate.PreserveTopologyOn()
    decimate.Update()


    writer = vtk.vtkSTLWriter()
    writer.SetInputData(decimate.GetOutput())
    writer.SetFileTypeToASCII()  
    writer.SetFileName(output_path)  # .stl
    writer.Update()
    











        

