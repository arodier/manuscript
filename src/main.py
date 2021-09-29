# coding=utf-8

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# For the variations
import random

import re

# Random parameters
import random

class Writer:
    """A class used to simulate handwritten documents from text"""
    # Drawing parameters.
    width = 210
    height = 297
    dpi = 90
    fontPath = './fonts/Caveat-VariableFont_wght.ttf'
    fontSize = 40
    wordSpacing = [8,14]
    margin = (150,200)
    paragraphSpacing = [2,4]

    # Line tendance neg=down, pos=up
    direction = [0,2]

    # This need to be taken from the command line
    textFile = './texts/sample01.txt'
    penColor = (0,0,77)

    # Process page size
    pageWidth = int(dpi * width / 10)
    pageHeight = int(dpi * height / 10)

    # Create the fonts list
    writingFonts = []
    writingFonts.append(ImageFont.truetype(fontPath, fontSize-2, layout_engine=ImageFont.LAYOUT_RAQM))
    writingFonts.append(ImageFont.truetype(fontPath, fontSize-1, layout_engine=ImageFont.LAYOUT_RAQM))
    writingFonts.append(ImageFont.truetype(fontPath, fontSize, layout_engine=ImageFont.LAYOUT_RAQM))
    writingFonts.append(ImageFont.truetype(fontPath, fontSize+1, layout_engine=ImageFont.LAYOUT_RAQM))
    writingFonts.append(ImageFont.truetype(fontPath, fontSize+2, layout_engine=ImageFont.LAYOUT_RAQM))

    # Create the page
    img = Image.new("RGBA", (pageWidth,pageHeight), (255,255,255))
    draw = ImageDraw.Draw(img)

    # Load the text, and split by paragraphs
    reader = open(textFile, 'r')
    text = reader.read()
    text = re.sub(r'\n\n+', '\n\n', text)
    paragraphs = text.split('\n\n')

    # remember current page and position
    pageNb = 1
    x = margin[0]
    y = margin[1]

    def newPage(self):
        fileName = 'pages/page-%03d.png' % self.pageNb
        self.img.save(fileName)
        self.pageNb += 1
        self.img = Image.new("RGBA", (self.pageWidth,self.pageHeight), (255,255,255))
        self.draw = ImageDraw.Draw(self.img)
        self.x = self.margin[0]
        self.y = self.margin[1]

    def newLine(self, isLastWord=False):
        self.x = self.margin[0] + 2 * random.randint(-5,5)
        self.y += self.fontSize + 10 * self.direction[1]
        if not isLastWord and self.y >= (self.pageHeight - self.margin[1]):
            self.newPage()

    def newParagraph(self):
        self.x = self.margin[0] + 2 * random.randint(-5,5)
        spcMin = 10 * self.paragraphSpacing[0]
        spcMax = 10 * self.paragraphSpacing[1]
        spacing = (random.randint(spcMin, spcMax)) / 10
        self.y += spacing * self.fontSize + 3 * self.direction[1]
        if self.y >= (self.pageHeight - self.margin[1]):
            self.newPage()

    # Draw the word's characters
    def writeWord(self, word, newParagraph):
        stroke_width = random.randrange(0,1)
        x = self.x

        nbFonts = len(self.writingFonts)

        for letter in word:

            fontIndex = random.randrange(0, nbFonts)
            font = self.writingFonts[fontIndex]

            styleset = "ss0" + str(random.randrange(1,2))
            features = [ "curs", "dlig", styleset, "smcp", "salt", "cpsp" ]

            # Use swash variant for a new paragraph
            if newParagraph:
                features.append("swsh")

            size = self.draw.textsize(letter, font=font)

            y = self.y + random.randrange(-1,1)
            self.draw.text((x, y), letter, self.penColor, font=font,
                           stroke_width=stroke_width, features=features)

            x = x + size[0] - random.randrange(3,6)

    # Write words
    def createDoc(self):

        nbFonts = len(self.writingFonts)

        for paragraph in self.paragraphs:

            paragraph = re.sub(r'\s+', ' ', paragraph)
            words = paragraph.split(' ')
            self.x = self.margin[0]
            nbWords = len(words)

            isFirstWord = True

            for idx, word in enumerate(words, start=1):

                isLastWord = idx == nbWords

                font = self.writingFonts[nbFonts-1]

                # Check with if there is enough space on the line for the word
                size = self.draw.textsize(word, font=font)
                if (self.x + size[0]) > (self.pageWidth - self.margin[0]):
                    self.newLine(isLastWord)

                # Draw the character
                self.writeWord(word, isFirstWord)

                # Not the first word any more
                isFirstWord = False

                # avance cursor
                self.x += size[0] + random.randint(self.wordSpacing[0], self.wordSpacing[1])
                self.y -= random.randint(self.direction[0], self.direction[1])

            # new paragraph
            self.newParagraph()

        # Save last page
        self.draw = ImageDraw.Draw(self.img)
        fileName = 'pages/page-%03d.png' % self.pageNb
        self.img.save(fileName)


writer = Writer()
writer.createDoc()

# TODO: create the PDF
