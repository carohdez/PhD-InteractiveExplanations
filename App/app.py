import flask
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy import func
from sqlalchemy import desc
import pandas as pd
import os
from commands import bp

import logging

logger = logging.getLogger('app')
handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__, static_url_path='')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite'  # para conectar directamente a sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # para conectar directamente a sqlite
db = SQLAlchemy(app)
db.session.rollback()

# create blueprint to be able to run commands
app.register_blueprint(bp)

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
# engine = create_engine('sqlite:///mydb.sqlite',  poolclass=SingletonThreadPool) # added poolclass to avoid error of different threads
engine = create_engine('sqlite:///mydb.sqlite', echo=True, connect_args={"check_same_thread": False})

# associate it with our custom Session class
Session.configure(bind=engine)

# work with the session
# db_session = Session()

app.secret_key = 'antilope'

init_survey = datetime(year=2020, month=7 ,day=24 ,hour=14)
# flask.globals.session['condition'] = 0

# @app.route('/session/')
# def set_session(condition):
#     session['condition'] = condition
#     return render_template('index.html', name ='session')


# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable= False)
#     completed = db.Column(db.Integer, default=0)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Task %r>' % self.id

class Hotels(db.Model):
    hotelID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    num_reviews = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    stars_file = db.Column(db.String(200))

    def __repr__(self):
        return '<Hotel %r>' % self.hotelID


class Brief_explanations(db.Model):
    hotelID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, primary_key=True)
    explanation = db.Column(db.String, default='')

    def __repr__(self):
        return '<Hotel %r, User %r>' % self.hotelID, self.userID


class Aspects_hotels(db.Model):
    hotelID = db.Column(db.Integer, primary_key=True)
    aspect = db.Column(db.String, primary_key=True)
    comments_positive = db.Column(db.Integer, default=0)
    comments_negative = db.Column(db.Integer, default=0)
    comments_total = db.Column(db.Integer, default=0)
    per_positive = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Hotel %r, aspect %r>' % self.hotelID, self.aspect


class Comments(db.Model):
    hotelID = db.Column(db.Integer, primary_key=True)
    reviewID = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer)
    score = db.Column(db.Integer)
    sentence = db.Column(db.Integer)
    feature = db.Column(db.Integer, primary_key=True)
    polarity = db.Column(db.Integer)
    category_f = db.Column(db.Integer)

    def __repr__(self):
        return '<Hotel %r, review %r, feature %r>' % self.hotelID, self.reviewID, self.feature


