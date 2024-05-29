## Tools and Technologies used
- Django 
- GitHub
- Bootstrap


## Step 1
  `django-admin startproject book_tracker`
  `cd book_tracker`
  `python manage.py startapp book_app`
  `python manage.py runserver`
  [book_tracker] -> [settings.py] -> lista [INSTALLED_APPS] -> trecem noul app [book_app]


## Step 2
- Cream modelul de baza de date ca sa putem face storage la carti in baza de date [models.py] -> aici ne cream tabelele 
prin a mosteni *models.Model*


## Step 3
- Cream baza de date ruland comenzile `python manage.py makemigrations` si `python manage.py migrate`


## Step 4
  [view]      - Facem un view, definim o functie, in care sa randam homepage-ul.
  [templates] - Cream folderul [templates] -> [base.html] -> [home.html]'
  [url]       - In [urls.py] cream path-ul.

1. In [base.html] definim o sectiune [div.container], in care cine va mosteni base-ul, o sa insereze codul de HTML 
inauntru div-ului. 
2. Codul din home.html va fi practic randat in interiorul acestui div.
3. Pentru a fi posibil acest lucru, in acel div vom folosi `{% block content %}  {% endblock %}`
4. Facem un alt view in care sa afisam ce este in baza de date.
   [view show_books_view] -> [templates: books.html] -> [url 'books/']
 

## Step 5
- Populam baza de date din Shell
  `python manage.py shell`
  `import book_app.models from *`
  `Genre.objects.create(name="Action")`
  `Author.objects.create(first_name="First", last_name="Last")`
  `Book.objects.create(...)`


## Step 6
1. Cream clasa [BookForm] in fisierul [forms.py] creat in prealabil, mostenind *forms.ModelForm* si vom defini 
metoda [clean_title]
2. Cream un nou view [create_book] caruia o sa ii facem un nou template si un nou path.
3. In view-ul [create_book] vom trata cele doua cazuri, cand se face request de tip GET si POST si vom face 
validarea form-ului.
4. In [create_book.html] vom defini un form cu metoda POST, ca la submit sa trimita datele utilizatorului la server.


## Step 7 
  Ne ocupam de Admin Panel de unde putem sa introducem un nou autor.
  [admin.py] -> `admin.site.register(Author)`
  `python manage.py createsuperuser`
  Aici ii dam datele noastre: username, email, password
  Mergem pe [127.0.0.1:8000/admin] - de unde putem introduce nou autor. 


## Many to Many
1. Pentru relatie M2M, Django o sa creeze automat pentru noi o tabela intermediara intre Book si Author.
2. Ca sa referentiem Foreign Key-ul o sa spunem `book.authors.set(form.cleaned_data['author'])` ca sa setam lista de 
autori care ne vine din formular ca fiind autorii acelei carti. 


## Step 8
  Optimizam form-ul din [create_books.html] accesand fiecare field individual si stilizand campurile.
  `{{ form.non_field_errors }}` -> daca noi am facut validare si formularul are niste erori pe el, o sa printeze erorile 
  care nu sunt specifice pentru field-uri 
  `{{ form.title.errors }}` -> specific field-ului title, asa accesam erorile unui field

## Add class to django form field
  In [BookForm] ne redefinim campul de CharField cu niste lucruri custom.
    `title = forms.CharField(
            widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Title'
                }
            )
        )`


## Step 9
  [SEARCH FUNCTIONALITY]
  In navbar avem form-ul de search unde vom face setarile de mai jos:
    - method="get"
    - action="{% url 'books' %}"

  Practic ii spunem sa se duca la pagina 'books' si sa ne aduca rezultatul cautarii.
  Ii definim name-ul='search' si value, valoare pe care o luam dinamic.

1. Implementam logica de search in view, la functia show_books_view.
2. Obiectul care contine toate cartile il vom retine intr-o varibila.
3. Parametrii pe care ii dam cu semnul intrebarii in URL, ei vin pe request.GET, ceea ce imi returneaza un dictionar si 
atunci apelam metoda get() de pe dictionar pasandu-i stringul 'search'
4. Verificam daca search_text-ul nostru exista si daca exista, facem filtrare dupa acesta.
5. Ca sa ne ramana cuvantul pe care il cautam in search, trimitem valoarea din search_text in 
`context={'search_text': search_text}`

## STATIC FILES

