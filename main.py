import itk


def segmentar_con_watershed(input_image, output_image, threshold, level):
    # Lectura de la imagen de entrada
    Dimension = 2

    FloatPixelType = itk.ctype("float")
    FloatImageType = itk.Image[FloatPixelType, Dimension]
    reader = itk.ImageFileReader[FloatImageType].New(FileName=input_image)
    reader.Update()

    # Aplicación del filtro Gradient Magnitude
    gradientMagnitude = itk.GradientMagnitudeImageFilter.New(Input=reader.GetOutput())

    # Aplicación del filtro Watershed
    watershed = itk.WatershedImageFilter.New(Input=gradientMagnitude.GetOutput())
    watershed.SetThreshold(threshold)
    watershed.SetLevel(level)

    # Aplicación del filtro de mapa de colores
    colormapImageFilter = itk.ScalarToRGBColormapImageFilter.New(
        Input=watershed.GetOutput()
    )
    colormapImageFilter.SetColormap(itk.ScalarToRGBColormapImageFilterEnums.RGBColormapFilter_Jet)

    # Escritura de la imagen de salida
    writer = itk.ImageFileWriter.New(Input=colormapImageFilter.GetOutput(), FileName=output_image)
    writer.Update()


def segmentar_con_confidence_connected(input_image, output_image, seedX, seedY):
    # Lectura de la imagen de entrada
    input = itk.imread(input_image, itk.UC)

    # Creación del filtro Confidence Connected
    confidenceConnectedFilter = itk.ConfidenceConnectedImageFilter.New(
        InitialNeighborhoodRadius=3,
        Multiplier=2,
        NumberOfIterations=5,
        ReplaceValue=255,
        Input=input
    )
    # Establecimiento de las coordenadas de la semilla
    seed = itk.Index[2]()
    seed[0] = seedX
    seed[1] = seedY
    confidenceConnectedFilter.SetSeed(seed)

    # Escritura de la imagen segmentada
    itk.imwrite(confidenceConnectedFilter.GetOutput(), output_image)


# Segmentación con Watershed
segmentar_con_watershed("apples1.jpeg", "apples1_watershed.png", 0.1, 0.2)
segmentar_con_watershed("apples2.jpg", "apples2_watershed.png", 0.1, 0.2)
segmentar_con_watershed("apples3.jpg", "apples3_watershed.png", 0.1, 0.2)
# Segmentación con Confidence Connected
segmentar_con_confidence_connected("apples1.jpeg", "apples1_confidence.png", 100, 150)
segmentar_con_confidence_connected("apples2.jpg", "apples2_confidence.png", 100, 150)
segmentar_con_confidence_connected("apples3.jpg", "apples3_confidence.png", 100, 150)
