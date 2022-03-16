# Blog-Post
## Author

[Brian Otieno](https://github.com/Otybrian)

# Description

A great way to solidify your knowledge is to teach it to other people. 
There is no better way to express your ideas and opinions than with a personal blog.



## Development Installation
To get the code..

1. Cloning the repository:
  ```bash
https://github.com/Otybrian/My-blog-post
  ```
2. Move to the folder and install requirements
  ```bash
  cd Blog-Post
  pip install -r requirements.txt
  ```
3. Exporting Configurations
  ```bash
  export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://{User Name}:{password}@localhost/{database name}
  ```
4. Running the application
  ```bash
  python3.8 manage.py server
  ```
5. Testing the application
  ```bash
  python3.8 manage.py test
  ```
Open the application on your browser `127.0.0.1:5000`.


## Technology used

* [Python3.8](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Heroku](https://heroku.com)


## License
* *MIT License:*