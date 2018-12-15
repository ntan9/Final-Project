"""
Sprite move between different rooms.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_rooms
"""
import math
import arcade
import os
import objects

#For the dialogue stuff
TEXT_BOX_HEIGHT = 100

#Scaling all the images on the screen
SPRITE_SCALING = 5
SPRITE_NATIVE_SIZE = 8
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 30
SCREEN_HEIGHT = SPRITE_SIZE * 16

#Game states
START = -1
GAME = 0
DIALOGUE = 1
INVENTORY = 2

#Inherent traits of player
MOVEMENT_SPEED = 5

class Player(arcade.Sprite):
    def __init__(self):
        """creates the character Sprite"""
        #The parent init method
        super().__init__("Images/CharacterRight.png", SPRITE_SCALING)
        
        #Motion variables
        self.leftMotion = False
        self.rightMotion = False
        self.upMotion = False
        self.downMotion = False
        self.inventory = Inventory()

        #Directional Facing
        self.direction = ["UP", "RIGHT"]

        #Interacting Variables
        self.useObject = False
    
    def update_animation(self):
        """Adding images that show which direction the character is facing"""
        if self.direction[1] == 'LEFT':
            self.texture = arcade.load_texture("Images/CharacterRight.png", mirrored = True, scale = SPRITE_SCALING)
        elif self.direction[1] == 'RIGHT':
            self.texture = arcade.load_texture("Images/CharacterRight.png", scale = SPRITE_SCALING)

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self, ):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None
        self.portal_list = None
        self.object_list = None
        self.door_list = None
        self.transparent_list = arcade.SpriteList()
        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None
        

