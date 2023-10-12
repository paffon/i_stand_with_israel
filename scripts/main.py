from PIL import Image
import os
import pyperclip


# def show(img, name):
#     path = os.path.join('../debug', name + '.png')
#     img.save(path)


def resize_image_proportionally(img, desired_width):
    """
    Resize an image proportionally to the desired width while maintaining the aspect ratio.

    :param img: The path to the input image file.
    :param desired_width: The desired width for the resized image.
    :return: A resized image with the specified width.
    """

    # Calculate the new height to maintain the aspect ratio
    width_percent = (desired_width / float(img.size[0]))
    new_height = int((float(img.size[1]) * float(width_percent)))

    # Resize the image
    resized_img = img.resize((desired_width, new_height), Image.ANTIALIAS)

    return resized_img


def expand_with_empty_space(img, target_size, x_pos, y_pos):
    """
    Expand the given image with empty space to fit the target size while positioning it as specified.

    :param img: The input image to be expanded.
    :param target_size: A tuple representing the target size (width, height).
    :param y_pos: The vertical position for the input image: 'top', 'middle', or 'bottom'.
    :param x_pos: The horizontal position for the input image: 'left', 'middle', or 'right'.
    :return: A new image expanded to the target size with the input image positioned accordingly.
    """

    # Create a new image of the target size with a transparent background
    new_img = Image.new('RGBA', target_size, (0, 0, 0, 0))

    # Calculate the position to paste the small image based on x_pos and y_pos
    paste_x = 0
    paste_y = 0

    if y_pos == 'top':
        paste_y = 0
    elif y_pos == 'middle':
        paste_y = (target_size[1] - img.height) // 2
    elif y_pos == 'bottom':
        paste_y = target_size[1] - img.height

    if x_pos == 'left':
        paste_x = 0
    elif x_pos == 'middle':
        paste_x = (target_size[0] - img.width) // 2
    elif x_pos == 'right':
        paste_x = target_size[0] - img.width

    # Paste the small image onto the new image
    new_img.paste(img, (paste_x, paste_y))

    return new_img


def my_paste(project_folder, background: Image, art_name='corner_flag.png', desired_background_width=1000, x_pos='bottom', y_pos='right', ratio=1):

    corner_flag = Image.open(os.path.join(project_folder, 'art', art_name))

    resized_background = resize_image_proportionally(background, desired_background_width)

    desired_foreground_width = int(desired_background_width * ratio)

    resized_corner_flag = resize_image_proportionally(corner_flag, desired_foreground_width)
    resized_corner_flag = expand_with_empty_space(resized_corner_flag, resized_background.size, x_pos, y_pos)

    resized_background.paste(resized_corner_flag, (0, 0), resized_corner_flag)

    return resized_background


project_folder = os.path.dirname(os.getcwd())

input_folder = os.path.join(project_folder, 'given_images')

image_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg") or f.endswith(".png")]

os.makedirs(os.path.join(project_folder, 'output_images'), exist_ok=True)

for original_name in image_files:

    # original_name = 'BLM_profile.jpg'

    original_img = Image.open('../given_images/' + original_name)

    art_pieces = [
        # {'name': 'i_stand_with_israel.png', 'x': 'right', 'y': 'top', 'ratio': 1},
        # {'name': 'corner_flag.png', 'x': 'right', 'y': 'bottom', 'ratio': 0.45},
        {'name': 'gays2.png', 'x': 'left', 'y': 'bottom', 'ratio': 0.45},
        {'name': 'pig1.png', 'x': 'right', 'y': 'middle', 'ratio': 0.4},
        {'name': 'loving_pigs.png', 'x': 'right', 'y': 'top', 'ratio': 0.6},
    ]

    for art in art_pieces:
        art_name = art['name']
        x_pos = art['x']
        y_pos = art['y']
        ratio = art['ratio']

        original_img = my_paste(project_folder, original_img, art_name, 1000, x_pos, y_pos, ratio)

    original_img.save('../output_images/' + original_name)

coppied_text = 'FREE PALESTINE FROM HAMAS! This is amazing. Thank you for your support against HAMAS and ISIS.'

pyperclip.copy(coppied_text)
