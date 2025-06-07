from datetime import datetime, timedelta
from itertools import count
from suadmin.models import Event, EventParticipants
import profile
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from sklearn.ensemble import RandomForestClassifier
from account.models import Profile, Roles
from games.models import GamesPlayed
from staff.models import Attendance, ClassRoomDiscussion, Staff
from student.models import BestPerfomer, Coin, ExtraCirricular, Feedback, Flipped, Student, StudentAttendance, StudentCRDiscussion, StudentQuiz
from pathlib import Path
import csv
import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from joblib import dump, load
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
@ensure_csrf_cookie
def index(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Admin Dashboard'
            
            badges_flip = Flipped.objects.all().order_by('-coin')[:3]
            content['badges_flip'] = badges_flip
            content['best_performers'] = Flipped.objects.all()
            most_coins = Coin.objects.order_by('-coin')[:3]
            content['most_coins'] = most_coins
            students = Profile.objects.filter(role_id = 3)
            games_list = []
            for s in students:
                games = GamesPlayed.objects.filter(profile_id = int(s.id))
                count_coin = 0
                game_dict = {}
                for gm in games:
                    count_coin = count_coin + gm.coins
                game_dict = {'name' : s.name, 'coin' : count_coin}
                games_list.append(game_dict)
            content['games_list'] = sorted(games_list, key = lambda i: i['coin'], reverse = True)
            return render(request, 'admin/index.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

@csrf_protect
def train(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            if request.method == 'POST':
                # Get training option if provided
                training_option = request.POST.get('training_options', 'all')
                
                file_exists = Path(str(BASE_DIR) + '/dataset/dataset.csv')
                if file_exists.is_file():
                    os.remove(str(BASE_DIR) + '/dataset/dataset.csv')

                file = open(str(BASE_DIR) + '/dataset/dataset.csv', 'w')
                file.close()

                # ML part
                crd = StudentCRDiscussion.objects.all()
                fc = Flipped.objects.all()
                gms = GamesPlayed.objects.all()
                atts = StudentAttendance.objects.all()
                quiz = StudentQuiz.objects.all()
                extra = ExtraCirricular.objects.all()

                with open(str(BASE_DIR) + '/dataset/dataset.csv', 'w') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(['id', 'student', 'coin', 'date'])

                current_date = datetime.today()
                
                # Filter data based on training option
                if training_option == 'recent':
                    thirty_days_ago = current_date - timedelta(days=30)
                    crd = crd.filter(date__gte=thirty_days_ago)
                    gms = gms.filter(date__gte=thirty_days_ago)
                    atts = atts.filter(date__gte=thirty_days_ago)
                    quiz = quiz.filter(date_started__gte=thirty_days_ago)
                    extra = extra.filter(date__gte=thirty_days_ago)
                elif training_option == 'high_engagement':
                    # Focus on high coin activities
                    crd = crd.filter(coins__gt=5)
                    gms = gms.filter(coins__gt=10)
                    atts = atts.filter(coin__gt=3)
                    quiz = quiz.filter(score__gt=70)
                    extra = extra.filter(coin__gt=8)
                
                for i in crd:
                    enddate = datetime.strptime(str(i.date), "%Y-%m-%d")
                    days = enddate
                    with open(str(BASE_DIR) + '/dataset/dataset.csv', 'a') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([i.profile.id, i.profile, i.coins, days])
                        
                for i in gms:
                    enddate = datetime.strptime(str(i.date), "%Y-%m-%d")
                    days = enddate
                    with open(str(BASE_DIR) + '/dataset/dataset.csv', 'a') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([i.profile.id, i.profile, i.coins, days])
                        
                for i in atts:
                    enddate = datetime.strptime(str(i.date), "%Y-%m-%d")
                    days = enddate
                    with open(str(BASE_DIR) + '/dataset/dataset.csv', 'a') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([i.student_profile.id, i.student_profile, i.coin, days])
                        
                for i in quiz:
                    enddate = datetime.strptime(str(i.date_started), "%Y-%m-%d")
                    days = enddate
                    with open(str(BASE_DIR) + '/dataset/dataset.csv', 'a') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([i.profile.id, i.profile, i.score, days])
                        
                for i in extra:
                    enddate = datetime.strptime(str(i.date), "%Y-%m-%d")
                    days = enddate
                    with open(str(BASE_DIR) + '/dataset/dataset.csv', 'a') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([i.student_profile.id, i.student_profile, i.coin, days])

                # ML processing
                try:
                    df = pd.read_csv(str(BASE_DIR) + '/dataset/dataset.csv')
                    df['date'] = pd.to_datetime(df['date'])
                    df['date'] = (df['date'] - df['date'].min()) / np.timedelta64(1,'D')
                    df['coin'] = df['coin'].astype('float')
                    
                    # Feature selection and target
                    feature_cols = ['coin', 'date']
                    X = df[feature_cols] # Features
                    y = df.id # Target variable

                    # Split dataset into training set and test set
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

                    # Use Random Forest classifier with improved parameters
                    rfc = RandomForestClassifier(
                        n_estimators=100,
                        max_depth=10,
                        min_samples_split=5,
                        min_samples_leaf=2,
                        random_state=42
                    )
                    
                    # Train model
                    rfc = rfc.fit(X_train, y_train)
                    dump(rfc, str(BASE_DIR) + '/dataset/model_rfcc.pkl')
                    
                    # Calculate accuracy
                    y_pred_rfc = rfc.predict(X_test)
                    accuracy = metrics.accuracy_score(y_test, y_pred_rfc)
                    
                    messages.success(request, f'Model trained successfully with {accuracy:.2%} accuracy')
                except Exception as e:
                    messages.error(request, f'Error training model: {str(e)}')
                
                return HttpResponseRedirect(reverse('su-predict'))
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

@csrf_protect
def predict(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Predict Student Engagement'
            content['student'] = ''
            
            if request.method == 'POST':
                try:
                    model = load(str(BASE_DIR) + '/dataset/model_rfcc.pkl')
                    coin_value = float(request.POST['coin'])
                    days_value = float(request.POST['days'])
                    
                    predict = model.predict([[coin_value, days_value]])
                    
                    # Get confidence score
                    confidence = model.predict_proba([[coin_value, days_value]])
                    max_confidence = np.max(confidence) * 100
                    
                    student = Profile.objects.get(pk=int(predict[0]))
                    if student:
                        content['student'] = f"{student.name} is the predicted student (Confidence: {max_confidence:.1f}%)"
                    else:
                        content['student'] = 'No predictions. Try again with different data'
                except Exception as e:
                    content['student'] = f'Error making prediction: {str(e)}'
            
            return render(request, 'admin/predict.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

@csrf_protect
@ensure_csrf_cookie
def staff(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Staff Management'
            
            # Process staff creation form
            if request.method == 'POST':
                try:
                    # Create profile first
                    profile = Profile()
                    profile.name = request.POST['name']
                    profile.username = request.POST['username']
                    profile.password = request.POST['password']
                    profile.role = Roles.objects.get(pk=2)  # Staff role
                    profile.save()
                    
                    # Then create staff record
                    staff = Staff()
                    staff.profile = profile
                    staff.email = request.POST['email']
                    staff.contact = request.POST['contact']
                    staff.save()
                    
                    messages.success(request, "Staff account created successfully.")
                except IntegrityError:
                    messages.error(request, "Username already exists. Please try another one.")
                except Exception as e:
                    messages.error(request, f"Error creating staff account: {str(e)}")
                
            # Display all staff members
            content['staffs'] = Staff.objects.all()
            
            return render(request, 'admin/staff.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def event(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Events Management'
            
            # Handle event creation
            if request.method == 'POST':
                try:
                    event = Event()
                    event.name = request.POST['name']
                    event.description = request.POST['description']
                    event.date = request.POST['date']
                    event.save()
                    messages.success(request, "Event created successfully.")
                except Exception as e:
                    messages.error(request, f"Error creating event: {str(e)}")
            
            # Display all events
            content['events'] = Event.objects.all()
            
            return render(request, 'admin/event.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def eventParti(request, pk):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Event Participants'
            
            try:
                event = Event.objects.get(pk=pk)
                content['event'] = event
                content['participants'] = EventParticipants.objects.filter(event=event)
                
                # Handle adding participants
                if request.method == 'POST':
                    student_id = request.POST.get('student_id')
                    if student_id:
                        student = Student.objects.get(pk=student_id)
                        participant = EventParticipants()
                        participant.event = event
                        participant.student = student
                        participant.save()
                        messages.success(request, "Participant added successfully.")
                    
                # Available students to add
                content['students'] = Student.objects.all()
                
            except Event.DoesNotExist:
                messages.error(request, "Event not found.")
                return HttpResponseRedirect(reverse('su-event'))
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
            
            return render(request, 'admin/event_participants.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))

def feedback(request):
    if request.session.has_key('account_id'):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Student Feedback'
            
            # Get all feedback items
            content['feedbacks'] = Feedback.objects.all().order_by('-date')
            
            return render(request, 'admin/feedback.html', content)
        else:
            return HttpResponseForbidden()
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('account-login'))
