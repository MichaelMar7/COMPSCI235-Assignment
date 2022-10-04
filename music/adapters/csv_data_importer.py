import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.domainmodel.review import Review

# add ModelException class in domain model

#from music.domain.model import Article, Tag, User, make_tag_association, make_comment, ModelException

### TODO: MOVE TO csvdatareader.csv file

def read_csv_file(filename:str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        for row in reader:
            row = [item.strip() for item in row]
            yield row

def load_users(data_path: Path, repo: AbstractRepository):
    users = dict()
    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            1,
            user_name = data_row[1],
            password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def load_reviews(data_path: Path, repo: AbstractRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):
        review = Review(
            track=repo.get_track_by_id(int[data_row[0]]),
            review_text = data_row[2],
            rating=data_row[3]
        )
        repo.add_review(review)
