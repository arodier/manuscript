clean:
	rm -f pages/*png

all:
	@echo 'Creating sample document'
	python src/main.py

# Create the PDF with ImageMagick
pdf:
	convert pages/*.png doc.pdf
