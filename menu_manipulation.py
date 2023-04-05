import pygame as pg 
from pygame import Rect
from random import randint
from menu_assets import Label, Button

def gen_rect(x,y):
    return pg.Rect((0,0),(x,y))

def is_rect_dict(d):
    if not type(d) == dict: 
        return False
    for k,v in d.items():
        if not isinstance(k, Rect):
            return False
    return True

def is_label_dict(d):
    if not type(d) == dict: 
        return False
    for k,v in d.items():
        if not isinstance(k,Label):
            return False
    return True

def is_button_dict(d):
    if not type(d) == dict: 
        return False
    for k,v in d.items():
        if not isinstance(k,Button):
            return False
    return True

def map_rects_func(rects,func):
    new_rects = []
    for rect in rects:
        new_rects.append(func(rect))
    return new_rects

def map_rect_dict_func(rects_dict, func):
    new_rects_dict = {}
    for key, rect in rects_dict.items():
        new_rect = func(rect)
        new_rects_dict[key] = new_rect
    return new_rects_dict

def map_label_dict_func(label_dict, function):
    new_label_dict = label_dict
    for key,label in new_label_dict.items():
        label.rect = function(label_dict[key]) 
    return new_label_dict

def map_rect_dict_list_func(rects_dict, func):
    rect_list = []
    key_list = []
    for key, rect in rects_dict.items():
        rect_list.append(rect)
        key_list.append(key)
    new_rect_list = func(rect_list)
    return dict(zip(key_list,new_rect_list))
        
def rect_to_label_function(label, func):
    new_label = label
    new_label.rect = func(label.rect)
    return new_label

def margin_top_rect(margin_px, rect):
    new_rect = rect
    new_rect.y += margin_px
    new_rect.height -= margin_px
    return new_rect
def margin_top_label(margin_px,label):
    return rect_to_label_function(label, lambda rect: margin_top_rect(margin_px,rect))
def margin_top_label_dict(margin_px,label_dict):
    return { key: margin_top_label(margin_px,label) for key,label in label_dict.items()}

def margin_top(margin_px, obj):
    if isinstance(obj, Label):
        return margin_top_label(margin_px,obj)
    elif type(obj) == dict:
        return margin_top_label_dict(margin_px,obj)
    elif type(obj) == Rect:
        return margin_top_rect(margin_px,obj)

def margin_bottom_rect(margin_px,rect):
    new_rect = rect
    new_rect.height -= margin_px
    return new_rect
def margin_bottom_label(margin_px,label):
    return rect_to_label_function(label,lambda rect: margin_bottom_rect(margin_px,rect))
def margin_bottom_label_dict(margin_px,label_dict):
    return {key : margin_bottom_label(margin_px,label) for key,label in label_dict.items()}

def margin_vertical_rect(margin_px,rect):
    margin_bottom_rect(margin_px,margin_top_rect(margin_px,rect))
def margin_vertical_label(margin_px,label):
    return margin_top_label(margin_px,margin_bottom_label(margin_px,label))
def margin_vertical_label_dict(margin_px,label_dict):
    return {key:margin_vertical_label(margin_px,label) for key,label in label_dict.items()}

def margin_right_rect(margin_px,rect):
    new_rect = rect
    new_rect.width -= margin_px
    return new_rect
def margin_right_label(margin_px,label):
    return rect_to_label_function(label,lambda rect: margin_right_rect(margin_px,rect))
def margin_right_label_dict(margin_px,label_dict):
    return { key: margin_right_label(margin_px,label) for key,label in label_dict.items()}

def margin_left_rect(margin_px,rect):
    new_rect = rect
    new_rect.left += margin_px
    new_rect.width -= margin_px
    return new_rect
def margin_left_label(margin_px,label):
    return rect_to_label_function(label, lambda rect: margin_left_rect(margin_px,rect))
def margin_left_label_dict(margin_px,label_dict):
    return { key: margin_left_label(margin_px,label) for key,label in label_dict.items()}