- CSS | Scriind books.css, href ul din link ul pe care il adaugam in base.html -> head, fisierul asta o sa se afle pe 
serverul meu cand il deployez. Trebuie sa ii spun cumva serverului sa imi dea fisierul asta.
- Trebuie sa definim in settings.py - STATIC_URL = 'static/' -> lucrul asta e definit automat la crearea proiectului. 
- Practic asta va spune "vezi ca ruta la care o sa se afle fisierele este 'static/' 

1. Cream folderul static unde mutam fisierele statice (in cazul nostru, fisierul books.css)
2. In base.html adaugam:
   Folosim tag ul `{% load static %}`
   `<link rel="stylesheet" href="{% static '../static/books.css' %}">`
    - folosim "functia" / tagname ul STATIC si ii pasam ca ruta un string.
3. In urls.py adaugam urmatoarea sintaxa imediat dupa lista urlpatterns:
   `+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`

4. url-ul '/static/' pune un request la /static/ si dupa aia se serveste fisierul catre care se face request.
5. load-ul include tag-ul STATIC, fara load nu ar merge acest STATIC.


## CONTEXT
- Putem sa trimitem variabile prin context.
- views.py -> functia show_books_view -> context={'context_books': books} - unde [books] reprezinta Book.objects.all()
- Practic trimitem [books]=Book.objects.all() in books.html facand un `for book in context_books`, iar fiecare book va 
reprezenta cate o inregistrare din tabela Book.


## AUTHENTICATION MECHANISM (Registration 'Sign up', Login, Authentication)
PROCESUL AUTENTIFICARII
Partea de autentificare se face la fiecare request.
Daca mergem pe un site si dam un enter, de fiecare data browser ul meu o sa ii trimita la server dovada de autentificare
Datele de autentificare sunt salvate in cookies.
Cand ii zic prima data id ul si parola, el o sa imi returneze un string pe care browser ul o sa il salveze undeva, 
si eu mereu cand o sa dau enter, browserul o sa ii trimita de fiecare data in mod automat serverului meu string ul respectiv

HASH ALGORITHM
In baza de date nu trebuie facut niciodata storage la parola asa cum e ea. Se folosesc anumiti algoritmi de hashing, 
algoritmi care obtin din parola pe care eu o pun un string random f mare dar stringul are o anumita propriateta, si 
anume ca este posibil sa il obtin de fiecare data cu aceiasi cheie. Practic se face incriptie pe baza de date.

Nici macar ownerul unei baze de date nu va stii parola, la autentificare parola se va compara de fiecare data cu stringul 
generat random care a ramas in baza de date.

`python manage.py shell`
`from django.contrib.auth.models import User`
`User`
`user = User.objects.create_user('pahar', password='pahar')`  - asta e modelul de user pe care ni-l da Django
`user.password`
`user.objects.first()`
`Go to db.sqlite3` -> SELECT * FROM auth_user
Mai putem sa dam o parola folosind metoda asta: user.set_password('pahar')


`from django.contrib.auth import authenticate`
authenticate(username='pahar', password='pahar')  -> OUTPUT: <User: pahar> -> daca ne retruneaza un user, inseamna
ca userul s a logat cu succes. 
Daca vreau sa fac autentificare la un user, cand o sa vina pe view-ul meu, practic cand o sa faca un post, si pe 
request.post ul ala o sa imi vina username-ul si parola, o sa folosim tot flow-ul de mai sus.
Adica o sa facem o functie, o sa ii dam un formular la user, formularul o sa aiba un username si o parola,iar la click pe 
SIGN IN o sa faca un post request la view ul nostru si in view ul nostru acest request.post o sa contina username ul si
parola pe dictionarul asta. Astea vor fi valorile din formular.  

O sa avem acces pe obiectul de request pe care il primim mereu in VIEW, o sa avem mereu acces la request.user
Daca mergem si pune intr-un view in care n-am facut nici un fel de autentificare, proprietatea asta request.user tot
exista, numai ca o sa ne returneze obiectul AnonymouseUser.

La cookies sunt generate niste chei care sunt trimise la browser si browserul trimite de fiecare data cheia aia, ca sa nu trebuiasca 
la fiecare reqest sa ii ceri userului - user ul si parola.
Si atunci trebuie sa generam treaba asta, se apeleaza metoda login si Django in spate face tot ce trebuie, deci prin login, 
mereu avem un cookie de sesiune pe care il dam browsrului.
Iar daca apelam metoda logout sterge din memorie stringul hash uit.
E foarte secure sistemul de autentificare a Django ului.

