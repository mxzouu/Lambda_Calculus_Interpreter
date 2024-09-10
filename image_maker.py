from PIL import Image,ImageDraw,ImageFont
import logic
import random
import datetime

colors = ['black','blue','green','orange','pink','purple','red','yellow'] 

dic_colors={'black': (66,66,66), 'blue':(0,119,255), 'green':(0,255,6), 'orange':(255,135,10), 'pink':(249,161,207), 'purple':(255,0,237), 'red':(255,0,6), 'yellow':(247,255,0)} 

inverse_dic_colors={(66,66,66): 'black',(0,119,255):'blue', (0,255,6):'green',(255,135,10):'orange', (249,161,207):'pink', (255,0,237):'purple',(255,0,6):'red', (247,255,0):'yellow'  }

def color_image(img, color):
    def change_color(pixel):
        return color if pixel == (66, 66, 66) else pixel

    img = img.convert("RGB")  
    img = img.point(lambda p: change_color((p, p, p)))
    
    return img

def associateVariableWithColorBis(variable):
    if str(variable) not in variables_colors_couple:
        variables_colors_couple[str(variable)] = dic_colors[colors[-1]]
        return colors.pop()
    else:
        return inverse_dic_colors[variables_colors_couple[str(variable)]]

def new_color():  
    # TODO!: the loop is not necessary,we can just return the random color unless the intention was to use i as a value for the interval
    for i in range(3):
        r = random.randint(i,255) 
        g = random.randint(i,255) 
        b = random.randint(i,255)
    return (r,g,b)

def close_colors(a,b):
    r = abs(a[0]-b[0])
    g = abs(a[1]-b[1])
    b = abs(a[2]-b[2])
    return r*r+g*g+b*b <= 100*100


variables_colors_couple = {}

def associateVariableWithColor(variable):
    assert logic.isVariable(variable)

    while True:
        c = new_color()
        colors = list(variables_colors_couple.values())

        if not any(close_colors(c, color) for color in colors):
            break

    if str(variable) not in variables_colors_couple:
        variables_colors_couple[str(variable)] = c
#------------------------------------------------------------------------------------------------------------------------------------------
class My_image:
    def __init__(self,image,b):
        self.image=image
        self.is_egg=b

    def resize(self,width,height):
        if not(self.is_egg):
            self.image.resize(width, height)
        else:
            self.image.resize(min(self.image.width,width), min(self.image.height,height))
#---------------------------------------------------------------------------------------------------------------------------------
def createVarImage(variable): 
    assert (logic.isVariable(variable)) 
    if len(colors)!=0: 
        k=associateVariableWithColorBis(variable) 
        egg_img = Image.open("figures/egg_"+k+".png") 
        return egg_img.convert("RGB")
    else: 
        associateVariableWithColor(variable) 
        egg_img = Image.open("figures/egg_black.png") 
        egg_img = egg_img.convert("RGB")
        egg_img = color_image(egg_img,variables_colors_couple[str(variable)]) 
        return egg_img.convert("RGB")

def createAlligator(terme):
    assert logic.isVariable(terme)
    try:
        if len(colors) != 0:
            k = associateVariableWithColorBis(terme)
            alligator_img = Image.open(f"figures/alligator_{k}.png")
        else:
            associateVariableWithColor(terme)
            alligator_img = Image.open("figures/alligator_black.png")
            alligator_img = color_image(alligator_img, variables_colors_couple[str(terme)])
        
        return alligator_img.convert("RGB")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def createAbsImage(terme):
    assert (logic.isAbstraction(terme)), f"Expected ABS type, got {logic.checkType(terme)}"
    input = logic.getInputFromAbs(terme)
    output = logic.getOutputFromAbs(terme)
    im1 =createAlligator(input)
    im2 = createImage(output)
    im1 = im1.resize((max(im2.image.width, im1.width), max((int(im1.height * im2.image.width / im1.width),im1.height))) )
    abstraction = Image.new('RGB', (max(im1.width, im2.image.width), im1.height + im2.image.height), (255, 255, 255))
    abstraction.paste(im1, ((max(im1.width, im2.image.width)-im1.width) // 2, 0))
    abstraction.paste(im2.image, ( 0 , im1.height))
    return abstraction


def get_concat_h_multi_resize(im_list, resample=Image.BILINEAR, space_width=0):
    max_height=max(im.height for im in im_list)
    min_width=min(im.width for im in im_list)

    if space_width == 0:
        space_width=(int(min_width*0.3))
    else:
        space_width=min(space_width,int(min_width*0.3))

    totalWidth = sum(im.width for im in im_list) + space_width * (len(im_list) - 1)

    dst = Image.new('RGB', (totalWidth, max_height),(255,255,255))
    pos_x = 0
    for im in im_list:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width + space_width
    return dst


def createOldAlligator():
    return Image.open("figures/old_alligator.png")


def createOldAlligatorFamily(terme):
    old_alli_img = createOldAlligator()
    family_img = createImage(terme)
    old_alli_img = old_alli_img.resize((max(family_img.image.width, old_alli_img.width), max((int(old_alli_img.height * family_img.image.width / old_alli_img.width),old_alli_img.height))) )
    old_alligator_fam = Image.new('RGB', (max(old_alli_img.width, family_img.image.width), old_alli_img.height + family_img.image.height), (255, 255, 255))
    old_alligator_fam.paste(old_alli_img, ((max(old_alli_img.width, family_img.image.width)-old_alli_img.width) // 2, 0))
    old_alligator_fam.paste(family_img.image, ( 0 , old_alli_img.height))
    return old_alligator_fam

def addNumberToImage(image,number):
    draw = ImageDraw.Draw(image.image)
    font = ImageFont.truetype("AllerDisplay_Std_Rg.ttf", 150)
    draw.text((5, 0),str(number),(0,0,0),font=font)
    return image

def createAppImage(terme):
    assert (logic.isApplication(terme)), f"Expected APP type, got {logic.checkType(terme)}"

    left = logic.getFirstTerm(terme)
    right = logic.getSecondTerm(terme)
    im1 = createImage(left)

    if len(terme) == 4:
        im1 = addNumberToImage(im1,terme[3])
        left = left[:3]
    if len(terme) == 5:
        im1 = addNumberToImage(im1,terme[-1])
    if logic.isApplication(right):
        im2 = createOldAlligatorFamily(right)
        application = get_concat_h_multi_resize([im1.image,im2])
    else:
        im2 = createImage(right)
        application = get_concat_h_multi_resize([im1.image,im2.image])
    return application

def resize_image(im):
    if im.width * im.height > 2073600:
        if ((im.width * 0.5) * (im.height * 0.5)) < 518400:
            im = im.resize((int(im.width * 0.7), int(im.height * 0.7)))
        else:
            im = im.resize((int(im.width * 0.5), int(im.height * 0.5)))
    return im

def createImage(terme):
    if logic.isVariable(terme):
        return My_image(createVarImage(terme),True)
    if logic.isAbstraction(terme):
        im = createAbsImage(terme)
        im = resize_image(im)
        return My_image(im,False)
    
    if logic.isApplication(terme):
        im = createAppImage(terme)
        im = resize_image(im)
        return My_image(im,False)
    else:
        raise Exception("Unsupported term type")


def construct_filename(name, path, date):
    if date:
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d__%H-%M-%S")
        filename = f"{now_string}---{name}.jpeg"
    else:
        filename = f"{name}.jpeg"
    
    if path:
        return f"{path}/{filename}"
    return filename

def saveImage(image, name, path=None, date=True):
    filename = construct_filename(name, path, date)
    image.image.save(filename, 'jpeg', optimize=True, quality=85)
