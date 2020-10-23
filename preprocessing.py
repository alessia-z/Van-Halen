import SimpleITK as sitk
import itk


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

    image = sitk.ReadImage(nrrd_path)
    print ('reading image')
    arr = sitk.GetArrayFromImage(image)
    image2d = arr[1208,:,:]
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
    
    


        

