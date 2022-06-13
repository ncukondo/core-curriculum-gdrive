.PHONY: downloads python_files csv markdown output texts docs

output:
	make downloads
	rm -rf output
	make csv
	make texts
	make docs
	mkdir -p output_in_github
	cp -r ./output/* output_in_github


csv:
	python ./python/output_outcomes_csv.py

texts:
	python ./python/output_outcomes_text.py

docs:
	python ./python/output_docs_data.py


downloads:
	python ./python/download_sheets.py
	python ./python/download_docx.py
	python ./python/download_zip_doc.py

python_files:
	jupyter nbconvert --to python ./src/*.ipynb
	rm -rf python
	mkdir -p python
	cp ./src/*.py python
	cp -r ./src/lib python
	rm ./src/*.py