class Inventory:
    """Holds all the information about the player's inventory"""
    def __init__(self, screen_width = SCREEN_WIDTH, center_height = SCREEN_HEIGHT - (TEXT_BOX_HEIGHT // 4), inv_height = TEXT_BOX_HEIGHT // 2):
        self.item_sprites = arcade.SpriteList()
        self.screen_width = screen_width
        self.inv_height = inv_height
        self.center_height = center_height
        self.item_list = ['KEY'] #starts with key for now for debugging

    def storeSprites(self):
        """Stores each item in the player's inventory as a sprite in item_sprites"""
        item_locations = [150, 200, 250]
        location = 0
        for item in self.item_list:
            if item == 'KEY':
                key = arcade.Sprite('Images/key.png', SPRITE_SCALING)
                key.left = item_locations[location]
                key.bottom = self.center_height - 20
                location += 1
                self.item_sprites.append(key)
            else:
                continue
    
    def useItem(self):
        """Uses up an item and removes from inventory"""
        self.item_list.pop()
        self.item_sprites = arcade.SpriteList()
        self.storeSprites()

    def showInventory(self):
        """Draws the inventory and all its current components."""
        arcade.draw_rectangle_filled(self.screen_width//2, self.center_height, self.screen_width, self.inv_height, arcade.color.EGGPLANT)
        arcade.draw_text('INVENTORY:', 20, self.center_height - 8, arcade.color.BLACK, 18)
        self.storeSprites()
        self.item_sprites.draw()
        


class Portal(arcade.Sprite):
    """
    This class represents the portals on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

def setup_room_1():
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.portal_list = arcade.SpriteList()
    room.object_list = arcade.SpriteList()
    room.door_list = arcade.SpriteList()

    # Draw background
    for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
        for y in range(0, SCREEN_HEIGHT, SPRITE_SIZE):
            floor = arcade.Sprite("Images/RogueSprites/floor.png", SPRITE_SCALING)
            floor.left = x
            floor.bottom = y
            room.transparent_list.append(floor)

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create walls of holding cell
    for x in range(0, 6 * SPRITE_SIZE, SPRITE_SIZE):
        wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
        wall.left = x
        wall.bottom = 6 * SPRITE_SIZE
        room.wall_list.append(wall)
    for y in range(0, 5 * SPRITE_SIZE, SPRITE_SIZE):
        if (y != SPRITE_SIZE * 3):
            wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
            wall.left = 5 * SPRITE_SIZE
            wall.bottom = y
            room.wall_list.append(wall)        

    # Create walls of first room
    for x in range(0, 11 * SPRITE_SIZE, SPRITE_SIZE):
        wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
        wall.left = x
        wall.bottom = 8 * SPRITE_SIZE
        room.wall_list.append(wall)
    for y in range(0, 8 * SPRITE_SIZE, SPRITE_SIZE):
        if (y != SPRITE_SIZE * 3):
            wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
            wall.left = 10 * SPRITE_SIZE
            wall.bottom = y
            room.wall_list.append(wall)   

    # Create middle dividing wall
    for y in range(0, SCREEN_HEIGHT, SPRITE_SIZE):
        if (y != SPRITE_SIZE * 5):
            wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
            wall.left = 14 * SPRITE_SIZE
            wall.bottom = y
            room.wall_list.append(wall)         

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up on the right side
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5) or x == 0:
                wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    # If you want coins or monsters in a level, then add that code here.
    # Make a portal
    portal = Portal("Images/gold_portal.png", SPRITE_SCALING)
    portal.left = 5 * SPRITE_SIZE
    portal.bottom = 6 * SPRITE_SIZE
    room.portal_list.append(portal)

    # Adding interactable objects
    box = objects.InteractObjects("Images/Sign.png", SPRITE_SCALING, "A boring, brown, container... Oh, never mind. It has a key.", otherMessage = "Yup, just a boring, brown, container...", key = True)
    box.left = 2 * SPRITE_SIZE
    box.bottom = 13 * SPRITE_SIZE
    # Adding this object to the wall_list so that it can be drawn and have collision
    room.wall_list.append(box)
    room.object_list.append(box)

    # Same as the above
    box2 = objects.InteractObjects("Images/Sign.png", SPRITE_SCALING, "Another daft box. ")
    box2.left = 4 * SPRITE_SIZE
    box2.bottom = 13 * SPRITE_SIZE
    room.wall_list.append(box2)
    room.object_list.append(box2)

    # Crates
    crate1 = objects.InteractObjects("Images/barrel.png", SPRITE_SCALING, "A sturdy wooden crate. ")
    crate1.left = 3 * SPRITE_SIZE
    crate1.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(crate1)
    room.object_list.append(crate1)

    # Creating starting note
    note1 = objects.InteractObjects("Images/note.png", SPRITE_SCALING, "The note reads: Sometimes, backtracking is necessary.")
    note1.left = 4 * SPRITE_SIZE
    note1.bottom = 1 * SPRITE_SIZE
    room.object_list.append(note1)
    #room.transparent_list.append(note1)
    room.wall_list.append(note1)

    # Creating doors:
    door1 = objects.InteractObjects("Images/LockDoor.png", SPRITE_SCALING, "A locked door. I'll need to get a key.", lock = True, door = True)
    door1.left = 14*SPRITE_SIZE
    door1.bottom = 5*SPRITE_SIZE
    room.wall_list.append(door1)
    room.door_list.append(door1)
    room.object_list.append(door1)

    door2 = objects.InteractObjects("Images/LockDoor.png", SPRITE_SCALING, "A locked door. I'll need to get a key.", lock = True, door = True)
    door2.left = 5*SPRITE_SIZE
    door2.bottom = 3*SPRITE_SIZE
    room.wall_list.append(door2)
    room.door_list.append(door2)
    room.object_list.append(door2)

    door3 = objects.InteractObjects("Images/LockDoor.png", SPRITE_SCALING, "A locked door. I'll need to get a key.", lock = True, door = True)
    door3.left = 10*SPRITE_SIZE
    door3.bottom = 3*SPRITE_SIZE
    room.wall_list.append(door3)
    room.door_list.append(door3)
    room.object_list.append(door3)

    # Furniture
    bed = objects.InteractObjects("Images/bed.png", SPRITE_SCALING, "A filthy bed... Looks like there's a key hidden beneath the blanket.", otherMessage="A filthy bed.", key = True)
    bed.left = 1 * SPRITE_SIZE
    bed.bottom = 1 * SPRITE_SIZE
    room.wall_list.append(bed)
    room.object_list.append(bed)


    #door4 = objects.InteractObjects("Images/LockDoor.png", SPRITE_SCALING, 'Opened the door.', door = True)
    #door4.left = 5*SPRITE_SIZE
    #door4.bottom = 7*SPRITE_SIZE
    #room.wall_list.append(door4)
    #room.door_list.append(door4)
    #room.object_list.append(door4)

    # Load the background image for this level.
    room.background = arcade.load_texture("Images/floor1.jpg")

    return room


def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.portal_list = arcade.SpriteList()
    room.object_list = arcade.SpriteList()
    room.door_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH -  SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5) or x != 0:
                wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("Images/RogueSprites/block1.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)



    #Setting the background of the room
    room.background = arcade.load_texture("Images/floor1.jpg")

    return room



class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(x, y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Start", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()



class MyGame(arcade.Window):
    """ Main application class. """
    
    def __init__(self, width, height):
        """
        Initializer
        """
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Button list
        self.button_list = None

        # Sprite lists
        self.current_room = 0

        #Setting the state of the game
        self.state = GAME

        #The object that has a message with it
        self.current_message = None

        # Set up the player
        self.rooms = None
        self.score = 0
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None
        self.useObject = None
        self.total_time = 0.0

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.score = 0
        self.player_sprite = Player()
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        #Setting the state of the game
        self.state = START

        # Our button list
        self.button_list = []
        
        start_button = StartTextButton(60, 570, self.start_game)
        self.button_list.append(start_button)

        # Our list of rooms
        self.rooms = []

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        # Our starting room number
        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

    def start_game(self):
        """
        Start the game
        """
        self.state = GAME

    def draw_start(self):
        """
        Draw the start menu
        """
        for button in self.button_list:
            button.draw()

    def draw_game(self):
        """
        Render the screen.
        """

        # Draw the background texture

        self.rooms[self.current_room].transparent_list.draw()

        #arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
        #                              SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)


        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()

        # If you have coins or monsters, then copy and modify the line
        # above for each list.
        self.rooms[self.current_room].portal_list.draw()


        #Draws all player sprites
        self.player_list.draw()



        self.rooms[self.current_room].door_list.draw()

    def draw_dialogue(self):
        """Draws the dialogue over the screen"""
        self.draw_game()
        """Delivers the object's message when interacted with"""

        message = self.current_message.message
        # displays a rectangle of a certain color at the bottom of the screen.
        #arcade.start_render()
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2, TEXT_BOX_HEIGHT//2, SCREEN_WIDTH, TEXT_BOX_HEIGHT, arcade.color.DARK_BLUE)
        
        # displays text inside the rectangle.
        arcade.draw_text(message, 20,  TEXT_BOX_HEIGHT - 35, arcade.color.WHITE, 16)


    def draw_inventory(self):
        self.draw_game()
        self.player_sprite.inventory.showInventory()
        

    def on_draw(self):
        """Draws the things on the screen"""
        arcade.start_render()

        if self.state == START:
            self.draw_start()

        elif self.state == GAME:
            self.draw_game()

        elif self.state == DIALOGUE:
            self.draw_dialogue()
        elif self.state == INVENTORY:
            self.draw_inventory()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        
        
        if self.state == GAME:
            ## MOVEMENT:
            if key == arcade.key.UP:
                #The direction is made so that we'll know what object the player will interact with
                self.player_sprite.direction[0] = "UP"
                #This boolean is used for the program to remember that this key was pressed and is held down
                self.player_sprite.upMotion = True
                #Changing the velocity of the player
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.direction[0] = "DOWN"
                self.player_sprite.downMotion = True
                self.player_sprite.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.direction[1] = "LEFT"
                self.player_sprite.leftMotion = True
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.direction[1] = "RIGHT"
                self.player_sprite.rightMotion = True
                self.player_sprite.change_x = MOVEMENT_SPEED

            ## PLAYER INTERACTIONS:
            elif key == arcade.key.Z:
                self.player_sprite.useObject = True
            
            elif key == arcade.key.C:
                #Ensuring there is no movement after opening the inventory
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.rightMotion = False
                self.player_sprite.leftMotion = False
                self.player_sprite.upMotion = False
                self.player_sprite.downMotion = False

                self.state = INVENTORY

        #Exiting the diaglogue stage
        elif self.state == DIALOGUE:
            if key == arcade.key.Z:
                #Changing the dialouge if the object has another message
                if self.current_message.otherMessage != None:
                    self.current_message.changeMessage()
    

                self.player_sprite.useObject = False
                self.state = GAME
                
        #Press X or C to exit inventory
        elif self.state == INVENTORY:
            if key == arcade.key.C or key == arcade.key.X:
                self.state = GAME
        

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        ## MOVEMENT:
        if self.state == GAME:
            #Handles if two opposing keys are being pressed
            #UP and DOWN key
            if self.player_sprite.upMotion and self.player_sprite.downMotion:
                #If UP is released, move down
                if key == arcade.key.UP:
                    #Make the upMotion boolean false bc not moving up anymore
                    self.player_sprite.upMotion = False
                    #Change the direction the player is facing
                    self.player_sprite.direction[0] = 'DOWN'
                    #Changing the velocity of the object
                    self.player_sprite.change_y = -MOVEMENT_SPEED
                #If DOWN is released, move up
                elif key == arcade.key.DOWN:
                    self.player_sprite.downMotion = False
                    self.player_sprite.direction[0] = 'UP'
                    self.player_sprite.change_y = MOVEMENT_SPEED
                #This will handle any other key being released
                elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                    self.player_sprite.rightMotion = False
                    self.player_sprite.leftMotion = False
                    self.player_sprite.change_x = 0
            #RIGHT and DOWN key 
            elif self.player_sprite.leftMotion and self.player_sprite.rightMotion:
                #If RIGHT is released, move left
                if key == arcade.key.RIGHT:
                    self.player_sprite.rightMotion = False
                    self.player_sprite.direction[1] = 'LEFT'
                    self.player_sprite.change_x = -MOVEMENT_SPEED
                #If LEFT is released, move right
                elif key == arcade.key.LEFT:
                    self.player_sprite.leftMotion = False
                    self.player_sprite.direction[1] = 'RIGHT'
                    self.player_sprite.change_x = MOVEMENT_SPEED
                #Handle all other key being pressed
                elif key == arcade.key.UP or key == arcade.key.DOWN:
                    self.player_sprite.upMotion = False
                    self.player_sprite.downMotion = False
                    self.player_sprite.change_y = 0

            #Normal movement with only one key being held down
            elif key == arcade.key.UP or key == arcade.key.DOWN:
                self.player_sprite.upMotion = False
                self.player_sprite.downMotion = False
                self.player_sprite.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.rightMotion = False
                self.player_sprite.leftMotion = False
                self.player_sprite.change_x = 0
            

            ## PLAYER INTERACTIONS
            elif key == arcade.key.Z:
                self.player_sprite.useObject = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        check_mouse_release_for_buttons(x, y, self.button_list)

    def update(self, delta_time):
        """ Movement and game logic """
        ## TIME:
        self.total_time += delta_time

        #Changing the sprite to face direction it's direction
        self.player_sprite.update_animation()

        #Normalizing diagonal movement.\:
        #Diagonal speed will be 5 
        #If the player has upward movement
        if self.player_sprite.upMotion:
            if self.player_sprite.rightMotion and self.player_sprite.change_x > 0:
                x = math.sqrt(MOVEMENT_SPEED**2/2)
                y = math.sqrt(MOVEMENT_SPEED**2/2)
            elif self.player_sprite.leftMotion and self.player_sprite.change_x < 0:
                x = -1 * math.sqrt(MOVEMENT_SPEED**2/2)
                y = math.sqrt(MOVEMENT_SPEED**2/2)
        #If the player has downward movement
        if self.player_sprite.downMotion:
            if self.player_sprite.rightMotion and self.player_sprite.change_x > 0:
                x = math.sqrt(MOVEMENT_SPEED**2/2)
                y = -1 * math.sqrt(MOVEMENT_SPEED**2/2)
            elif self.player_sprite.leftMotion and self.player_sprite.change_x < 0:
                x = -1 * math.sqrt(MOVEMENT_SPEED**2/2)
                y = -1 * math.sqrt(MOVEMENT_SPEED**2/2)
    
        #Collision list for portals
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].portal_list)

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        #PORTAL INTERACTION
        elif self.current_room == 0 and len(hit_list) > 0 and self.player_sprite.useObject == True: # len(hit_list) > 0 should be changed later on to be more specific
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

        #Object Interaction
        for items in self.rooms[self.current_room].object_list:
            if items.isColliding(self.player_sprite) and self.player_sprite.useObject:
                #If the object has a key, update inventory
                if items.key:
                    items.key = False
                    self.player_sprite.inventory.item_list.append('KEY')
                
                #Opening doors with a key
                if items.lock and 'KEY' in (self.player_sprite.inventory.item_list):
                    items.message = "Used the key."
                    items.unlock()
                    items.lock = False
                    self.rooms[self.current_room].wall_list.remove(items)
                    self.rooms[self.current_room].object_list.remove(items)
                    self.player_sprite.inventory.useItem()

                #Opening unlocked doors
                #if items.lock == False and items.door == True:
                #    items.unlock()
                #    self.rooms[self.current_room].wall_list.remove(items)
                #    self.rooms[self.current_room].object_list.remove(items)
                    
                #Ensuring there is no movement after interacting with an object
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.rightMotion = False
                self.player_sprite.leftMotion = False
                self.player_sprite.upMotion = False
                self.player_sprite.downMotion = False
                
                self.current_message = items

                #Changing the state of the game
                self.state = DIALOGUE
        

        

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()