def margin_horizontal_rect(margin_px,rect):
    return margin_left_rect(margin_px,margin_right_rect(margin_px,rect))
def margin_horizontal_label(margin_px,label):
    return margin_left_label(margin_px,margin_right_label(margin_px,label))
def margin_horizontal_label_dict(margin_px,label_dict):
    return margin_left_label_dict(margin_px,margin_right_label_dict(margin_px,label_dict))


def margin_label(margin_px,label):
    return margin_horizontal_label(margin_px,margin_vertical_label(margin_px,label))
def margin_label_dict(margin_px,label_dict):
    return margin_horizontal_label_dict(margin_px,margin_vertical_label_dict(margin_px,label_dict))

def margin(margin_px,obj):
    if is_button_dict(obj) or is_label_dict(obj):
        return margin_label_dict(margin_px,obj)
    elif isinstance(obj,Label):
        return margin_label(margin_px,obj)
    return None

def random_square(size_min,size_max):
    size = randint(size_min,size_max)
    return pg.Rect(0,0,size,size)

def rect_below(rect1, rect2):
    rect2.top = rect1.bottom
    return rect2
def rect_dict_below(reference_rect, rect_dict):
    return map_rect_dict_func(rect_dict, lambda rect: rect_below(reference_rect, rect))
def label_dict_below(reference_rect, label_dict):
    new_label_dict = label_dict
    for key,label in new_label_dict.items():
        new_label_dict[key].rect = rect_below(reference_rect, label.rect)
    return new_label_dict

def below(obj1,obj2):
    print (get_rect(obj1),obj2)

def get_rect(obj):
    if type(obj) == dict:
        return get_rect(next(iter(obj.items())))[1]
    if type(obj) == list:
        return get_rect(obj[0])
    if not isinstance(obj,Rect):
        return get_rect(obj.rect)
    return obj

def flow_rects_right(rects_list):
    if not rects_list:
        return [] 
    aligned_rects = []
    prev_right = rects_list[0].right
    for i, r in enumerate(rects_list):
        if i != 0:
            r.x = prev_right
            prev_right = r.right
        aligned_rects.append(r.copy())
    return aligned_rects

def flow_label_dict_right(labels_dict):
    if not labels_dict:
        return {}
    aligned_labels = labels_dict
    first_key, first_label = next(iter(aligned_labels.items()))
    prev_right = first_label.rect.right
    for key, label in aligned_labels.items():
        if key != first_key:
            label.rect.x = prev_right
            prev_right = label.rect.right
    return aligned_labels
 
def flow_rect_dict_right(rect_dict):
    return map_rect_dict_list_func(rect_dict, flow_rects_right)

def flow_right(obj):
    if type(obj) == dict:
        if is_rect_dict(obj):
            return flow_rect_dict_right(obj)
        elif is_label_dict(obj) or is_button_dict(obj):
            return flow_label_dict_right(obj)
    elif type(obj) == list:
        return flow_rects_right(obj)
    return None

def translate_rects(rects_list, offset):
    if not rects_list or not offset:
        return []
    
    rects = []
    for r in rects_list:
        r.move_ip(offset)
        rects.append(r.copy()) 
    return rects

def space_rects_right(rects_list, offset):
    if not rects_list:
        return []
    head = [rects_list[0]]
    tail = rects_list[1:]
    translated_tail = translate_rects(tail, (offset,0))
    return head + space_rects_right(translated_tail , offset)
    

       


def align_rects_top(rects_list):
    if not rects_list:
        return []

    aligned_rects = []
    
    y = rects_list[0].y
    for r in rects_list:
        r.y = y
        aligned_rects.append(r.copy())
    return aligned_rects

def align_rects_bottom(rects_list):
    if not rects_list:
        return []

    aligned_rects = []
    bottom = rects_list[0].bottom
    for i, r in enumerate(rects_list):
        if i != 0: 
            r.bottom = bottom
        aligned_rects.append(r.copy())
    return aligned_rects

def draw_rects(surface, rects_list, color=(255,255,255)):
    for r in rects_list:
        pg.draw.rect(surface,color,r)

