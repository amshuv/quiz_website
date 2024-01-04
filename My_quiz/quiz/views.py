from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView
from .models import User, QuesModel, ResultModel
from .forms import PlayerSignUpForm, addQuestionform
from django.http import HttpResponse , HttpResponseRedirect
from django.core.mail import EmailMessage,send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
import io

# Create your views here.

def main(request):
    return render(request, 'main.html')

class player_register(CreateView):
    model = User
    form_class = PlayerSignUpForm
    template_name = 'player_register.html'

    def form_valid(self, form):
        user = form.save(commit=False)  # Save the user form data without committing to the database
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email_id']
        user.save()  # Save the user data to the database
        # Log in the user
        login(self.request, user)

        # Send a registration confirmation email
        subject = 'Registration Confirmation'
        message = 'Thank you for registering on Quizzers. Your account has been successfully created.'
        from_email = 'kataribhuvana2364@gmail.com'  # Replace with your email
        recipient_list = [user.email]  # Use the user's email
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(self.request, 'Registration successful. You are now logged in.')
        return redirect('/quiz/home')

def login_user(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)

                # Send a login confirmation email
                subject = 'Login Confirmation'
                message = 'You have successfully logged in to our website.'
                from_email = 'your_email@example.com'  # Update with your email
                recipient_list = [user.email]  # Use the user's email
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return redirect('/quiz/home')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'login.html',context={'form':AuthenticationForm()})

def logout_user(request):
    logout(request)
    return redirect('/quiz/main')

def home(request):
    return render(request,'home.html')


def addQuestion(request, level):
    if request.user.is_staff:
        form = addQuestionform() # fetches form from forms.py
        if(request.method=='POST'):
            form = addQuestionform(request.POST)
            if(form.is_valid()):
                # Set the level based on the URL parameter
                form.cleaned_data['level'] = level
                form.save()
                return redirect('/quiz/home')
        context={'form':form,'level':level}
        return render(request,'addQuestion.html',context)
    else:
        return redirect('/quiz/home')


def level1_quiz(request,level):
    if request.method == 'POST':
        print(request.POST)
        level1_questions = QuesModel.objects.filter(level='Level 1')
        score=0
        wrong=0
        correct=0
        total=0
        for q in level1_questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                score-=2
                wrong+=1
        percent = score/(total*10) *100
        user = request.user if request.user.is_authenticated else None
        # Create a ResultModel instance and save it
        result = ResultModel(user= user,
                             score=score,
                             level=level,
                             percentage=percent,
                             correct_answers=correct,
                             incorrect_answers=wrong,
                             total_question=total)
        result.save()
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'level':level,
            'date': timezone.now
        }
        return render(request,'result.html',context)
    else:
        level1_questions = QuesModel.objects.filter(level='Level 1')
        context = {
            'questions':level1_questions
        }
        return render(request,'level1.html',context)

def level2_quiz(request,level):
    if request.method == 'POST':
        print(request.POST)
        level2_questions = QuesModel.objects.filter(level='Level 2')
        score=0
        wrong=0
        correct=0
        total=0
        for q in level2_questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                score-=2
                wrong+=1
        percent = score/(total*10) *100
        user = request.user if request.user.is_authenticated else None
        # Create a ResultModel instance and save it
        result = ResultModel(user= user,
                             score=score,
                             level=level,
                             percentage=percent,
                             correct_answers=correct,
                             incorrect_answers=wrong,
                             total_question=total)
        result.save()
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'level': level,
            'date': timezone.now
        }
        return render(request, 'result.html', context)
    else:
        level2_questions = QuesModel.objects.filter(level='Level 2')
        context = {
            'questions': level2_questions
        }
        return render(request, 'level2.html', context)



def user_scores(request):
    # Query the ResultModel to get users and their scores, and sort by score in descending order
    user_scores = ResultModel.objects.select_related('user').order_by('-score')
    context = {'user_scores': user_scores}
    return render(request, 'list.html', context)


def certificate(request):
    if request.user.is_authenticated:
    # Retrieve the user's information from the ResultModel
        user = request.user
        result = ResultModel.objects.latest('date')  # Assuming there is one result per user
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'percentage': result.percentage,
            'level': result.level,
            'date': timezone.now
            }
        return render(request, 'certificate.html', context)
    else:
        return HttpResponse("User information not found.")



@login_required  # ensure only auth users can access
def generate_certificate(request):
    user = request.user
    user_name = user.first_name + ' ' + user.last_name
    # it retrives only auth users from the request and construct full name

    try:
        # Get the latest ResultModel instance for the user
        result_instance = ResultModel.objects.filter(user=user).order_by('-date').latest('date')
        percent = result_instance.percentage
        level = result_instance.level
        date = result_instance.date.strftime('%Y-%m-%d')  # Format the date as needed
    except ResultModel.DoesNotExist:
        result_instance = None
        percent = 'none'
        level = 'none'
        date = 'N/A'  # Handle the case when the ResultModel does not exist for the user
# retrive latest reusltmodel for user extract the date

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buffer, pagesize=landscape(letter))

    # Set font and size
    c.setFont("Times-Roman", 12)

    # Draw border
    c.setStrokeColorRGB(0, 0.447, 0.847)  # Border color
    c.rect(30, 30, 750, 550)  # Border around the certificate

    # Set styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading1_style = styles["Heading1"]
    body_style = styles["BodyText"]
    italic_style = styles["Italic"]

    # Certificate title
    c.setFont(title_style.fontName, 40)
    c.setFillColorRGB(0, 0.376, 0.663)  # Title color
    c.drawCentredString(415, 500, "Certificate Of Completion")

    # Certificate body
    c.setFillColorRGB(0, 0, 0)
    c.setFont(italic_style.fontName, 22)
    text = "This Certificate is awarded to"
    c.drawCentredString(415, 450, text)

    # User name
    c.setFont(heading1_style.fontName, 40)
    c.setFillColorRGB(0.01, 0.85, 0.56)
    c.drawCentredString(415, 385, user_name)

    # Additional text
    c.setFillColorRGB(0, 0, 0)
    c.setFont(body_style.fontName, 18)
    text = "For his/her completion of Quiz"
    c.drawCentredString(415, 350, text)

    c.setFont(body_style.fontName, 18)
    text = "along with "+str(percent)+"% of percentage for "+ level
    c.drawCentredString(410, 320, text)

    # Add an image
    cert_sign = "static/images/signature.png"
    c.drawInlineImage(cert_sign, 280, 200, width=250, height=80)

    # Additional text
    c.setFont(body_style.fontName, 12)
    c.drawString(374, 190, "Person Name")
    c.drawString(370, 160, "Learning Lead")
    c.drawString(367, 130, "Department Name")

    # Add the current date
    c.setFont(italic_style.fontName, 18)
    text = "Awarded on " + date
    c.drawString(330, 80, text)

    # Save the canvas to the PDF file
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename=f"{user_name}_certificate.pdf")

    # Create an EmailMessage with the certificate as an attachment
    subject = 'Certificate of Completion'
    body = f'Dear {user_name},\n\nCongratulations on completing the Quiz. Please find your certificate attached.\n\nBest regards,\nPrime Intuit'
    from_email = 'kataribhuvana2364@gmail.com'  # Replace with your organization's email
    to_email = [user.email]

    email = EmailMessage(subject, body, from_email, to_email)
    email.attach(f"{user_name}_certificate.pdf", buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send()

    # Optionally, you can render a response to the user
    return redirect('/quiz/certificate')