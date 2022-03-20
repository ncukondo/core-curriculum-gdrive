.PHONY: sheets python_files csv markdown

markdown:
	python ./python/output_markdown.py

csv:
	python ./python/output_csv.py

sheets:
	python -m python.download_sheets

python_files:
	jupyter nbconvert --to python ./ipynb/*.ipynb
	rm -rf python
	mkdir python
	cp ./ipynb/*.py python
	cp -r ./ipynb/lib python
	rm ./ipynb/*.py
