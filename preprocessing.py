import SimpleITK as sitk
import os
import itk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import vtk
import tempfile
import time
from image_io import readImage


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
    # image = itk.imread(nrrd_path)
    # extractFilter = itk.ExtractImageFilter.New(image)
    # extractFilter.SetDirectionCollapseToSubmatrix()
    # inputRegion = image.GetBufferedRegion()
    # size = inputRegion.GetSize()
    # size[2] = 1  # we extract along z direction
    # start = inputRegion.GetIndex()
    # start[2] = 169
    # desiredRegion = inputRegion
    # finalSize = [size[0], size[1], 0]
    # desiredRegion.SetSize(finalSize)
    # desiredRegion.SetIndex(start)
    # extractFilter.SetExtractionRegion(desiredRegion)
    reader = sitk.ImageFileReader()
    reader.SetFileName(nrrd_path)
    reader.ReadImageInformation()
    size = reader.GetSize()
    tot = size[2]
    z = tot*2//3
    print(z)

    image = sitk.ReadImage(nrrd_path)
    print ('reading image')
    arr = sitk.GetArrayFromImage(image)
    image2d = arr[z,:,:]
    print('creating the slice')
    # from arr nnumero di fette, 512, 512 estrarre 1 fetta
    # image_slice = sitk.GetImageFromArray(new array)
    newimage= sitk.GetImageFromArray(image2d)
    print(newimage)
    sitk.WriteImage(newimage, output_path)
    
    inputImage = itk.imread(output_path)

    sitk.WriteImage(newimage, output_path)
    InputImageType = itk.Image[itk.F, 2]
    OutputImageType = itk.Image[itk.SS, 2]

    castImageFilter = itk.CastImageFilter[InputImageType, OutputImageType].New()
    castImageFilter.SetInput(inputImage)

    houghfilter = itk.HoughTransform2DCirclesImageFilter.New()
    houghfilter.SetInput(castImageFilter.GetOutput())
    houghfilter.SetNumberOfCircles(1)
    houghfilter.SetMinimumRadius(10.0)
    houghfilter.SetMaximumRadius(20.0)
    print("RUN FILTER")
    houghfilter.Update()
    circles = houghfilter.GetCircles()
    print(circles.size())
    center0 = circles[0].GetCenterInObjectSpace()
    #center1 = circles[1].GetCenterInObjectSpace()
    print(center0)
    #print(center1)
    
    
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
    seed1 = [275, 336, z]
    seed2 = [245, 273, z]
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
    seed2 = [245, 273, 573]
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


