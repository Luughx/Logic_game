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
maxTime = 300
time = 0

#Carga todas las preguntas de los archivos .json
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
    page.scroll = ft.ScrollMode.ALWAYS

    global lives
    textQuestion = Text("",size=20)
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
                    ft.SafeArea(
                        ft.Column(
                            [
                                ft.Text("Game name", size=30, weight=ft.FontWeight.W_600),
                                txtName,
                                Column(
                                    [
                                        ft.ElevatedButton(text=f"Jugar", icon=ft.icons.PLAY_ARROW, on_click=openQuestions),
                                        ft.ElevatedButton(text="Ranking", icon=ft.icons.TABLE_ROWS_OUTLINED, on_click=openRanking),
                                        ft.ElevatedButton(text="¿Cómo jugar?", icon=ft.icons.EDIT_NOTE_SHARP, on_click=openHowToPlay),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=50
                        )
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
                        ft.SafeArea(
                            ft.Container(
                                ft.Column(
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
                            ),
                            expand=True
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
                        ft.SafeArea(
                            Container(
                                ft.ListView(
                                    [
                                        ft.DataTable(
                                            columns=[
                                                ft.DataColumn(Text("#"), numeric=True),
                                                ft.DataColumn(Text("Nombre", text_align=ft.TextAlign.CENTER)),
                                                ft.DataColumn(Text("Tiempo", text_align=ft.TextAlign.CENTER)),
                                                ft.DataColumn(Text("Puntos", text_align=ft.TextAlign.CENTER), numeric=True),
                                                ft.DataColumn(Text("Fecha", text_align=ft.TextAlign.CENTER)),
                                            ],
                                            rows=getRanking(),
                                            expand=True
                                        ),
                                        Container(height=20)
                                    ]
                                    
                                ),
                                padding=30,
                            ),
                            expand=True
                        ),
                        
                    ]
                )
            )

        if page.route == '/how-to-play':
            page.views.append(
                View(
                    '/How-to-play',
                    [
                        AppBar(bgcolor=colors.PRIMARY_CONTAINER, title=Text("Como jugar")),
                        ft.SafeArea(
                            Container(
                                ft.ListView(
                                    [
                                        Text("Como jugar uwu")
                                    ]
                                ),
                                padding=30,
                            ),
                            expand=True
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

    def openHowToPlay(event):
        page.go('/how-to-play')
        page.update()

    # Questions

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

    def getQuestion():
        global current
        global difficult

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

    def getAnswers():
        global current
        global answers

        answers.clear()

        for i, answer in enumerate(current["responses"]):
            answers.append(Text(f"{list(ascii_lowercase)[i]}) {answer}", size=18))

        return answers

    def initializeTime():
        global timeBreaker
        global time
        global maxTime

        time = maxTime
        minutes = 0
        seconds = 0
        firstDefeat = False
        while True:
            if time > -1:
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
                page.update()

    #--------------

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
            if points == 0:
                dialogWrong.content = Text(f"Perdiste, conseguiste {points} puntos, tu resultado no será guardado")
                dialogWrong.actions = [ft.ElevatedButton("Aceptar", on_click=closeDefeat, autofocus=True)]

                page.dialog = dialogWrong
                dialogWrong.open = True
            else:
                dialogWrong.content = Text(f"Perdiste, conseguiste {points} puntos, ¿Deseas guardar tu resultado?")
                dialogWrong.actions = [ft.ElevatedButton("Sí", on_click=saveDataSQL, autofocus=True), ft.ElevatedButton("No", on_click=closeDefeat)]

                page.dialog = dialogWrong
                dialogWrong.open = True

    def openRanking(event):
        try:
            requests.get("https://www.google.com", timeout=3)
        except (requests.ConnectionError, requests.Timeout):
            print("Sin conexión a internet.")
            page.snack_bar = ft.SnackBar(ft.Text(f"No tienes conexión a internet, para ver el ranking es necesario que te conectes a una red", color=colors.ON_PRIMARY_CONTAINER), bgcolor=colors.PRIMARY_CONTAINER, )
            page.snack_bar.open = True
            page.update()
        else:
            print("Con conexión a internet.")
            page.go('/ranking')

    # Alerts

    def closeName(event):
        dialogName.open = False
        page.update()
    
    def closeDefeat(event):
        dialogWrong.open = False
        page.update()
        page.go("/ranking")

    def saveDataSQL(event):
        global time
        global points
        global name
        dialogWrong.open = False
        page.update()
        insertUser(name, points, time)
        page.go("/ranking")

    # Returns
    def getRanking():
        listRanking = []
        users = getUsers()
        for i, user in enumerate(users):
            minutes = int(user[3] / 60)
            seconds = f"0{user[3] - (minutes * 60)}" if user[3] - (minutes * 60) < 10 else user[3] - (minutes * 60)
            listRanking.append(
                    ft.DataRow(
                        cells= [
                            ft.DataCell(Text(f"{i+1}", text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(Text(f"{user[1]}", text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(Text(f"{minutes}:{seconds}", text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(Text(f"{user[2]}", text_align=ft.TextAlign.CENTER)),
                            ft.DataCell(Text(f"{user[4]}", text_align=ft.TextAlign.CENTER))
                        ]
                    )
            )

        listRanking[0].color = colors.SECONDARY_CONTAINER

        return listRanking
        
    def getFields():
        global fieldsQuestion
        global current
        fieldsQuestion.clear()

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