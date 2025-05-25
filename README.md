Нашият проект е улеснена версия на електронен дневник. За да бъде стартиран проекта трябва да се навигира до директорията на първата папка \GradePro, при което да бъде написана командата - python manage.py runserver и ако се сблъскате с проблем направете следното:
Get-ChildItem -Recurse -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" -and $_.FullName -like "*\migrations\*" } | Remove-Item
, последвана от -
Get-ChildItem -Recurse -Filter "*.pyc" | Where-Object { $_.FullName -like "*\migrations\*" } | Remove-Item

в power shell за изтриване на миграциите и python manage.py makemigrations и python manage.py migrate за създаване на новите и после пак python manage.py runserver

Венцислав Желев е направил следните html страници - login.html, register.html, create_class.html, base.html
Константин Митов е направил - hero.html, profile.html, about_us.html
Кирил Елисеев е създал следните страници - home.html, view_classes.html

Backend-а е и от тримата и е възможно най-прост и минимален.
Всеки от нас има по поне 2 page-а и js файла и всеки page си има css файл със съответващо име в папките с заглавие static.