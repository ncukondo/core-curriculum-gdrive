.PHONY: sheets python_files csv markdown output

output:
	make sheets
	rm -rf output
	make csv
	make markdown
	mkdir -p output_in_github
	cp -r ./output/* output_in_github

markdown:
	python ./python/output_markdown.py

csv:
	python ./python/output_csv.py

sheets:
	python ./python/download_sheets.py

python_files:
	jupyter nbconvert --to python ./src/*.ipynb
	rm -rf python
	mkdir -p python
	cp ./src/*.py python
	cp -r ./src/lib python
	rm ./src/*.py
