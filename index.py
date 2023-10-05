import flet as ft
from time import sleep
from flet import AppBar, ElevatedButton, Page, Text, View, colors, Container, Column, Row
import json
import random
from db import *
from string import ascii_lowercase
import requests

medium_questions = []
easy_questions = []
hard_questions = []
resolves = [[],[],[]]
answers = []
name = ""
difficult = 0
current = {'id': 4, 'description': 'Esta es una pregunta facil 4', 'responses': ['a', 'b', 'c', 'd', 'e'], 'correct': ['a']}
fieldsQuestion = []
maxLives = 3
lives = maxLives
points = 0
timeBreaker = False
maxTime = 10
time = 0

def loadQuestions():
    global medium_questions
    global easy_questions
    global hard_questions
    with open("./questions/easy_questions.json", "r", encoding="utf-8") as file:
        easy_questions = json.load(file)
    with open("./questions/medium_questions.json", "r", encoding="utf-8") as file:
        medium_questions = json.load(file)
    with open("./questions/hard_questions.json", "r", encoding="utf-8") as file:
        hard_questions = json.load(file)

def main(page: Page):
    page.title = 'Logic Game'
    global lives
    textQuestion = Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ac lectus a risus fringilla tempor. Aliquam malesuada dictum arcu at bibendum. Fusce congue blandit semper. Pellentesque eleifend et mi a imperdiet. Sed suscipit facilisis odio, a mollis ante laoreet at. Curabitur imperdiet rhoncus nisi, vitae lacinia est luctus id. Mauris justo ex, lobortis ut turpis nec, luctus rutrum metus.",size=20)
    textTime = Text("7:30", size=20)
    iconTime = ft.Icon(ft.icons.ACCESS_TIME)
    textPoints = Text(f"{points} puntos", size=20)
    textlives = Text(f"{lives} vidas", size=20)
    txtName = ft.TextField(label="Nombre", text_align=ft.TextAlign.CENTER, width=300, max_length=20, border_color=colors.SECONDARY, autofocus=True)
    dialogName = ft.AlertDialog(title=Text("Nombre"), content=Text("El campo de nombre no puede estar vacio"))
    dialogWrong = ft.AlertDialog(title=Text("Perdiste"), modal=True)

    def route_change(event):
        global lives
        global points
        global timeBreaker
        global colorAppBar
        global resolves
        global difficult

        print('Ruta cambiada:', event.route)
        page.views.clear()
        lives = maxLives
        difficult = 0
        points = 0
        resolves = [[],[],[]]
        textPoints.value = f"{points} puntos"
        timeBreaker = True
        txtName.value = ""

        txtName.on_submit = buttonPlay
        
        page.views.append(
            View(
                '/',
                [
                    ft.Column(
                            [
                                ft.Text("Game name", size=30, weight=ft.FontWeight.W_600),
                                txtName,
                                Column(
                                    [
                                        ft.ElevatedButton(text=f"Jugar", icon=ft.icons.PLAY_ARROW, on_click=openQuestions),
                                        ft.ElevatedButton(text="Ranking", icon=ft.icons.TABLE_ROWS_OUTLINED, on_click=openRanking),
                                        ft.ElevatedButton(text="¿Cómo jugar?", icon=ft.icons.EDIT_NOTE_SHARP),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=50
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        if page.route == '/questions':
            page.views.append(
                View(
                    '/questions',
                    [
                        AppBar(
                            actions= [
                                Container(
                                    Row([
                                        #ft.Icon(ft.icons.FAVORITE, size=17),
                                        textlives
                                    ]),
                                    padding=ft.padding.only(left=30,right=30),
                                ),
                                Container(
                                    textPoints,
                                    padding=ft.padding.only(left=30,right=30),
                                ),
                                Container(
                                    Row([
                                        iconTime,
                                        textTime,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    padding=ft.padding.only(left=30,right=30),
                                ),
                            ],
                            bgcolor=colors.PRIMARY_CONTAINER
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    Container(
                                        Column([
                                            textQuestion,
                                            Column(getAnswers())
                                        ]),
                                        padding=ft.padding.only(left=40, right=40)
                                    ),
                                    ft.Row(
                                        getFields(),
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        wrap=True
                                    ),
                                    ft.Row(
                                        [
                                            ElevatedButton(
                                                "Siguiente",
                                                on_click=nextQuestion,
                                                icon=ft.icons.NAVIGATE_NEXT
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    ),
                                ],
                                spacing=50,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            padding=60
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.SPACE_EVENLY
                )
            )
        
        if page.route == '/ranking':
            page.views.append(
                View(
                    '/ranking',
                    [
                        AppBar(bgcolor=colors.PRIMARY_CONTAINER),
                        Container(
                            Column(
                                [
                                    Row(
                                        [
                                            Text(" "),
                                            Text("Nombre", text_align=ft.TextAlign.CENTER),
                                            Text("Tiempo", text_align=ft.TextAlign.CENTER),
                                            Text("Puntos", text_align=ft.TextAlign.CENTER),
                                            Text("Fecha", text_align=ft.TextAlign.CENTER),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                    ),
                                    Container(height=15),
                                    getRanking()
                                ]
                            ),
                            padding=30,
                        ),
                        
                    ]
                )
            )
        
        page.update()

    def view_pop(event):
        print('View pop:', event.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def buttonPlay(event):
        openQuestions(event)

    def openQuestions(event):
        global current
        global timeBreaker
        global name

        if len(txtName.value) != 0:
            name = txtName.value
            loadQuestions()
            getQuestion()
            page.go('/questions')
            timeBreaker = False
            initializeTime()
        else:
            dialogName.actions = [ft.ElevatedButton("Aceptar", on_click=closeName, autofocus=True)]
            page.dialog = dialogName
            dialogName.open = True
            page.update()
    
    def initializeTime():
        global timeBreaker
        global time
        global maxTime

        time = maxTime
        minutes = 0
        seconds = 0
        firstDefeat = False
        while True:
            minutes = int(time / 60)
            seconds = f"0{time - (minutes * 60)}" if time - (minutes * 60) < 10 else time - (minutes * 60)
            textTime.value = f"{minutes}:{seconds}"
            page.update()
            if timeBreaker:
                break
            sleep(1)
            if timeBreaker:
                break
            time -= 1
            if time < 60:
                iconTime.color = colors.ON_ERROR_CONTAINER
                textTime.color = colors.ON_ERROR_CONTAINER
            if time <= 0 and not firstDefeat:
                firstDefeat = True
                defeat()

    def closeName(event):
        dialogName.open = False
        page.update()

    def nextQuestion(event):
        global fieldsQuestion
        global current
        global lives
        global points
        correct = True
        for i in range(len(current["correct"])):
            if current["correct"][i] != fieldsQuestion[i].value.lower():
                correct = False

        if correct:
            points += current['points']
            textPoints.value = f"{points} puntos"

            page.snack_bar = ft.SnackBar(ft.Text(f"Tu respuesta fue correcta, ganaste {current['points']} puntos", color=colors.ON_PRIMARY_CONTAINER), bgcolor=colors.PRIMARY_CONTAINER, )
            page.snack_bar.open = True

            if difficult == 0:
                resolves[0].append(current["id"])
            if difficult == 1:
                resolves[1].append(current["id"])
            if difficult == 2:
                resolves[2].append(current["id"])  
            getQuestion()
            getAnswers()
            getFields()
        else:
            lives -= 1
            print("te salio mal :c")

            if lives > 0:
                textlives.value = f"{lives} vidas"
                page.snack_bar = ft.SnackBar(ft.Text(f"Tu respuesta fue incorrecta, te quedan {lives} vidas", color=colors.ON_ERROR_CONTAINER), bgcolor=colors.ERROR_CONTAINER, )
                page.snack_bar.open = True
                fieldsQuestion[0].autofocus = True
            else:
                defeat()
        page.update()

    def defeat():
        try:
            requests.get("https://www.google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            print("Sin conexión a internet.")
            dialogWrong.title = Text("Sin conexión")
            dialogWrong.content = Text(f"Conseguiste {points} puntos, tu resultado no se guardará por falta de conexión a internet")
            dialogWrong.actions = [ft.ElevatedButton("Aceptar", saveDataSQL, autofocus=True)]
            page.go("/")
            page.dialog = dialogWrong
            dialogWrong.open = True
        else:
            print("Con conexión a internet.")
            dialogWrong.content = Text(f"Perdiste, conseguiste {points} puntos, ¿Deseas guardar tu resultado?")
            dialogWrong.actions = [ft.ElevatedButton("Sí", on_click=saveDataSQL, autofocus=True), ft.ElevatedButton("No", on_click=closeDefeat)]

            page.dialog = dialogWrong
            dialogWrong.open = True
    
    def closeDefeat(event):
        dialogWrong.open = False
        page.update()
        page.go("/ranking")

    def getAnswers():
        global current
        global answers

        answers.clear()

        for i, answer in enumerate(current["responses"]):
            answers.append(Text(f"{list(ascii_lowercase)[i]}) {answer}", size=15))

        return answers

    def saveDataSQL(event):
        global time
        global points
        global name

        print("entra")
        dialogWrong.open = False
        page.update()
        print("Cierra")
        insertUser(name, points, time)
        print("guarda")
        page.go("/ranking")
   
    def getQuestion():
        global current
        global difficult

        print(difficult)
        print(resolves)

        if difficult == 0:
            if len(easy_questions) <= len(resolves[0]):
                difficult = 1
            else:
                current = random.choice(easy_questions)
                while current["id"] in resolves[0]:
                    current = random.choice(easy_questions)

        if difficult == 1:
            if len(medium_questions) <= len(resolves[1]):
                difficult = 2
            else:
                current = random.choice(medium_questions)
                while current["id"] in resolves[1]:
                    current = random.choice(medium_questions)

        if difficult == 2:
            if len(hard_questions) <= len(resolves[2]):
                page.go('/ranking')
            else: 
                current = random.choice(hard_questions)
                while current["id"] in resolves[2]:
                    current = random.choice(hard_questions)

        textQuestion.value = current["description"]

    def openRanking(event):
        try:
            requests.get("https://www.google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            print("Sin conexión a internet.")
            page.snack_bar = ft.SnackBar(ft.Text(f"No tienes conexión a internet, para ver el ranking es necesario que te conectes a una red", color=colors.ON_PRIMARY_CONTAINER), bgcolor=colors.PRIMARY_CONTAINER, )
            page.snack_bar.open = True
            page.update()
        else:
            print("Con conexión a internet.")
            page.go('/ranking')

    def getRanking():
        listRanking = ft.ListView(spacing=30, height=600)
        users = getUsers()
        for i, user in enumerate(users):
            minutes = int(user[3] / 60)
            seconds = f"0{user[3] - (minutes * 60)}" if user[3] - (minutes * 60) < 10 else user[3] - (minutes * 60)
            listRanking.controls.append(
                Container(
                    Row(
                        [
                            Text(f"{i+1}", text_align=ft.TextAlign.CENTER),
                            Text(f"{user[1]}", text_align=ft.TextAlign.CENTER),
                            Text(f"{minutes}:{seconds}", text_align=ft.TextAlign.CENTER),
                            Text(f"{user[2]}", text_align=ft.TextAlign.CENTER),
                            Text(f"{user[4]}", text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                )
            )
            
        return listRanking

    def changeField(event):
        #event.control.value
        alphabet = list(ascii_lowercase)
        if len(event.control.value) == 1:
            indice = alphabet.index(event.control.value)
            answers[indice].weight = ft.FontWeight.W_600
        
    def getFields():
        global fieldsQuestion
        global current
        fieldsQuestion.clear()
        #print(f"Get fields: {current}")
        for i in range(len(current["correct"])):
            if len(current["correct"]) == 1:
                txtField = ft.TextField(text_align=ft.TextAlign.CENTER, width=120, value="", label="Respuesta", border_color=colors.SECONDARY)
                txtField.on_submit = nextQuestion
                txtField.autofocus = True
                fieldsQuestion.append(txtField)
            else:
                if i == 0:
                    txtField.autofocus = True
                txtField =ft.TextField(text_align=ft.TextAlign.CENTER, width=120, value="", label=f"Posición {i}", border_color=colors.SECONDARY)
                txtField.on_submit = nextQuestion
                fieldsQuestion.append(txtField)

        return fieldsQuestion
    
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER)