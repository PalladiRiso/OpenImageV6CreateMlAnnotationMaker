from os import listdir
from os.path import isfile, join
import string
from PIL import Image
import json

imagespath = './data'
classespath = './metadata/classes.csv'
labelsPath = './labels/detections.csv'

def getImagesNamesAndSizes():
    onlyfiles = []
    for f in listdir(imagespath):
        if isfile(join(imagespath, f)):
            img=Image.open(imagespath + '/' + f)
            w,h=img.size    # w=Width and h=Height
            f = f.removesuffix('.jpg')
            onlyfiles.append([f,w,h])
            
    return onlyfiles

def getCodesToClassesDict():
    d = {}
    with open(classespath) as f:
        for line in f:
            (key, val) = line.split(',')
            d[str(key)] = val.removesuffix('\n')
    return d

def getAnnotationsCsvToDict(): 

    d = {}
    with open(labelsPath) as f:

        for line in f:
            key = line.split(',')[0]
            array = line.split(',')
            val = getValues(array)
            if key in d:
                d[key].append(val)
               
            else:            
                d[str(key)] = [val]


    return d

def getValues(array):
    val = []
    indexis = [2, 4, 5, 6, 7]
    for i in indexis:
        val.append(array[i])
    return val

def createAnnotationsJson(imagesNamesAndSizes, codesToClassesDict, annotationsDict):
    annotations = []
    for imageNameAndSizes in imagesNamesAndSizes:
        if annotationsDict.keys().__contains__(imageNameAndSizes[0]):
            imageSizes = [imageNameAndSizes[1], imageNameAndSizes[2]]
            annotations.append({
                "image": imageNameAndSizes[0] + ".jpg",
                "annotations": convertAnnotations(annotationsDict[imageNameAndSizes[0]], codesToClassesDict, imageSizes)
            })
    return annotations


def convertAnnotations(annotations, codesToClassesDict, imageSizes):
    convertedAnnotations = []
    for annotation in annotations:
        #print(annotation)
        #print('\n')
        
        convertedAnnotations.append({
            "label": codesToClassesDict[annotation[0]],
            "coordinates": {

                "x": round(float(annotation[1]) * int(imageSizes[0])),
                "y": round(float(annotation[3]) * int(imageSizes[1])),
                "width": round((float(annotation[2]) * int(imageSizes[0])) - (float(annotation[1]) * int(imageSizes[0]))),
                "height": round((float(annotation[4]) * int(imageSizes[1])) - (float(annotation[3]) * int(imageSizes[1])))
            }
        })
    return convertedAnnotations
    

def main():
    imagesNamesAndSizes = getImagesNamesAndSizes()

    codeToClasses = getCodesToClassesDict() 
    #print(codeToClasses)
    badFormattedAnnotations = getAnnotationsCsvToDict() 
    data = createAnnotationsJson(imagesNamesAndSizes, codeToClasses, badFormattedAnnotations)
    
    with open('annotations.json', 'w') as f:
        json.dump(data, f, indent=2)
        print("New json file is created from data.json")



if __name__ == "__main__":
    main()