class Preferences(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    pref_0 = db.Column(db.String, primary_key=True)
    pref_1 = db.Column(db.String, primary_key=True)
    pref_2 = db.Column(db.String, primary_key=True)
    pref_3 = db.Column(db.String, primary_key=True)
    pref_4 = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '<UserID %r>' % self.userID


class Feature_category(db.Model):
    feature = db.Column(db.String, primary_key=True)
    category = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '<Feature %r, category %r>' % self.feature, self.category


class Reviews(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    hotelID = db.Column(db.Integer)
    review_text = db.Column(db.String)
    author = db.Column(db.String)
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<ReviewID %r>' % self.reviewID


class Actions(db.Model):
    actionID = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String)
    page = db.Column(db.String)
    feature = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    workerID = db.Column(db.String)
    userID = db.Column(db.Integer)
    condition = db.Column(db.Integer)
    hotelID = db.Column(db.Integer)
    reviewID = db.Column(db.Integer)
    back = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Back %r>' % self.back


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'POST':
            # task_content = request.form['content']
            # new_task = Todo(content=task_content)
            # try:
            #     db.session.add(new_task)
            #     db.session.commit()
            #     return redirect('/') # redirect to home page
            # except:
            #     return 'A problem happened'
            print('algo')
        else:
            if not request.args.get('actionslog', None) is None:
                if request.args.get('actionslog', None) == 'a158':
                    #actions = Actions.query.filter(Actions.back == 0).all()
                    # actions=db_session.query(Actions.action_type, Actions.page,Actions.feature,Actions.description,Actions.date,Actions.userID,Actions.condition,Actions.workerID,Actions.hotelID,Actions.reviewID ). \
                    #     filter(Actions.back == 0).order_by(desc(Actions.date)).all()
                    actions = db.session.query(Actions.action_type, Actions.page, Actions.feature, Actions.description,
                                               Actions.date, Actions.userID, Actions.condition, Actions.workerID,
                                               Actions.hotelID, Actions.reviewID). \
                        filter(Actions.back == 0).filter(Actions.date>=init_survey).order_by(desc(Actions.date)).all()

                    return render_template('actionslog.html', actions=actions)
            try:
                # validation initial set of variables
                if (flask.globals.session.get("condition") is None) | (flask.globals.session.get("workerID") is None) | (flask.globals.session.get("userID") is None):
                    if (request.args.get('condition', None) is None) | (request.args.get('workerID', None) is None) | (request.args.get('features', None) is None):
                        return render_template('no_params.html')


                if not request.args.get('book', None) is None: # if user clicked to book hotel
                    if request.args.get('book', None) == 'yes':
                        hotelID=''
                        if not request.args.get('hotelID', None) is None:
                            hotelID = request.args.get('hotelID', None)
                        try:
                            new_action = Actions(page='index', action_type='book', description='',
                                                 userID=flask.globals.session['userID'],
                                                 condition=flask.globals.session['condition'],
                                                 workerID=flask.globals.session['workerID'], hotelID=hotelID)

                            db.session.add(new_action)
                            db.session.commit()
                            db.session.close()
                            return render_template('end_page.html')
                        except Exception as e:
                            db.session.rollback()
                            db.session.close()
                            print('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                            logger.error('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])



                first_in = False
                # set variables in session
                if flask.globals.session.get("condition") is None:  # there's no variables in session yet
                    if not request.args.get('condition', None) is None:  # if we receive the condition in the url (first call)
                        flask.globals.session['condition'] = request.args.get('condition', None)  # then set the variable
                        first_in = True
                else:
                    if not request.args.get('condition', None) is None:
                        if flask.globals.session.get("condition") != request.args.get('condition',
                                                                                      None):  # new condition sent in request
                            flask.globals.session['condition'] = request.args.get('condition', None)

                if flask.globals.session.get("workerID") is None:  # there's no variables in session yet
                    if not request.args.get('workerID', None) is None:  # if we receive the workerID in the url (first call)
                        flask.globals.session['workerID'] = request.args.get('workerID', None)  # then set the variable

                if flask.globals.session.get("userID") is None:  # there's no variables in session yet
                    if not request.args.get('features', None) is None:  # if we receive the features in the url (first call)
                        try:
                            # TODO: infer the user that correspond to the participant' preferences
                            survey = request.args.get('features', None)
                            # survey = survey.split('-')

                            aspects_all = ['facilities', 'staff', 'room', 'bathroom', 'location', 'price', 'ambience',
                                           'food', 'comfort', 'checking']
                            #survey = '1a-9a2a-9a3a4a5a-9a-9'
                            survey = survey.split('a')
                            aspects_survey_str = []
                            for i in range(1, 6):
                                aspects_survey_str.append(aspects_all[survey.index(str(i))])
                            survey = aspects_survey_str
                            print('features from survey: ' + str(survey) + ', workerID:'+flask.globals.session['workerID'])
                            #survey = ['room', 'facilities', 'staff', 'location', 'price']
                            logger.info('features from survey: ' + str(survey) + ', workerID:'+flask.globals.session['workerID'])
                            preferences = Preferences.query.all()

                            common_aspects = pd.DataFrame(columns=['userID', 'common'])
                            for pref in preferences:
                                count_occ = 0
                                for i in survey:
                                    if i in [pref.pref_0, pref.pref_1, pref.pref_2, pref.pref_3, pref.pref_4]: count_occ += 1
                                # print([pref.pref_0, pref.pref_1, pref.pref_2, pref.pref_3, pref.pref_4])
                                # print(count_occ)
                                common_aspects = common_aspects.append(pd.DataFrame({'userID': [pref.userID], 'common': [count_occ]}))

                            max_occ = common_aspects['common'].max()
                            common_aspects = common_aspects[common_aspects.common == max_occ]
                            most_similar = 0
                            for idx, row in common_aspects.iterrows():
                                preferences = Preferences.query.filter(Preferences.userID == row.userID).all()
                                if pref.pref_0 == survey[0]:
                                    most_similar = row.userID # the one with the same first preference

                            if most_similar == 0:
                                for idx, row in common_aspects.iterrows():
                                    if pref.pref_1 == survey[0]:
                                        most_similar = row.userID # the one with the same second preference
                            if most_similar == 0:
                                most_similar = common_aspects.iloc[0,:].userID # first of the most commonalities

                        except Exception as e:
                            print('Error Processing user preferences: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                            logger.error('Error Processing user preferences, we will set the default user: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                            most_similar = 160

                        print("most_similar:" + str(most_similar))
                        userID = most_similar
                        flask.globals.session['userID'] = userID
                    else:
                        userID = 160
                        flask.globals.session['userID'] = userID
                        logger.info('We havent received features, so, we will set the default user: ' + str(e))
                # hotels = Hotels.query.order_by(Hotels.num_reviews).all()  # bring data single table

                # log action
                back = 0
                if not request.args.get('back', None) is None: back = 1
                try:
                    new_action = Actions(page='index', action_type='load', description='',
                                        userID=flask.globals.session['userID'], condition=flask.globals.session['condition'],
                                        workerID=flask.globals.session['workerID'], back=back)

                    db.session.add(new_action)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                    logger.error('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])

                userID=flask.globals.session['userID']
                # hotels = db_session.query(Hotels.hotelID, Brief_explanations.hotelID, Hotels.name, Hotels.num_reviews,
                #                           Brief_explanations.explanation, Hotels.price, Hotels.stars_file). \
                #     outerjoin(Brief_explanations, Hotels.hotelID == Brief_explanations.hotelID). \
                #     filter(Brief_explanations.userID == userID).all()

                hotels = db.session.query(Hotels.hotelID, Brief_explanations.hotelID, Hotels.name, Hotels.num_reviews,
                                          Brief_explanations.explanation, Hotels.price, Hotels.stars_file). \
                    outerjoin(Brief_explanations, Hotels.hotelID == Brief_explanations.hotelID). \
                    filter(Brief_explanations.userID == userID).all()

                # hotels = session.query(Hotels).all()
                return render_template('index.html', hotels=hotels)

            except Exception as e:

                print('Error loading index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                logger.error('Error loading index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                return render_template('error.html')

    except:
        session.rollback()
        print('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        logger.error('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        return render_template('error.html')
    finally:
        print("I will close the session")
        db.session.close()

@app.route('/aspects/<int:hotelID>&<int:back>', methods=['GET', 'POST'])
def aspects(hotelID,back):
    try:
        if request.method == 'POST':
            # task.content = request.form['content']
            # try:
            #     db.session.commit()
            #     return redirect('/') # comeback to homepage
            # except:
            #     return 'There was a problem with updating'
            print('algo')
        else:
            try:
                # aspects_hotel = Aspects_hotels.query.filter(Aspects_hotels.hotelID == hotelID).all() # get consolidated number of comments pos and neg
                #db_session
                aspects_hotel = db.session.query(Hotels.hotelID, Aspects_hotels.hotelID, Hotels.name, Hotels.num_reviews,
                                                 Hotels.stars_file, Hotels.score,
                                                 Aspects_hotels.aspect, Aspects_hotels.comments_negative,
                                                 Aspects_hotels.comments_positive, Aspects_hotels.comments_total). \
                    outerjoin(Aspects_hotels, Hotels.hotelID == Aspects_hotels.hotelID). \
                    filter(Aspects_hotels.hotelID == hotelID).all()

                userID = flask.globals.session.get("userID")
                preferences = Preferences.query.filter(Preferences.userID == userID).all()
                pref = [preferences[0].pref_0, preferences[0].pref_1, preferences[0].pref_2, preferences[0].pref_3,
                        preferences[0].pref_4]
                aspects_all = ['facilities', 'staff', 'room', 'bathroom', 'location', 'price', 'ambience', 'food', 'comfort','checking']
                non_pref = []

                # obtain condition from session
                condition = 0
                if not flask.globals.session.get("condition") is None:
                    condition = flask.globals.session['condition']
                print("condition:" + str(condition))

                # when "more features" option is clicked
                moref = 'no'
                if not request.args.get('moref', None) is None:  # if user clicked more/less aspects
                    moref = request.args.get('moref', None)
                    # Log action
                    try:
                        new_action = Actions(page='aspects', action_type='click', description='more_aspects:'+moref, hotelID=hotelID,
                                             userID=flask.globals.session['userID'],
                                             condition=flask.globals.session['condition'],
                                             workerID=flask.globals.session['workerID'], back=0)

                        db.session.add(new_action)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                        logger.error('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])

                else:
                    try:
                        new_action = Actions(page='aspects', action_type='load', description='', hotelID=hotelID,
                                             userID=flask.globals.session['userID'],
                                             condition=flask.globals.session['condition'],
                                             workerID=flask.globals.session['workerID'], back=back)

                        db.session.add(new_action)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                        logger.error('Error logging action index page: ' + str(e)+ ', workerID:'+flask.globals.session['workerID'])



                for aspect in aspects_all:
                    if not aspect in pref:
                        non_pref.append(aspect)
                        if moref == 'yes':
                            pref.append(aspect)
                aspects_hotel_aux = Aspects_hotels.query.filter(Aspects_hotels.hotelID == hotelID).order_by(
                    Aspects_hotels.comments_total).all()  # get consolidated number of comments pos and neg
                x_ticks = ['0']
                if len(aspects_hotel_aux) > 1:
                    max_comments = aspects_hotel_aux[-1].comments_total  # max number of comments per aspect
                    if max_comments > 10:
                        x_ticks.append(str(round(max_comments / 4)))
                        x_ticks.append(str(round(max_comments / 2)))
                        x_ticks.append(str(round(max_comments / 2) + round(max_comments / 4)))
                        x_ticks.append(str(max_comments))
                    else:
                        x_ticks.append('')
                        x_ticks.append(str(round(max_comments / 2)))
                        x_ticks.append('')
                        x_ticks.append(str(max_comments))
                else:
                    x_ticks = ['', '', '', '', '']
                    max_comments = 1

                #  get the aspect with the most number of negative comments.
                aspects_hotel_aux = Aspects_hotels.query.filter(Aspects_hotels.hotelID == hotelID).order_by(
                    Aspects_hotels.comments_negative).all()
                most_negative_aspect = aspects_hotel_aux[-1].aspect
                per_most_negative_aspect = str(
                    round((aspects_hotel_aux[-1].comments_negative / aspects_hotel_aux[-1].comments_total) * 100))

                print("hotelID" + str(hotelID))
                return render_template('aspects.html', aspects_hotel=aspects_hotel, preferences=preferences, pref=pref,
                                       moref=moref, condition=condition, max_comments=max_comments, x_ticks=x_ticks,
                                       most_negative_aspect=most_negative_aspect,
                                       per_most_negative_aspect=per_most_negative_aspect,
                                       hotelID=hotelID, aspect=aspect)
                # return render_template('update.html', task=task)
            except Exception as e:
                print('Error loading aspects page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                logger.error('Error loading aspects page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                return render_template('error.html')
        return ""
    except:
        session.rollback()
        print('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        logger.error('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        return render_template('error.html')
    finally:
        print("I will close the session")
        db.session.close()

@app.route('/comments/', methods=['GET', 'POST'])
def comments():  # hotelID, feature
    try:
        if request.method == 'POST':
            # task.content = request.form['content']
            # try:
            #     db.session.commit()
            #     return redirect('/') # comeback to homepage
            # except:
            #     return 'There was a problem with updating'
            print('algo')
        else:
            try:
                hotelID = request.args.get('hotelID', None)
                feature = request.args.get('aspect', None)
                aspect = request.args.get('aspect', None)

                # when specific feature option is clicked
                activated = 'All'
                specific_feature = 'no'
                category_f = 1
                if not request.args.get('specific', None) is None:  # if we receive the specific feature
                    specific_feature = request.args.get('specific', None)
                    activated = specific_feature
                    category_f = 0

                feature_query = feature
                if specific_feature != 'no':
                    if specific_feature == 'All':
                        feature_query = aspect
                        category_f = 1
                    else:
                        feature_query = specific_feature

                # Get the comments to display -----------------------------------------------------------------------------
                # comments = Comments.query.filter(Comments.hotelID == hotelID).filter(Comments.feature == feature).all()
                #db_session
                comments = db.session.query(Hotels.hotelID, Comments.hotelID, Hotels.name, Hotels.num_reviews,
                                            Hotels.stars_file, Hotels.score,
                                            Comments.reviewID, Comments.author, Comments.score, Comments.sentence,
                                            Comments.feature, Comments.polarity, Comments.category_f). \
                    outerjoin(Comments, Hotels.hotelID == Comments.hotelID). \
                    filter(Comments.hotelID == hotelID). \
                    filter(Comments.feature == feature_query).\
                    filter(Comments.category_f == category_f).all()

                # get number of comments of specific features--------------------------

                # select count(1) as num_comments,c.feature from comments c, feature_category fc
                # where fc.feature = c.feature
                # and hotelID= 76083 and fc.category = 'location'
                # and category_f=0 group by c.feature order by num_comments
                # db_session
                comments_features = db.session.query(func.count(Comments.sentence).label("num_comments"), Comments.feature). \
                    outerjoin(Feature_category, Comments.feature == Feature_category.feature). \
                    filter(Comments.hotelID == hotelID). \
                    filter(Feature_category.category == aspect). \
                    filter(Comments.category_f == 0). \
                    group_by(Comments.feature). \
                    order_by(desc(func.count(Comments.sentence))). \
                    all()
                # print("most commented feat:" + comments_features[0].feature + ": " + str(comments_features[0].num_comments))
                # print("least commented feat:" + comments_features[-1].feature + ": " + str(comments_features[-1].num_comments))
                most_comm_features = ['All']
                if len(comments_features) > 3:
                    num_buttons = 4
                else:
                    num_buttons = len(comments_features)

                for i in range(0, num_buttons):
                    most_comm_features.append(comments_features[i].feature)
                print(most_comm_features)
                # comments_features = db_session.query(Comments.feature, func.count(Comments.feature)).group_by(Comments.feature). \
                #     filter(Comments.hotelID == hotelID).filter(Comments.feature == feature).filter(Comments.category_f == 0). \
                #     order_by(func.count(Comments.feature)).all()
                # specific_features=[]
                # print(comments_features[-1].feature)
                # specific_features.append(comments_features[-1].feature)

                try:
                    back = 0
                    if not request.args.get('back', None) is None: back = 1
                    if not request.args.get('specific', None) is None:  # if we receive the specific feature
                        description='activated:'+request.args.get('specific', None)
                        action_type='click'
                    else:
                        description = ''
                        action_type='load'
                    new_action = Actions(page='comments', action_type=action_type, description=description, hotelID=hotelID,
                                         userID=flask.globals.session['userID'],
                                         condition=flask.globals.session['condition'],
                                         workerID=flask.globals.session['workerID'], back=back, feature=aspect)

                    db.session.add(new_action)
                    db.session.commit()
                except Exception as e:
                    print('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                    logger.error('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                    db.session.rollback()


                return render_template('comments.html', comments=comments, most_comm_features=most_comm_features,
                                       activated=activated, aspect=aspect)
            except Exception as e:
                print('Error loading comments page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                logger.error('Error loading comments page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                return render_template('error.html')
        return ""
    except:
        session.rollback()
        print('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        logger.error('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        return render_template('error.html')
    finally:
        print("I will close the session")
        db.session.close()

@app.route('/review/<int:reviewID>&<string:aspect>', methods=['GET', 'POST'])
def review(reviewID, aspect):  # reviewID
    try:
        if request.method == 'POST':
            # task.content = request.form['content']
            # try:
            #     db.session.commit()
            #     return redirect('/') # comeback to homepage
            # except:
            #     return 'There was a problem with updating'
            print('algo')
        else:
            try:
                # reviewID = request.args.get('reviewID', None)

                # Get the review to display -----------------------------------------------------------------------------
                review = Reviews.query.filter(Reviews.reviewID == reviewID).all()

                try:
                    new_action = Actions(page='review', action_type='load', description='',
                                         userID=flask.globals.session['userID'],
                                         condition=flask.globals.session['condition'],
                                         workerID=flask.globals.session['workerID'], reviewID=reviewID)

                    db.session.add(new_action)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                    logger.error('Error logging action index page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])


                return render_template('review.html', review=review, aspect=aspect)
            except Exception as e:
                print('Error loading review page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                logger.error('Error loading review page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                return render_template('error.html')
        return ""
    except:
        session.rollback()
        print('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        logger.error('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        return render_template('error.html')
    finally:
        print("I will close the session")
        db.session.close()

@app.route('/hotel_general/<int:hotelID>', methods=['GET', 'POST'])
def hotel_general(hotelID):
    try:
        if request.method == 'POST':
            # task.content = request.form['content']
            # try:
            #     db.session.commit()
            #     return redirect('/') # comeback to homepage
            # except:
            #     return 'There was a problem with updating'
            print("algo")
        else:
            try:
                #db_session
                hotel_revs = db.session.query(Hotels.hotelID, Reviews.hotelID, Hotels.name, Hotels.num_reviews,
                                              Hotels.stars_file, Hotels.score,
                                              Reviews.author, Reviews.score, Reviews.review_text). \
                    outerjoin(Reviews, Hotels.hotelID == Reviews.hotelID). \
                    filter(Hotels.hotelID == hotelID).all()
                try:
                    new_action = Actions(page='hotel_general', action_type='load', description='', hotelID=hotelID,
                                         userID=flask.globals.session['userID'],
                                         condition=flask.globals.session['condition'],
                                         workerID=flask.globals.session['workerID'], back=0)

                    db.session.add(new_action)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Error logging action hotel general page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                    logger.error('Error logging action hotel general page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])


                return render_template('hotel_general.html', hotel_revs=hotel_revs)
            except Exception as e:
                print('Error loading comments page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                logger.error('Error loading comments page: ' + str(e) + ', workerID:'+flask.globals.session['workerID'])
                return render_template('error.html')
        return ""
    except:
        session.rollback()
        print('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        logger.error('Error loading index page: ' + str(e) + ', workerID:' + flask.globals.session['workerID'])
        return render_template('error.html')
    finally:
        print("I will close the session")
        db.session.close()

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/delete/<int:id>') # a wrap # id is the name of the column that we'll use as identifier
# def delete(id): # in html is referenced as a new page, e.g. /delete/{{task.id}}, task.id is the param value
#     task_to_delete = Todo.query.get_or_404(id) # if task with that id doesn't exist, then throw an 404
#     print("delete")
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect ('/')
#     except:
#         return 'There was a problem with deleting'
#


# <td>{{ (aspect.comments_positive/total_comments * 100)|round|int}}</td>
#             <td>{{ (aspect.comments_negative/total_comments * 100)|round|int}}</td>
#

# create db on interactive console
# from app import db
# db.create_all()
