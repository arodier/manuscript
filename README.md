# manuscript

manuscript is a simple python script to generate a PDF document from a text, that seems handwritten.

For an example, see the PDF generated:

- Original text file:  [texts/sample01.txt](texts/sample01.txt)
- Generated PDF: [texts/sample01.pdf](texts/sample01.pdf)

## requirements

The script requires Python 3 and python3-pil:

```
apt install python3-pil
```

## Bugs

On Debian buster, you will have to temporarily allow ImageMagick to convert PDF files.

Parsing PDF is disabled in /etc/ImageMagick-6/policy.xml due to its inherent insecurity.
You may enable it locally by commenting out the following line in the file mentioned above:

```xml
<policy domain="coder" rights="none" pattern="PDF" />
```

See this bug report on arch linux: [imagemagick does not work with PDFs](https://bugs.archlinux.org/task/60580).
