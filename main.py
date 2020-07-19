from PIL import Image, ImageFont, ImageDraw, ImageStat
from collections import defaultdict
import math, glob, os, time, pprint


def get_avg_brightness(image):
    stat = ImageStat.Stat(image)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def convert_to_jpg(file):
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    rgb_im.save(str(file).split('.')[0] + '.jpg')


def file_runner(path, picture, p):
    start_time = time.time()
    progress_dict = {}
    count = 0

    os.chdir(path)
    print(str(len(glob.glob("*.png"))) + " Files To Be Converted To JPEG")
    num_png_files = len(glob.glob('*.png'))
    for file in glob.glob("*.png"):
        convert_to_jpg(file)
        os.remove(file)
        progress_text(num_png_files, count, progress_dict)
    progress_dict.clear()
    print("Files Converted!\n")

    testList = []

    print("Finding average brightness of " + str(len(glob.glob("*.jpg"))) + " photos!")
    dictList = defaultdict(list)
    num_jpg_files = len(glob.glob('*.jpg'))
    for file in glob.glob("*.jpg"):
        count += 1
        image = Image.open(file)
        testList.append(get_area_avg_color(image))
        #dictList[str(rounder(get_avg_brightness(image), base=25))].append(file)
        progress_text(num_jpg_files, count, progress_dict)
    progress_dict.clear()

    if [range(1,25),range(1,25),range(1,25)] in testList:
        print("test")


    print("Files Processed!\n")

    #pprint.pprint(testList)
    image = Image.open(picture)


    #bw_pic_writer(dictList, image, p, progress_dict, start_time)


def imageResize(image, width,height):

    image = image.resize((width,height))
    return image


def get_area_avg_brightness(x,y, n, image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner)
    is (x, y) in the given image"""

    r, g, b = 0, 0, 0
    count = 0
    for s in range(x, x + n + 1):
        for t in range(y, y + n + 1):
            pixlr, pixlg, pixlb = image.getpixel((x,y))
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1

    return rounder(((r/count) + (g/count)+ (b/count)) / 3, base=25)

def get_area_avg_color (image):

    return ImageStat.Stat(image).median


def rounder(x, base=5):
    return int(base * round(float(x)/base))


def pic_chooser (dictList, brightness, count):
    brightness = str(brightness)
    if len(dictList[brightness]) - 1 == count[brightness]:
        count[brightness] = 0
    else:
        count[brightness] = count[brightness] + 1
    return dictList[brightness][count[brightness]], count


def simple_picture_writer (image, p):
    width, height = image.size
    newImage = image.copy()
    for y in range(0,height,p):
        for x in range(0, width,p):
            if get_area_avg_brightness(x,y,p, newImage) == 0:
                newImage.paste(imageResize(Image.open('collect\\bw\\' + str(get_area_avg_brightness(x,y,p, newImage)) + '.jpg'), p,p), (x, y))

    newImage.save('test.png')


def bw_pic_writer(dictList, image, p, progress_dict, start_time):
    width, height = image.size
    newImage = image.copy()

    count = {'0': 0, '25': 0, '50': 0, '75': 0, '100': 0, '125': 0, '150': 0, '175': 0, '200': 0, '225': 0, '250': 0}

    print("Starting to create photo...")
    for y in range(0,height,p):
        for x in range(0, width,p):
            progress_text(height, y, progress_dict)

            avg_brightness =  get_area_avg_brightness(x,y,p, newImage)
            file, count = pic_chooser(dictList, avg_brightness, count)

            newImage.paste(imageResize(Image.open(file), p,p), (x,y))

    newImage.convert('L').save('output\\test2.png')
    print("Image Complete")
    print("Time Taken: " + str(float(time.time() - start_time) / 60) + " Minute(s)")


def progress_text(total, current, dict):
    dict.setdefault('25', False)
    dict.setdefault('50', False)
    dict.setdefault('75', False)


    if current >= total / 4 and not dict['25']:
        dict['25'] = True
        print("25% Complete")
    elif current >= total / 2 and not dict['50']:
        dict['50'] = True
        print("50% Complete")
    elif current >= total / 1.5 and not dict['75']:
        dict['75'] = True
        print("75% Complete")



def textWriter(image):
    file = open('text.txt', 'w')

    image = imageResize(image,2)
    width, height = image.size

    newImage = Image.new('RGB', (width,height), 'white')
    draw = ImageDraw.Draw(newImage)
    font = ImageFont.truetype("arial.ttf", 10)
    rbg = image.convert('RGB')
    for y in range(0,height,5):
        for x in range(0, width,5):
            r,g,b = rbg.getpixel((x,y))
            brightness = sum([r,g,b]) / 3

            if brightness == 0:
                file.write('@')
                draw.text((x,y),'@',(0,0,0), font=font)
            elif brightness <= 50:
                file.write('%')
                draw.text((x, y), '%',(0,0,0), font=font)
            elif brightness <= 100:
                file.write("*")
                draw.text((x, y), '*',(0,0,0), font=font)
            elif brightness <= 150:
                file.write("+")
                draw.text((x, y), '+',(0,0,0), font=font)
            elif brightness <= 200:
                file.write(',')
                draw.text((x, y), ',',(0,0,0), font=font)
            elif brightness <= 255:
                file.write('.')
                draw.text((x, y), ' ',(0,0,0), font=font)

        file.write("\n")
    newImage.save('amazing.png')
    file.close()


file_runner('images\\collect\\', 'e.jpg', 10)


