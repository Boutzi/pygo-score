# Project 2: Books To Scrape

This script allows you to retrieve information about all products from the website http://books.toscrape.com/.

# Installation:
First, install Python.
Then open the console, navigate to the folder of your choice, and clone this repository:

```
git clone https://github.com/Boutzi/oc-da-python-p2.git
```
Navigate to the repo folder and create a new virtual environment:
```
python -m venv env
```
Next, activate it.
For Windows:
```
env\scripts\activate.bat
```
For Linux:
```
source env/bin/activate
```
Now, install the required packages:
```
pip install -r requirements.txt
```
Finally, you can run the script:
```
python main.py
```

# Config:
In the **main.py** file, change ```page``` and ```category``` variables to switch modes.

```python
# scrape all books from the website
page = 0 
```
```python
# scrape all books from pages between 1 and 50
# example with page 32
page = 32 
```
```python
# scrape all books from any category
# example with Peotry
page = -1 
category = "Poetry"
```