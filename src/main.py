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
    wordSpacing = 20
    margin = (150,150)
    textFile = './texts/sample01.txt'

    # Process page size
    pageWidth = dpi * width / 10
    pageHeight = dpi * height / 10

    # Load the default font
    writingFont = ImageFont.truetype(fontPath, fontSize)

    # Create the page
    img = Image.new("RGBA", (pageWidth,pageHeight), (255,255,255))
    draw = ImageDraw.Draw(img)

    # Load the text, and split by paragraphs
    text = open(textFile, 'r')
    paragraphs = text.read().split('\n\n')

    # Line tendance neg=up, pos=down
    direction = -1

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
        self.y += self.fontSize + 2 * random.randint(-5,5) - self.direction
        if not isLastWord and self.y >= (self.pageHeight - self.margin[1]):
            self.newPage()

    # Write words
    def createDoc(self):
        for paragraph in self.paragraphs:
            paragraph = paragraph.replace('\n', ' ')
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
                self.draw.text((self.x, self.y), word, (0,0,0), font=self.writingFont)

                # avance cursor
                self.x += size[0] + self.wordSpacing
                self.y += self.direction

            # new paragraph
            self.newLine()
            self.newLine()

        # Save last page
        self.draw = ImageDraw.Draw(self.img)
        fileName = 'pages/page-%03d.png' % self.pageNb
        self.img.save(fileName)


writer = Writer()
writer.createDoc()

# TODO: create the PDF
