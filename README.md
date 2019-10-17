`pygame` is a python wrapper for SDL, Simple DirectMedia Layer which is a cross platform
development library designed to provide low level access to audio, keyboard, mouse,
joystick, and graphics hardware via OpenGL and Direct3D.

SDL officialy supports Windows, Mac OS X, Linux, IOS and android.

### Installation
Install **pygame** using *pip*,

`pip instal pygame` inside a virtualenv.

Check your pygame installation by running, `python -m pygame.examples.aliens`

## Basic pygame program
We will write a basic pygame program in which we will draw a blue circle in the center
of a white screen.

So to start with,

```
import pygame

# initialize the pygame library
pygame.init()

# setup the display window of 500 width & 500 height
screen = pygame.display.set_mode((500, 500))

# run the loop until user closes the window
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with white background color
    screen.fill((255, 255, 255))

    # draw a solid blue color in the center
    pygame.draw.circle(screen, (0, 255, 255), (250, 250), 75)

    # flip the display
    pygame.display.flip()


# at last quit from pygame
pygame.quit()
```

Without initializing `pygame` library using `pygame.init()` there is no pygame.

To draw a cirlce we use, `pygame.draw.circle` which takes,

1. window on which to draw the cirlce, `screen`
2. The color of the circle, `(0, 255, 255) # rgb`
3. `(250, 250)` is the center coordinates of the circle
4. `75` is the radius of the circle to draw in pixels.

Updates the contents of the display to the screen, without calling this nothing will be
displayed on the screen. Last line `exists` pygame only after the loop ends.

## Writing our game
We have imported some constants from `pygame.locals` to avoid writing them, now initialize
the pygame using `pygame.init()` to connect pygame modules with the specific hardware you
are using.

```
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pygame.init()

# define constants for screen width & height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
```

### Setting up game loop
Every game uses a game loop to control gameplay. The game loop does four very important
things,

1. Processes user input
2. Updates the state of all game objects
3. Updates the audio and display of game
4. Maintains the speed of the game

Every cycle of the game is called a frame and the quicker you do things in each cycle
the faster your game will run. Frames continue to occur until the game is met some
condition and exists.

The first thing that game loop does is process user input to allow the player to move
around the screen. Therefore, you need some way to capture and process the variety of
inputs, you can do this using pygame event system.

There are many ways through which events are generated for example, mouse clicks,
keyboard button presses, joysticks clicks, handling all these events is referred to as
**handling** them and the code for them is called **event handler**.

Each event that is passed into pygame is stored in a queue which contains some attributes,
like the **type** of event and the **key** which is actually pressed.

We can access list of all the active events from a queue from `pygame.event.get()`. You
then loop through these events, inspect each type and handle event accordingly.

```
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # user has clicked the escape key, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # user has clicked the window close button, stop the loop
        elif event.type == QUIT:
            running = False
```

In previous example we used `screen.fill(r, g, b)` and `pygame.draw.circle()` to draw on'
the screen, now we will use **surface** for drawing on the screen.

**Screen** is a **Surface** object, we can create separate surfaces using
`pygame.Surface((width, height))` and treat it like any other screen,

```
...
screen.fill((255, 255, 255))

surf = pygame.Surface((50, 50))
surf.fill((0, 0, 0))
rect = surf.get_rect()
...
```

We access the underlying **rect** from **Surface** using `.get_rect()` which we will use
later.

Just creating a surface isn't enough to show it on the screen, we need to **blit** the
surface onto another surface, here **blit** is **Block Transfer** and we will do it onto
the **screen**. Keep in mind that you can only `blit()` one surface over another surface.

```
screen.blit(surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
pygame.display.flip()
```

`.blit()` takes two arguments, one the surface on which to draw and second the location
at which to draw it on the surface.

Don't forget to call `.flip()` after the `.blit()` because this updates the entire
screen with everything that's been drawn since the last flip. Without the call to
`.flip()` nothing is shown.

