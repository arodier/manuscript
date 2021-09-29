all: prepare images pdf clean

prepare:
	test -d pages || mkdir pages

images:
	@echo 'Creating sample document'
	python3 src/main.py

clean:
	echo rm -f pages/*png

# Create the PDF with ImageMagick
pdf:
	convert pages/*.png texts/sample01.pdf
