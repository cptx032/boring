from draw import RectangleDraw, OvalDraw

def draggable(item, update=None, init=None, end=None, kmapobject=None):
    '''
    item: must have x and y attributes and bind method
    update(event): function called at each mouse movement
    init(event): function called in the first click
    end(event): function called in release of mouse
    kmapobject: an object with a 'kmap' property where type(kmapobject) == dict

    use item.draggable to set if item is draggable or not
    '''
    item.mouse_offset = None
    item.draggable = True
    def __click(evt):
        if not item.draggable:
            return
        item.mouse_offset = [evt.x - item.x, evt.y - item.y]
        if init:
            init(evt)
    item.bind('<1>', __click, '+')
    def __release(evt):
        if not item.draggable:
            return
        item.mouse_offset = None
        if end:
            end(evt)
    item.bind('<ButtonRelease-1>', __release, '+')
    def __drag(evt):
        if not item.draggable:
            return
        if (kmapobject==None) or (not kmapobject.kmap.get('y', False)):
            item.x = evt.x - item.mouse_offset[0]
        if (kmapobject==None) or (not kmapobject.kmap.get('x', False)):
            item.y = evt.y - item.mouse_offset[1]
        if update:
            update(evt)
    item.bind('<B1-Motion>', __drag, '+')

DRAG_CONTROL_STYLE = {
    'fill': '#00aacc',
    'outline': '#333'
}
def change_control_point_color(item):
    '''
    when mouse is over a control point
    the control points changes your color
    '''
    def __over(event):
        item.style['outline'] = 'red'
        item.update()
    item.bind('<Enter>', __over, '+')
    def __leave(event):
        item.style = DRAG_CONTROL_STYLE
        item.update()
    item.bind('<Leave>', __leave, '+')

def update_control_points(item):
    item.lower_right.x = item.x+item.width-item.lower_right.radius
    item.lower_right.y = item.y+item.height-item.lower_right.radius

    item.bounds.x = item.x
    item.bounds.y = item.y
    item.bounds.width = item.image.width()
    item.bounds.height = item.image.height()
    # put control points over every thing inside canvas
    item.lower_right.up()

def drag_control(item, radius=5, kmapobject=None):
    '''
    create dragcontrol points
    radius: the radius of each control point

    item: must have x, y, width and height attributes and bind method
    '''
    def update_control_point_position(event):
        '''
        when the main item is dragged the control points
        follow
        '''
        update_control_points(item)

    def drag_control_point(event):
        item.width = item.lower_right.x + radius - item.x
        item.height = item.lower_right.y + radius - item.y
        item.bounds.width = item.width
        item.bounds.height = item.height

    item.bounds = RectangleDraw(item.canvas,
        item.x, item.y, item.width, item.height,
        fill='', outline=DRAG_CONTROL_STYLE['fill'])
    item.bounds.style['width'] = 2
    item.bounds.update()
    item.lower_right = OvalDraw(item.canvas,
        item.x+item.width-radius, item.y+item.height-radius, radius*2,
        radius*2, **DRAG_CONTROL_STYLE)

    draggable(item, update=update_control_point_position, kmapobject=kmapobject)
    draggable(item.lower_right, update=drag_control_point, kmapobject=kmapobject)
    change_control_point_color(item.lower_right)

def remove_drag_control(item):
    '''
    remove control points
    '''
    item.draggable = False
    item.lower_right.delete()