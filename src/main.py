# coding=utf-8

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import re

# Random parameters
import random

class Writer:
    """A class used to simulate handwritten documents from text"""
    # Drawing arameters. TODO: use the DPI value
    width = 210
    height = 297
    dpi = 90
    fontPath = './fonts/HaloHandletter.otf'
    fontSize = 68
    wordSpacing = [15,25]
    margin = (150,150)
    paragraphSpacing = [2,2.5]

    # This need to be taken from the command line
    textFile = './texts/sample01.txt'
    penColor = (0,0,77)

    # Process page size
    pageWidth = int(dpi * width / 10)
    pageHeight = int(dpi * height / 10)

    # Load the default font
    writingFont = ImageFont.truetype(fontPath, fontSize)

    # Create the page
    img = Image.new("RGBA", (pageWidth,pageHeight), (255,255,255))
    draw = ImageDraw.Draw(img)

    # Load the text, and split by paragraphs
    reader = open(textFile, 'r')
    text = reader.read()
    text = re.sub(r'\n\n+', '\n\n', text)
    paragraphs = text.split('\n\n')

    # Line tendance neg=down, pos=up
    direction = [2,3]

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

    # Draw the character
    def drawCharacter1(self, word, size):
        self.draw.text((self.x, self.y), word, self.penColor, font=self.writingFont)

    # Draw the character
    def drawCharacter2(self, word, size):
        charImg = Image.new("RGBA", size, (255,255,255))
        charDraw = ImageDraw.Draw(charImg)
        self.draw.image((self.x, self.y), charImg, self.penColor, font=self.writingFont)

    # Write words
    def createDoc(self):
        for paragraph in self.paragraphs:
            paragraph = re.sub(r'\s+', ' ', paragraph)
            words = paragraph.split(' ')
            self.x = self.margin[0]
            nbWords = len(words)
            for idx, word in enumerate(words, start=1):
                isLastWord = idx == nbWords

                # Check with if there is enough space on the line for the word
                size = self.draw.textsize(word, font=self.writingFont)
                if (self.x + size[0]) > (self.pageWidth - self.margin[0]):
                    self.newLine(isLastWord)

                # Draw the character
                self.drawCharacter1(word, size)

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