You might have noticed that we wanted the surface to be in the center of the screen but
it is slightly onto the right, we need to subtract the surface height and width from the
screen height and width and then divide the resultant half.

```
surf_center = (
    ((SCREEN_WIDTH - surf.get_width()) / 2),
    ((SCREEN_HEIGHT - surf.get_height()) / 2)
)

screen.blit(surf, surf_center)
pygame.display.flip()
```

This will place the Surface object right in the center of the screen.

We have planned to make the objects appear from the right and the player with move from
left to right so, how do we know that the player has hit the object and what about
many other events that will take place in the game, we achieve all of this using
**sprites**.

In programming terms, **sprite** is a 2D representation of something on the screen

## Players
We will be using `Sprite` object with the current game to define our player

```
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.rect.get_rect()
```

Now we will be using our new Player class object to draw the player, replace the
surface with the surface from the Player object

```
player = Player()


    ...
    screen.blit(player.surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    pygame.display.flip()
```

If you pass in `player.rect` as the coordinates for `.blit` then it uses the top left
corner of the screen to draw the surface, this will come handy when moving the object.

## User input
Till now we have been using the event queue and looping over the list to get all the
active key press events using `KEYDOWN`, pygame also provides us with
`pygame.key.get_pressed()` which will return a dictionary of the active pressed keys.

Now we will take in user input and move the player rectangle accordingly,

Inside `Player` class define a method `update` that would take in the `pressed_keys`
dictionary and update the position of the player with the user's input,
```
class Player(pygame.sprite.Sprite):
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

...
while running:
    ...
    # fetch the dict containing active pressed keys in queue
    pressed_keys = pygame.key.get_pressed()

    # pass the pressed keys for player to update posisiton
    player.update(pressed_keys)

    ...
    # change the coordinates of blit surface to the rect of player
    screen.blit(player.surf, player.rect)
```

Notice the way we update the position of the rectangle by using `.move_ip` which stands
for **move in place** and,

1. For moving up we pass in negative value as second arg
2. For moving down we pass positive value as second arg
3. For moving left we pass negative value as first arg
4. For moving right we pass positive value as first arg

Keeping the first first arg as *0* in UP & DOWN and the second arg as *0* in LEFT &
RIGHT movements.

Now you should be able to change the position of the player using the UP, DOWN, LEFT
& RIGHT keys.

There are two things to be noticed,

1. On keeping the keys pressed they move very fast.
2. The rectangle goes beyond the screen.

We will fix the boundaries of the rectangle by adding a check on the coordinates of
the rectangle and stopping it to go beyond the screen width and height.

Add code to the `update` method of `Player` to restrict the player to screen boundaries.

```
    def update(self, pressed_keys):
        ...

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
```

Instead of changing the position using `.move` we simply change the coordiantes directly.

The above logic is very simple to be explained, just know that we map the screen from top
left corner with coordinates `(0, 0)`.

## Sprite Groups
Sprite groups is another useful class which is an object that holds all the sprite
objects. With the help of methods provided by Sprite groups, we can detect collisions
between enemy and player and update things easily.

For our purpose we will be creating two sprite groups,

1. Holds all the sprite objects
2. Holds only the enemy objects

```
# Create sprite groups for all and enemies
#    - all sprites will be used for rendering
#    - enemies will be used to detect collisions and updates
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group
all_sprites.add(enemies)
```

`.kill` method of sprite kills the sprite object from everywhere, including the
sprite groups which helps the python garbage collector the reclaim the memory as
necessary.

We can loop over all the sprites and render them on the screen,

```
    ...
    # loop over all objects and draw them
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # flip everything to display
    pygame.display.flip()
    ...
```

## Custom events
`pygame` defines events internally as unique integers so to define our custom event
in pygame we need to define a new event with a unique integer. The last event in pygame
is `USEREVENT` so we add **1** to it and make our event unique.

