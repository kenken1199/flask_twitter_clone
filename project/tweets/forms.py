from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class PostTweetForm(FlaskForm):
    tweet = StringField(
        'Tweet',
        validators=[DataRequired(), Length(min=6, max=140 , message = '40文字以内で入力してください')]
    )