Userul introduce userul si parola, da submit si pe request.post o sa ne vina userul si parola lui.
Trecem prin functia de authenticate, daca ne returneaza un user <User: username> inseamna ca userul s-a logat cu 
succes si atunci trebuie sa ii zicem la server ul nostru pe raspuns sa trimita un cookie catre server.
Apoi cu metoda logout, invalideaza cookie ul de sesiune. 


## LOGIN -> LoginView
Django ne ofera LoginView ready to use 
1. path('accounts/login/', LoginView.as_view(), name='login'),
2. Cream folderul registration in folderul templates, iar aici vom avea login.html in care vom extinde base.html
3. Includem un formular in interiorul paginii login.html, iar LoginView o sa ne trimita un formular `{{ form }}`
4. Pe form trebuie sa punem metoda POST
5. Pasam parametrul `LoginRequiredMixin` view-ului care la care dorim ca utilizatorul sa fie logat inainte de a 
accesa pagina respectiva.
6. La logare, dupa ruta accounts/login trebuie sa avem pagina la care o sa ne faca redirect, iar pentru asta vom pune
localhost/accounts/login/?next=/ - este o functionalitate pe care ne-o da loginView-ul.
Django are un default care dupa logare te trimite la /accounts/profile, iar ca sa nu crape, poti sa ii dai acel next.
7. O alta modalitate pentru redirect putem sa mergem in settings.py si sa ii dam LOGIN_REDIRECT_URL = 'hello'
8. Daca vrem sa vedem daca un user este autentificat folosim `request.user.is_authenticated`. O sa avem AnonymousUser 
daca userul nu este logat.

## LOGOUT -> LogoutView
1. In base.html, navbar, adaugam html ul de mai jos:
    <div class="navbar-nav ml-auto">
      <div class="nav-item dropdown">
        {% if user.is_authenticated %}
          <a class="nav-link active dropdown-toggle" href="#" data-toggle="dropdown">
            {% if user.first_name %}Hello, {{ user.first_name }}!
            {% else %}Hello, {{ user.username }}!{% endif %}
          </a>
          <div class="dropdown-menu dropdown-menu-right">
            <a class="dropdown-item text-right" href="{% url 'logout' %}">Logout</a>
            <a class="dropdown-item text-right" href="{% url 'password_change' %}">Change password</a>
          </div>
        {% else %}
          <a class="nav-link active dropdown-toggle" href="#" data-toggle="dropdown">
            You are not logged in.
          </a>
          <div class="dropdown-menu dropdown-menu-right">
            <a class="dropdown-item text-right" href="{% url 'login' %}">Login</a>
          </div>
        {% endif %}
      </div>
    </div>

2. In urls.py adaugam `path('logout/', LogoutView.as_view(), name='logout')`

## USER - NE PUTEM DEFINI UN USER CUSTOMIZAT
1. punem in `settings.py` numele aplicatiei plus numele clasei pe care o vom folosi pentru userul nou
   si clasa asta trebuie sa mosteneasca din AbstrasctUser - `AUTH_USER_MODEL = 'viewer.User'`
2. Ca sa nu primim eroarea in care ne spune ca aplicatia nu expune modelul de user, in fisierul `admin.py` vom pune
   `admin.site.register(User, UserAdmin)`
3. Vom sterge din folderul migrations toate fisierele, mai putin `__init__.py` si baza de date `db.sqlite3`. 
   Apoi vom face din noi migrarea
4. Cream un nou user:
   from viewer.models import User
   user = User.objects.create_user('madi', password='pahar')

## REGISTRATION -> UserCreationForm
Cream o inregistrare in baza de date cu un anumit user. 
Sign up inseamna cand userul imi trimite niste informatii pe formularul de sign up si eu ii creez o inregistrare in 
baza de date. Si atunci cand incearca sa se logheze, verific in baza de date daca exista inregistrarea 
respectiva. De aceea calsa de SignUpView foloseste CreateView. Nu e ca la LoginView care are un LoginView dedicat. 
La SignUp pur si simplu creezi un user.

1. Facem un CreateView in care vom folosi un formular si ii asignam un template
    class SignUpView(CreateView):
       template_name = 'sign_up.html'
       form_class = SignUpForm
       success_url = reverse_lazy('hello')

2. Django ne ofera formularul - UserCreationForm pe care il definim in forms.py
   class SignUpForm(UserCreationForm):
       class Meta(UserCreationForm.Meta):
           model = User

3. Definim o ruta
    path('sign_up', SignUpView.as_view(), name='sign_up')
