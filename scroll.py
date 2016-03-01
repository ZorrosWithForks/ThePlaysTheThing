import pygame
import string

'''
 Instead of drawing your stuff directly to the screen, blit it to an intermediate 
 Surface that is higher than the screen Surface. If you want to scroll down, 
 just blit this intermediate Surface "above" the screen Surface.
'''

#IMPORTANT: 'Intermediate' surface *must* be larger than the 'screen' surface

pygame.init()

grey = (55,55,55)

light = (200,200,200)

#screen_width
s_w = 400

#screen_height
s_h = 400

#full_width
f_w = 1600

#full_height
f_h = 2400

#game screen
screen = pygame.display.set_mode((s_w, s_h))

#map window on game screen
display = screen.subsurface(pygame.Rect(50, 50, s_w-100, s_h-100))

#impromptu scroll bar
#scrollbar_y = screen.subsurface(pygame.Rect(s_w-200, 0, s_w-100, s_h-100))

#full display
intermediate = pygame.surface.Surface((f_w, f_h))

#create a Rect the size of the intermediate surface
i_a = intermediate.get_rect()

# x1 equals the 'left' value of the intermediate surface
x1 = i_a[0]

# x2 equals x1 plus the 'width' of the intermediate surface
x2 = x1 + i_a[2]

#still not sure what these are for
a, b = (255, 0, 0), (60, 255, 120)

# y1 equals the 'top' value of the intermediate surface
y1 = i_a[1]

# y2 equals y1 plus the 'height' value of the intermediate surface
y2 = y1 + i_a[3]

# height of the intermediate surface
h = y2-y1

#most of this seems specific to drawing the screen for the demo
#will need to tamper with this more
rate = (float((b[0]-a[0])/h),
         (float(b[1]-a[1])/h),
         (float(b[2]-a[2])/h)
         )
for line in range(y1,y2):
     color = (min(max(a[0]+(rate[0]*line),0),255),
              min(max(a[1]+(rate[1]*line),0),255),
              min(max(a[2]+(rate[2]*line),0),255)
              )
     pygame.draw.line(intermediate, color, (x1, line),(x2, line))

y = 20
f = pygame.font.SysFont('', 17)
for l in string.ascii_letters:
    intermediate.blit(f.render(l, True, (255, 255, 255)), (10, y))
    y += 20

clock = pygame.time.Clock()    
quit = False
#Update, yeah everything between this and the previous comment is just drawing
#the demo screen

#indicates how much the user has scrolled up or down
scroll_y = 0

scroll_x = 0

#limiter to keep keys from scrolling too fast
move_ticker = 0

delay = 0

#update the scroll_y value when the wheel is scrolled
while not quit:
   quit = pygame.event.get(pygame.QUIT)
   for e in pygame.event.get():
      if e.type == pygame.MOUSEBUTTONDOWN:
         if e.button == 4: scroll_y = min(scroll_y + 15, 0)
         if e.button == 5: scroll_y = max(scroll_y - 15, -(f_h-s_h))
      '''
      if e.type == pygame.KEYDOWN:
         if e.key == pygame.K_UP: scroll_y = min(scroll_y + 15, 0)
         if e.key == pygame.K_DOWN: scroll_y = max(scroll_y - 15, -(f_h-s_h))
         if e.key == pygame.K_LEFT: scroll_x = min(scroll_x + 15, 0)
         if e.key == pygame.K_RIGHT: scroll_x = max(scroll_x - 15, -(f_w-s_w))
      '''
         
   keys_pressed = pygame.key.get_pressed()

   
   if keys_pressed[pygame.K_LEFT]:
      if delay == 0:
         scroll_x = min(scroll_x + 15, 0)
         delay = 5
      else:
         delay -= 1

   if keys_pressed[pygame.K_RIGHT]:
      if delay == 0:
         scroll_x = max(scroll_x - 15, -(f_w-s_w))
         delay = 5
      else:
         delay -= 1

   if keys_pressed[pygame.K_UP]:
      if delay == 0:
         scroll_y = min(scroll_y + 15, 0)
         delay = 5
      else:
         delay -= 1

   if keys_pressed[pygame.K_DOWN]:
      if delay == 0:
         scroll_y = max(scroll_y - 15, -(f_h-s_h))
         delay = 5
      else:
         delay -= 1

   #by using a scroll_y variable when blitting the screen as the main loop,
   #you can scroll by redrawing the scene whenever scroll_y changes
   display.blit(intermediate, (scroll_x, scroll_y))
   #scroll_y.fill(200, 200, 200)
   pygame.display.flip()
   clock.tick(60)