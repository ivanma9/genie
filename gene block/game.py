import tkinter as tk
import random
#from tkinter import Canvas
from PIL import ImageTk, Image
import time

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500

player_queue = []
cat_queue = []
dot_canvas_list = []

# ideas:
#   when gene block catches a memento, his face blinks between two states
#   nyan cat as a snitch that gives an extra special memento
#   when u get all mementos, win game

def bait(canvas, dot_object_list, player, img):
    dot = Dot(canvas, player, img)
    dot_object_list.append(dot)


class Player:
    def __init__(self, canvas, img):
        self.x = 100
        self.y = 100
        self.turning_side = 0 # 0 = right, 1 = down, 2 = left, 3 = up
        self.draw(canvas, img)

    def draw(self, canvas, img):
        if len(player_queue) != 0:
            canvas.delete(player_queue[0]) # delete player from the canvas
            player_queue.pop()
        
        playerSize = 30

        x = canvas.create_image(self.x, self.y, image=img)
        canvas.image = img

        player_queue.append(x)
    
    def moveLeft(self, event, canvas, img):
        self.x -= 15
        self.turning_side = 2
        self.draw(canvas,img)
    
    def moveRight(self, event, canvas,img):
        self.x += 15
        self.turning_side = 0
        self.draw(canvas,img)

    def moveUp(self, event, canvas, img):
        self.y -= 15
        self.turning_side = 3
        self.draw(canvas, img)

    def moveDown(self, event, canvas, img):
        self.y += 15
        self.turning_side = 1
        self.draw(canvas, img)

class Cat:
    def __init__(self, canvas, img):
        self.x = 400
        self.y = 400
        self.draw(canvas, img)
    
    def draw(self, canvas, img):
        if len(cat_queue) != 0:
            canvas.delete(cat_queue[0])
            cat_queue.pop()

        x = canvas.create_image(self.x, self.y, image=img)
        canvas.image = img

        cat_queue.append(x)

    def move_to_nearest_food(self, dot_object_list, canvas, window, img):
        
        minDist = 1000000
        ind = -1
        for i in range(len(dot_object_list)):
            distX = self.x - dot_object_list[i].x
            distX = distX * distX
            distY = self.y - dot_object_list[i].y
            distY = distY * distY
            dist = distX + distY
            print(str(i) + " " + str(dist))
            if (dist < minDist):
                minDist = dist
                ind = i

        if (ind >= 0):
            xDifference = self.x - dot_object_list[ind].x
            yDifference = self.y - dot_object_list[ind].y
            if xDifference <= yDifference:
                if xDifference < 10 and abs(yDifference) > 10:
                    if yDifference > 10:
                        self.moveUp(canvas, img)
                    else:
                        self.moveDown(canvas, img)

                elif xDifference >= 0:
                    self.moveLeft(canvas, img)
                else:
                    self.moveRight(canvas, img)
            else:
                if yDifference < 10 and abs(xDifference) > 10:
                    if xDifference > 10:
                        self.moveLeft(canvas, img)
                    else:
                        self.moveRight(canvas, img)
                
                elif yDifference >= 0:
                    self.moveUp(canvas, img)
                else:
                    self.moveDown(canvas, img)

        window.after(300, self.move_to_nearest_food, dot_object_list, canvas, window, img)

    def move_to_player(self, player, canvas, window, img):
        xDifference = self.x - player.x
        yDifference = self.y - player.y
        
        if xDifference <= yDifference:
            if xDifference < 10 and abs(yDifference) > 10:
                if yDifference > 10:
                    self.moveUp(canvas, img)
                else:
                    self.moveDown(canvas, img)

            elif xDifference >= 0:
                self.moveLeft(canvas, img)
            else:
                self.moveRight(canvas, img)
        else:
            if yDifference < 10 and abs(xDifference) > 10:
                if xDifference > 10:
                    self.moveLeft(canvas, img)
                else:
                    self.moveRight(canvas, img)
            
            elif yDifference >= 0:
                self.moveUp(canvas, img)
            else:
                self.moveDown(canvas, img)
        
        window.after(300, self.move_to_player, player, canvas, window, img)
    
    def moveLeft(self, canvas, img):
        self.x -= 5
        self.draw(canvas, img)
    
    def moveRight(self, canvas, img):
        self.x += 5
        self.draw(canvas, img)
    
    def moveUp(self, canvas, img):
        self.y -= 5
        self.draw(canvas, img)
    
    def moveDown(self, canvas, img):
        self.y += 5
        self.draw(canvas, img)

