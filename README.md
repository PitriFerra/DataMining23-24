# Data mining project 2023/2024
This repository contains all the materials used for conducting the data mining project.

# Dependencies
Here's the list of all the libraries and tools to install before running the project:
* [pip](https://pypi.org/project/pip/)
* [sickit-learn](https://scikit-learn.org/stable/)
* [numpy](https://numpy.org/)
* [kneed](https://pypi.org/project/kneed/)
* [matplotlib](https://pypi.org/project/matplotlib/)
* [faiss](https://pypi.org/project/faiss-cpu/)

If you're on a Ubuntu-like operating system you can run the `dependencies.sh` file on the folder src by running `chmod +x dependencies.sh && ./dependencies.sh` in order to install all the dependencies automatically.

# How to run
Navigate towards the src/algorithms directory and run `python3 generate_data.py` in order to generate data.
Then run the command `python3 main.py` to run the program.

There are three different parts you can decide to run. Here's what you need to add in the CLI to run each different part.
* Add `-p1` to run part one.
* Add `-p2` to run part two.
* Add `-p3` to run part three.

There are a number of ways to run part two:
* Add `-item_item` to use item item collaborative filtering.
* Add `-item_item_lsh` to use item item collaborative filtering with LSH.
* Add `-user_user` to use user user collaborative filtering.
* Add `-user_user_lsh` to use user user collaborative filtering with LSH.
* Add `-content_based` to use content based filtering.
* Add `-content_based` to use content based filtering.
* Add `-hybrid` to use content hybrid filtering, i.e. content based with LSH + item item with LSH.

The default option is item item with LSH.
