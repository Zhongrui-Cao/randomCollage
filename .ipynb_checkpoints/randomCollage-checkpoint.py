import random
import glob
import sys
from PIL import Image, ImageFilter
import argparse

parser = argparse.ArgumentParser(description='Generate random collages from input images.')
parser.add_argument('input_dir', type=str,
                    help='directory of input images. dont put non img files in')
parser.add_argument('num_output', type=int,
                    help='number of output images you want')

args = parser.parse_args()

def random_crop(im):
    width, height = im.size
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    right = random.randint(0, width - x) + x
    bottom = random.randint(0, height - y) + y
    
    im1 = im.crop((x, y, right, bottom))
    return im1

def random_paste(img, background):
    width, height = background.size
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    background.paste(img, (x, y), img)

def produce_collage(images):
    # 2*5 inch canvas with 300 dpi
    count = 0
    l = len(images)
    printProgress(count, l, prefix='generating collage:', suffix='Complete', barLength=50)

    background = Image.new('RGBA', (600, 1500), (255, 255, 255, 255))

    for img in images:
        croped_img = random_crop(img).rotate(random.randint(5, 360))
        random_paste(croped_img, background)
        count += 1
        printProgress(count, l, prefix='generating collage:', suffix='Complete', barLength=50)
    return background

def random_rotate(img):
    if random.randint(0, 3) != 0:
        return img
    degrees = random.randint(1, 364)
    rotated = img.rotate(degrees, resample=Image.BICUBIC)
    return rotated

def random_filter(img):
    if random.randint(0, 4) == 0:
        r, g, b, a = img.split()
        r = r.point(lambda i: i * random.uniform(0.8, 1.2))
        g = g.point(lambda i: i * random.uniform(0.8, 1.2))
        b = b.point(lambda i: i * random.uniform(0.8, 1.2))
        result = Image.merge('RGBA', (r, g, b, a))
        return result
    if random.randint(0, 4) == 1:
        return img.filter(ImageFilter.BLUR)
    return img

def random_alpha(img):
    im_rgba = img.copy()
    if random.randint(0, 4) == 0:
        im_rgba.putalpha(random.randint(150, 254))
    else:
        im_rgba.putalpha(255)

    return im_rgba

def printProgress(iteration, total, prefix='', suffix='', decimals=1, barLength=100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if len(glob.glob(args.input_dir + '/*')) == 0:
    print("Error: No images in input folder, exiting..")
    quit()
    
l = len(glob.glob(args.input_dir + '/*'))
count = 0
printProgress(count, l, prefix='reading images:', suffix='done', barLength=50)

# Open images in directory
image_list = []
for filename in glob.glob(args.input_dir + '/*'): #dont put non images in path
    im=Image.open(filename).convert("RGBA")
    image_list.append(im)
    count += 1
    printProgress(count, l, prefix='reading images:', suffix='done', barLength=50)
random.shuffle(image_list)

add_prerotation = True
add_filter = True
add_alphafilter = False

# Preprocessing
preprocessed_list = []
count = 0
l = len(image_list)
printProgress(count, l, prefix='Preprocessing images:', suffix='done', barLength=50)
for img in image_list:
    if add_alphafilter:
        img = random_alpha(img)
    if add_prerotation:
        img = random_rotate(img)
    if add_filter:
        img = random_filter(img)

    preprocessed_list.append(img)
    count += 1
    printProgress(count, l, prefix='Preprocessing images:', suffix='Complete', barLength=50)
random.shuffle(preprocessed_list)

for i in range(0, args.num_output):
    collage = produce_collage(preprocessed_list)
    collage.save("./output/collage#" + str(i) + ".png")
    print("saved to " + "./output/collage#" + str(i) + ".png")
    