class Dot:
    def __init__(self, canvas, Player, img):
        # random position initializing
        # self.x = random.randrange(WINDOW_WIDTH)
        # self.y = random.randrange(WINDOW_HEIGHT)
        self.x = Player.x
        self.y = Player.y
        self.draw(canvas, img)

    # draw a dot on canvas
    def draw(self, canvas, img):
        size = 5

        x = canvas.create_image(self.x, self.y, image=img)
        canvas.image = img
        #x = canvas.create_oval(self.x - size, self.y - size, self.x + size, self.y + size, fill='white')
        dot_canvas_list.append(x)
    
    # # reassign random position
    # def changePos(self):
    #     self.x = random.randrange(WINDOW_WIDTH)
    #     self.y = random.randrange(WINDOW_HEIGHT)

def check(player, cat, dot_object_list, memento_list, level, canvas, window):
    # Check if cat reached food
    for dot in dot_object_list:
        if cat.x - 20 <= dot.x <= cat.x + 20 and cat.y - 20 <= dot.y <= cat.y + 20:
            position = dot_object_list.index(dot)
            canvas.delete(dot_canvas_list[position])
            dot_canvas_list.pop(position)
            dot_object_list.pop(position)

    # check if player reached cat
    if player.x - 30 <= cat.x <= player.x + 30 and player.y - 30 <= cat.y <= player.y + 30:
        
        x = canvas.create_image(level * 40 + 50, 30, image=memento_list[level])
        level += 1
        #     self.x = random.randrange(WINDOW_WIDTH)
        #     self.y = random.randrange(WINDOW_HEIGHT)
        if (level > len(memento_list)):
            time.sleep(3)
            print("GAME Complete!")
            # time.sleep(3)
            exit()
        
    window.after(100, check, player, cat, dot_object_list, memento_list, level, canvas, window) # use check() every 100 milliseconds

def main():
    window = tk.Tk() # create window pop-up
    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='black')  # Canvas widget is for drawing
    im = ImageTk.PhotoImage(Image.open("grass.png").resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.ANTIALIAS))
    canvas.pack()  # pack() organize, aka update, widgets onto canvas
    bg_im = canvas.create_image(0, 0, image=im, anchor="nw")

    # Collected mementos / memento inventory
    memento_list = []
    memento_list.append(ImageTk.PhotoImage(Image.open("andre.png").resize((30, 30), Image.ANTIALIAS)))
    memento_list.append(ImageTk.PhotoImage(Image.open("bear.png").resize((30, 30), Image.ANTIALIAS)))
    memento_list.append(ImageTk.PhotoImage(Image.open("eug.png").resize((50, 60), Image.ANTIALIAS)))
    memento_list.append(ImageTk.PhotoImage(Image.open("Paul_Eggert.png").resize((50, 60), Image.ANTIALIAS)))
    level = 0

    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    imag = ImageTk.PhotoImage(Image.open("block.png").resize((50, 60), Image.ANTIALIAS))
    ## The (250, 250) is (height, width)
    player = Player(canvas, imag)

    dotImg = ImageTk.PhotoImage(Image.open("fish.png").resize((30, 30), Image.ANTIALIAS))

    dot_object_list = []

    window.bind("<KeyPress-Left>", lambda event: player.moveLeft(event, canvas, imag)) # need to pass event, otherwise won't work
    window.bind("<KeyPress-Right>", lambda event: player.moveRight(event, canvas, imag))
    window.bind("<KeyPress-Up>", lambda event: player.moveUp(event, canvas, imag))
    window.bind("<KeyPress-Down>", lambda event: player.moveDown(event, canvas, imag))
    window.bind("<space>", lambda event: bait(canvas, dot_object_list, player, dotImg))
    
    path = "cat.png"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(Image.open(path).resize((30, 30), Image.ANTIALIAS))
    ## The (250, 250) is (height, width)
    cat = Cat(canvas, img)
    
    #create 20 dots on canvas

    # for i in range(20):
    #    dot = Dot(canvas)
    #    dot_object_list.append(dot)

    window.after(100, check, player, cat, dot_object_list, memento_list, level, canvas, window) # call check() to check dot&player after 100 milliseconds
    window.after(100, cat.move_to_nearest_food, dot_object_list, canvas, window, img) # call check() to check dot&player after 100 milliseconds
    window.mainloop() # tk.mainloop() -> keep looping until there's an update

main()