def aorta_segmentation(dcm_path, output_path):
    
    #dicom2nrrd
    print('dicom to nrrd')
    image = readImage(dcm_path)
    img_basename = os.path.basename(dcm_path)
    temp1 = tempfile.NamedTemporaryFile(suffix='.nrrd', delete= False)
    sitk.WriteImage(image, temp1.name)

    #gradient
    print('gradient')
    image = sitk.ReadImage(temp1.name)
    foo = sitk.GradientMagnitudeRecursiveGaussianImageFilter()
    foo.SetSigma(0.5)
    tic = time.perf_counter()
    gradient = foo.Execute(image)
    toc = time.perf_counter()
    print(f"gradient: {toc - tic:0.4f} seconds")
    
    #sigmoid
    print('sigmoid')
    sigmoidfilter = sitk.SigmoidImageFilter()
    sigmoidfilter.SetOutputMinimum(10)
    sigmoidfilter.SetOutputMaximum(900)
    sigmoidfilter.SetAlpha(-100.0)
    sigmoidfilter.SetBeta(100.0)
    tic = time.perf_counter()
    sigmoid = sigmoidfilter.Execute(gradient)
    toc = time.perf_counter()
    print(f"sigmoid: {toc - tic:0.4f} seconds")
    
    #hough transform
    print('hough transform')
    reader = sitk.ImageFileReader()
    reader.SetFileName(temp1.name)
    reader.ReadImageInformation()
    size = reader.GetSize()
    tot = size[2]
    z = tot*2//3
    

    arr = sitk.GetArrayFromImage(sigmoid)
    image2d = arr[z,:,:]
    newimage= sitk.GetImageFromArray(image2d)
    temp = tempfile.NamedTemporaryFile(suffix='.nrrd', delete= False)
    sitk.WriteImage(newimage, temp.name)

    inputImage = itk.imread(temp.name)
    temp.close()

    InputImageType = itk.Image[itk.F, 2]
    OutputImageType = itk.Image[itk.SS, 2]

    castImageFilter = itk.CastImageFilter[InputImageType, OutputImageType].New()
    castImageFilter.SetInput(inputImage)

    houghfilter = itk.HoughTransform2DCirclesImageFilter.New()
    houghfilter.SetInput(castImageFilter.GetOutput())
    houghfilter.SetNumberOfCircles(1)
    houghfilter.SetMinimumRadius(10.0)
    houghfilter.SetMaximumRadius(20.0)
    tic = time.perf_counter()
    houghfilter.Update()
    
    circles = houghfilter.GetCircles()
    center0 = circles[0].GetCenterInObjectSpace()

    toc = time.perf_counter()
    print(f"hough transform: {toc - tic:0.4f} seconds")

    #connected threshold
    print('connected threshold')
    seed = [int(center0[0]), int(center0[1]), z]
    image3 = sitk.ReadImage(temp1.name)
    segmentationfilter = sitk.ConnectedThresholdImageFilter()
    segmentationfilter.SetLower(200)
    segmentationfilter.SetUpper(800)
    segmentationfilter.SetReplaceValue(1)
    segmentationfilter.AddSeed(seed)
    tic = time.perf_counter()
    connected = segmentationfilter.Execute(image3)
    toc = time.perf_counter()
    print(f"connected threshold: {toc - tic:0.4f} seconds")
    temp1.close()

    #erode filter
    print('erode filter')
    erodefilter = sitk.BinaryErodeImageFilter()
    erodefilter.SetKernelRadius(3)
    erodefilter.SetForegroundValue(1)
    erodefilter.SetBackgroundValue(0)
    tic = time.perf_counter()
    erode = erodefilter.Execute(connected)
    toc = time.perf_counter()
    print(f"erode filter: {toc - tic:0.4f} seconds")

    #connected threshold 2
    print('connected threshold 2')
    segmentationfilter = sitk.ConnectedThresholdImageFilter()
    segmentationfilter.SetLower(1)
    segmentationfilter.SetUpper(1)
    segmentationfilter.SetReplaceValue(1)
    segmentationfilter.AddSeed(seed)
    tic = time.perf_counter()
    connected2 = segmentationfilter.Execute(erode)
    toc = time.perf_counter()
    print(f"connected threshold 2: {toc - tic:0.4f} seconds")

    #dilate filter
    print('dilate filter')
    dilatefilter = sitk.BinaryDilateImageFilter()
    dilatefilter.SetKernelRadius(3)
    dilatefilter.SetForegroundValue(1)
    dilatefilter.SetBackgroundValue(0)
    tic = time.perf_counter()
    dilate = dilatefilter.Execute(connected2)
    toc = time.perf_counter()
    print(f"dilate filter: {toc - tic:0.4f} seconds")

    #build surface
    print('build surface')
    temp = tempfile.NamedTemporaryFile(suffix='.vtk', delete= False)

    # initialize imageType and meshType
    temp2 = tempfile.NamedTemporaryFile(suffix='.nrrd', delete= False)
    sitk.WriteImage(dilate, temp2.name)
    dilateImage = itk.imread(temp2.name)
    temp2.close()

    imageType = itk.Image[itk.UC,3].New()
    meshType = itk.Mesh[itk.D,3].New()
    # Setup marching cubes filter
    mcubes = itk.BinaryMask3DMeshSource[imageType, meshType].New()
    mcubes.SetInput(dilateImage)
    mcubes.SetObjectValue(1)
    # Create temporarary file with .vtk and .stl file extensions
    #temp_vtk = './surface.vtk'
    #temp_stl =  './surface.stl'
    # Write surface model to file
    writer = itk.MeshFileWriter[meshType].New()
    writer.SetFileName(temp.name)
    writer.SetInput(mcubes.GetOutput())
    tic = time.perf_counter()
    writer.Update()
    toc = time.perf_counter()
    print(f"build surface: {toc - tic:0.4f} seconds")
    #Read with vtk, smooth and overwrite
    #smooth_surface(temp.name, temp_stl)

    #smooth surface
    print('smooth surface')
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(temp.name)
    reader.Update()
    temp.close()

    if (reader.GetOutput().GetNumberOfPoints() == 0):
        print('WARNING: nothing to smooth for')
        return 
    

    smoothingIterations = 50
    passBand = 0.05
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputData(reader.GetOutput())
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
    tic = time.perf_counter()
    writer.Update()
    toc = time.perf_counter()
    print(f"smooth surface: {toc - tic:0.4f} seconds")


    





   



        

