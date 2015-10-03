all: images pdf clean

images:
	@echo 'Creating sample document'
	python src/main.py

clean:
	rm -f pages/*png

# Create the PDF with ImageMagick
pdf:
	convert pages/*.png texts/sample01.pdf
