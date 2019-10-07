from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

class HangmanImage:
    """Draws the hangman image one body part at a time following incorrect guesses."""
    def __init__(self):
        self.image = Image.new('RGB', (300,300), (255,255,255))
        self.image = ImageOps.expand(self.image, border=4, fill="black")
        self.draw = ImageDraw.Draw(self.image)
        self.draw_structure()
        self.body_parts = [self.draw_head,
                           self.draw_torso,
                           self.draw_right_arm,
                           self.draw_left_arm,
                           self.draw_right_leg,
                           self.draw_left_leg]
        self.idx = 0
        
    def draw_structure(self):
        self.draw.line((140,280,280,280), fill="black", width=3)
        self.draw.line((225,280,225,40), fill="black", width=3)
        self.draw.line((225,40,110,40), fill="black", width=3)
        self.draw.line((110,40,110,60), fill="black", width=3)
        
    def draw_next(self):
        self.body_parts[self.idx]()
        self.idx+=1
        
    def draw_head(self):
        self.draw.ellipse((90,60,130,100), outline='black', width=2)
        
    def draw_torso(self):
        self.draw.line((110,100,110,160), fill="black", width=3)
    
    def draw_right_arm(self):
        self.draw.line((110,125,140,120), fill="black", width=3)
        
    def draw_left_arm(self):
        self.draw.line((110,125,80,120), fill="black", width=3)
    
    def draw_right_leg(self):
        self.draw.line((110,160,135,195), fill="black", width=3)
    
    def draw_left_leg(self):
        self.draw.line((110,160,85,195), fill="black", width=3)
        self.draw.text((98,70),"x  x", fill="black")
        
    def get_encoded_image(self):
        b = BytesIO()
        self.image.save(b, format='png')
        return b.getvalue()