Now we need to insert event into the event queue at regular intervals throughout the game
using `time` module in `pygame`. We add **ADDENMY** event using `time` modules `set_timer`
at four times a minute and it will fire throughout the entire game.

We call `pygame.timer.set_timer` outside the `while` loop which calls the `ADDENMY` event
which is catched by the condition inside `for` loop, when this event is caught we create
a object of `Enemy` class and add that object to the Enemy `Group` and also we add this
object in the `all_sprites` Group. At last we call the `update` method of the enemies
Group.

## Collision detection
`pygame` has many built-in methods to check for any collision with `Group` and a `Sprite`.
One such method is `spritecollideany` which accepts a `Sprite` and `Group` as parameters.
It looks for every object in the `Group` and checks if its `.rect.` intersects with
`.rect` of `Sprite`. If so then it returns True.

```
    if pygame.sprite.spritecollideany(player, enemies):
        # if so then remove the player and stop the loop
        player.kill()
        running = False
```

### Adding images
**pygame** has `image` module that lets us handle images, we don't wanna make our game
boring so we will use images for player, enemies and background as well.

Change the code for `Player` class and `Enemy`,

```
from pygame.locals import (
    RLEACCEL,
    ...
)
...
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/jet.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
...
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/missle.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
```

### Background image
For adding a background image we will use the same approach we applied for `Player`
and `Enemy` classes, we will list out out our process,

1. Create a `Cloud` class.
2. Add an image of cloud to it
3. Define a `update` method that would move the cloud images from left to right.
4. Create a custom event and handler to create cloud objects at certain time interval.
5. Add the newly created cloud objects to a new Group called `clouds`.
6. Update and draw the clouds in your game loop.

```
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/cloud.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
```

Now create a custom event just like you did with `ADDENMY`,

```
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
```

This timer will add custom event`ADDCLOUD` after every one second which we will then
handle to create new objects of `Cloud`.

```
...
clouds = pygame.sprite.Group()
```

Now we only have to handle this event using a event handler, we will create new objects
of `Cloud` in this event handler and give a moving background feeling to our players.

```
    elif event.type == ADDCLOUD:
        new_cloud = Cloud()
        clouds.add(new_cloud)
        all_sprites.add(new_cloud)

    ...
    enemies.update()
    clouds.update()
```

Number of frames handled each second is called the frame rate and this is the difference
between a playable game and a forgettable one. Normally you would want the frame rate to
be as high as possible but for our game we need to make is playable so we will use the
pygame's `time` module which has **Clock** which is designed for this purpose only.

Creating desired frame rate for the game requires only two lines of code, first initialize
the `clock` using `clock = pygame.time.Clock()`.

The second line of code calls the `.tick()` method to inform **pygame** that program has
reached the end of the frame.

## Sound effects
Pygame has `mixer` module which handles all the sound related code, the name `mixer`
refers to the fact that the module mixes sounds into a cohesive own.

`pygame.init()` will load the defaults for our `pygame.mixer` module but if you want
to change the defaults then call `pygame.mixer.init()` before `pygame.init()` with the
arguments you want to change.

After the system is initialized, we can get your sounds and background music setup.

```
# load and play background music
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# load all sound files
move_up_sound = pygame.mixer.Sound("Rissing_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
```

We load the background music file and add make it play in loops forever using named
paramter `loops=-1`.

We have loaded the music files for certain events like moving up and down and on
colliding, we can call the `.play()` method of the sound file in the `.update` methods.

```
class Player(pygame.sprite.Sprite):
    ...
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
```

We need to play the collision sound effect when we detect the collision,

```
    ...
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        # stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        running = False
```

We stop all other sounds because when the player collides with the enemy, the game is
stopped and only the collision sound is made since there are no movements after the
collision.

Finally when the game is over, all sounds are stopped by,

```
pygame.mixer.music.stop()
pygame.quit()
```
