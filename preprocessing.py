import SimpleITK as sitk

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