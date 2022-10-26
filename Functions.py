import json
from datetime import date
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
class Task(): #Task is filled with it's name, description and two dates - date of creation and the "deadline". I plan to develop this app to be reminder for exams etc, thats why deadline
    #determines if task is "finished".
    def __init__(self, taskname, taskdescr, taskdate1, taskdate2, isVIP):
        self.taskname = taskname
        self.descr = taskdescr
        self.taskdate1 = taskdate1
        self.taskdate2 = taskdate2
        self.is_VIP = isVIP

class PopupTask(Screen): #This is for Finished Tasks screen, works with popupwindow.
    def __init__(self, name, descr, date, **kwargs):
        super(PopupTask, self).__init__(**kwargs)
        self.ids.name.text = name
        self.ids.descr.text = descr
        self.ids.date.text = date

def update_rect(instance, value): #for popup window, makes it possiible to set canvas pos
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size

def LoginFunction(self): #simple login function, checking input with JSON.File
    file = open('JSON/data_base.JSON')
    data = json.load(file)
    print(data["users"][1])
    for i in range(len(data['users'])):
        print(str(i))
        if self.ids.user.text == data["users"][i]["username"]:
            if self.ids.passw.text == data["users"][i]["password"]:
                self.parent.get_screen('main').ids.loginbutton.text = "Logged as " + str(data["users"][i]["username"])
                self.parent.get_screen('main').currentuser = str(data["users"][i]["username"])
                self.ids.user.text = ''
                self.ids.passw.text = ''
                load_tasks(self)
                return 1
    file.close()
    print("Failed to Log in")
    return 0


def SigninFunction(self): #Sign in function makes addition in JSON file if all the date is written, creates new user
    file = open('JSON/data_base.JSON')
    data = json.load(file)
    if self.ids.name.text == '' or self.ids.user.text == '' or self.ids.passw.text == '' or self.ids.tel.text == '' or self.ids.email.text == '':
        print("One of the fields is not filled!")
        return 0
    elif self.ids.passw.text == self.ids.passw2.text:
        for i in range(len(data['users'])):
            if data["users"][i]["username"] == self.ids.user.text or data["users"][i]["tel"] == self.ids.tel.text or \
                    data["users"][i]["email"] == self.ids.email.text:
                print("Username is already taken or this phone number/email was already registered")
            else:
                data["users"].append(
                    {'no': len(data['users']) + 1, 'name': str(self.ids.name.text), 'username': str(self.ids.user.text),
                     'password': str(self.ids.passw.text),
                     'tel': str(self.ids.tel.text), 'email': str(self.ids.email.text)})
                json_object = json.dumps(data, indent=4)
                with open("JSON/data_base.JSON", "w") as outfile:
                    outfile.write(json_object)
                file.close()
                outfile.close()
                self.parent.get_screen('main').ids.loginbutton.text = "Logged as " + str(data["users"][i]["username"])
                self.parent.get_screen('main').currentuser = str(data["users"][i]["username"])
                self.ids.name.text = ''
                self.ids.user.text = ''
                self.ids.passw.text = ''
                self.ids.tel.text = ''
                self.ids.email.text = ''
                load_tasks(self)
                return 1
    else:
        print("Passwords don't match!")
        return 0


def maketaskdatabase(): #Makes database if there's no Json File with tasks, in case sb copies the project without the file
    # it also helped me to create "empty" Task_data_base with the structure I can easily traverse further in code
    file2 = open('JSON/data_base.JSON')
    data2 = json.load(file2)
    if data2:
        return 0
    else:
        dct = {}
        for i in range(len(data2['users'])):
            dct[data2["users"][i]["username"]] = [{}]
        json_object = json.dumps(dct, indent=4)
        with open("JSON/Task_data_base.JSON", "w") as outfile:
            outfile.write(json_object)
        file2.close()
        outfile.close()
        return 1


def adding_task(self): #Function that makes new task and adds it to the "Database"
    file = open("JSON/Task_data_base.JSON")
    data = json.load(file)
    if self.ids.task_name.text == '' or self.ids.describe.text == '' or self.ids.date.text == '':
        print("One of the fields is not filled!")
        return 0
    else:
        task = Task(self.ids.task_name.text, self.ids.describe.text, str(date.today()), self.ids.date.text,
                    self.ids.importance_check_box.active) #creating an instance of Task Class
        if data[self.parent.get_screen('main').currentuser]:
            taskd = {"no": len(data[self.parent.get_screen('main').currentuser]), "name": task.taskname, #creating a dict with structure used in Task_data_base
                     "descr": task.descr, "date_of_creation": task.taskdate1, "deadline": task.taskdate2,
                     "VIP": task.is_VIP}
            data[self.parent.get_screen('main').currentuser].append(taskd)
            if task.is_VIP == 0: #To make task visible in show_task screen
                label = MDLabel(text=task.taskname)
                label.font_size = 40
                label.font_name = 'fonts/unispace.ttf'
                label.halign = 'center'
                label.padding_y = 15
                label.size_hint = 1, None
                label2 = MDLabel(text=task.descr + "\n Date of creation: " +
                                      task.taskdate1 + "\n Deadline: " + task.taskdate2)
                label2.font_size = 15
                label2.font_name = 'fonts/unispace.ttf'
                label2.halign = 'center'
                label2.padding_y = 15
                label2.size_hint = 1, None
                self.parent.get_screen('show_tasks').ids.NormalTasksCard.add_widget(label)
                self.parent.get_screen('show_tasks').ids.NormalTasksCard.add_widget(label2)
                self.parent.get_screen('main').normaltasks.append(task)
            else:
                label3 = MDLabel(text=task.taskname)
                label3.font_size = 40
                label3.font_name = 'fonts/unispace.ttf'
                label3.halign = 'center'
                label3.padding_y = 15
                label3.size_hint = 1, None
                label4 = MDLabel(text=task.descr + "\n Date of creation: " +
                                      task.taskdate1 + "\n Deadline: " + task.taskdate2)
                label4.font_size = 15
                label4.font_name = 'fonts/unispace.ttf'
                label4.halign = 'center'
                label4.padding_y = 15
                label4.size_hint = 1, None
                self.parent.get_screen('show_tasks').ids.VIPTasksCard.add_widget(label3)
                self.parent.get_screen('show_tasks').ids.VIPTasksCard.add_widget(label4)
                self.parent.get_screen('main').VIPtasks.append(task)
        else: #if there are no tasks coming with the user, I cannot use len(), i just put 0 as this is the first task
            taskd = {"no": 0, "name": task.taskname, "descr": task.descr, "date_of_creation": task.taskdate1,
                     "deadline": task.taskdate2, "VIP": task.is_VIP}
            data[self.parent.get_screen('main').currentuser].append(taskd)
            if task.is_VIP == 0:
                label = MDLabel(text=task.taskname)
                label.font_size = 40
                label.font_name = 'fonts/unispace.ttf'
                label.halign = 'center'
                label.padding_y = 15
                label.size_hint = 1, None
                label2 = MDLabel(text=task.descr + "\n Date of creation: " +
                                      task.taskdate1 + "\n Deadline: " + task.taskdate2)
                label2.font_name = 'fonts/unispace.ttf'
                label2.font_size = 15
                label2.halign = 'center'
                label2.padding_y = 15
                label2.size_hint = 1, None
                self.parent.get_screen('show_tasks').ids.NormalTasksCard.add_widget(label)
                self.parent.get_screen('show_tasks').ids.NormalTasksCard.add_widget(label2)
                self.parent.get_screen('main').normaltasks.append(task)
            else:
                label3 = MDLabel(text=task.taskname)
                label3.font_size = 40
                label3.font_name = 'fonts/unispace.ttf'
                label3.halign = 'center'
                label3.padding_y = 15
                label3.size_hint = 1, None
                label4 = MDLabel(text=task.descr + "\n Date of creation: " +
                                      task.taskdate1 + "\n Deadline: " + task.taskdate2)
                label4.font_size = 15
                label4.font_name = 'fonts/unispace.ttf'
                label4.halign = 'center'
                label4.padding_y = 15
                label4.size_hint = 1, None
                self.parent.get_screen('show_tasks').ids.VIPTasksCard.add_widget(label3)
                self.parent.get_screen('show_tasks').ids.VIPTasksCard.add_widget(label4)
                self.parent.get_screen('main').VIPtasks.append(task)
        json_object = json.dumps(data, indent=4)
        with open("JSON/Task_data_base.JSON", "w") as outfile:
            outfile.write(json_object)
        file.close()
        outfile.close()
        for k in self.parent.get_screen('delete_task').ids.TasksToDelete.children:
            self.parent.get_screen('delete_task').ids.TasksToDelete.clear_widgets()
        self.parent.get_screen('delete_task').addingWidget = 1

        return 1


def load_tasks(self): #load tasks to show_task screen
    file = open("JSON/Task_data_base.JSON")
    data = json.load(file)
    self.parent.get_screen('main').normaltasks = []
    self.parent.get_screen('main').VIPtasks = []
    for i in range(len(data[self.parent.get_screen('main').currentuser])):
        if data[self.parent.get_screen('main').currentuser][i]["VIP"] == 0:
            task = Task(data[self.parent.get_screen('main').currentuser][i]["name"], #creating an instance of Task Class
                        data[self.parent.get_screen('main').currentuser][i]["descr"],
                        data[self.parent.get_screen('main').currentuser][i]["date_of_creation"],
                        data[self.parent.get_screen('main').currentuser][i]["deadline"],
                        data[self.parent.get_screen('main').currentuser][i]["VIP"])
            self.parent.get_screen('main').normaltasks.append(task) #adding task read from json file to the list
        else:
            task = Task(data[self.parent.get_screen('main').currentuser][i]["name"],
                        data[self.parent.get_screen('main').currentuser][i]["descr"],
                        data[self.parent.get_screen('main').currentuser][i]["date_of_creation"],
                        data[self.parent.get_screen('main').currentuser][i]["deadline"],
                        data[self.parent.get_screen('main').currentuser][i]["VIP"])
            self.parent.get_screen('main').VIPtasks.append(task) #adding task read from json file to the list
    for i in self.parent.get_screen('main').normaltasks:
        y = int(i.taskdate2[0:4])
        m = int(i.taskdate2[5:7])
        d = int(i.taskdate2[8:10])
        task_date = date(y, m, d)
        if task_date > date.today(): #if the date of read task (deadline) is below current date it should be only in finished tasks and not here
            label = MDLabel(text=i.taskname)
            label.font_size = 40
            label.font_name = 'fonts/unispace.ttf'
            label.halign = 'center'
            label.padding_y = 15
            label.size_hint = 1, None
            label2 = MDLabel(text=i.descr + "\n Date of creation: " + i.taskdate1 + "\n Deadline: " + i.taskdate2)
            label2.font_size = 15
            label2.font_name = 'fonts/unispace.ttf'
            label2.halign = 'center'
            label2.padding_y = 15
            label2.size_hint = 1, None
            self.parent.get_screen('show_tasks').ids.NormalTasksCard.add_widget(label)
            self.parent.get_screen('show_tasks').ids.NormalTasksCard.add_widget(label2)

    for i in self.parent.get_screen('main').VIPtasks:
        y = int(i.taskdate2[0:4])
        m = int(i.taskdate2[5:7])
        d = int(i.taskdate2[8:10])
        task_date = date(y, m, d)
        if task_date > date.today(): #if the date of read task (deadline) is below current date it should be only in finished tasks and not here
            label3 = MDLabel(text=i.taskname)
            label3.font_size = 40
            label3.font_name = 'fonts/unispace.ttf'
            label3.halign = 'center'
            label3.padding_y = 15
            label3.size_hint = 1, None
            label4 = MDLabel(text=i.descr + "\n Date of creation: " + i.taskdate1 + "\n Deadline: " + i.taskdate2)
            label4.font_size = 15
            label4.font_name = 'fonts/unispace.ttf'
            label4.halign = 'center'
            label4.padding_y = 15
            label4.size_hint = 1, None
            self.parent.get_screen('show_tasks').ids.VIPTasksCard.add_widget(label3)
            self.parent.get_screen('show_tasks').ids.VIPTasksCard.add_widget(label4)

    file.close()


class taskButton(MDRoundFlatButton): #for deleting tasks, I overrided Kivy button class to create new on_press method that calls delete_current() function
    def __init__(self, scr, **kwargs):
        super(MDRoundFlatButton, self).__init__(**kwargs)
        self.font_name = 'fonts/unispace.ttf'
        self.font_size = 30
        self.size_hint = 1, None
        self.height = 0.2 * scr.ids.scroller.height
        self.pos_hint = {"center_x": 0.5}

    def on_press(self, *args):
        super(MDRoundFlatButton, self).on_press(*args)
        self.parent.parent.parent.parent.deletecurrent(self) #so many parents to get to the delete_task screen..

class task2Button(MDRoundFlatButton):#for showing finished tasks with popup windows, for this child of Kivy button I also overrided on_press to create a popup window
    def __init__(self, scr, name, descr, date, **kwargs):
        super(MDRoundFlatButton, self).__init__(**kwargs)
        self.text = name
        self.font_name = 'fonts/unispace.ttf'
        self.font_size = 30
        self.size_hint = 1, None
        self.height = 0.2 * scr.ids.scroller.height
        self.pos_hint = {"center_x": 0.5}
        self.name = name
        self.descr = descr
        self.date = date

    def on_press(self, *args):
        super(MDRoundFlatButton, self).on_press(*args)
        show = PopupTask(self.name, self.descr, self.date)
        popupWindow = Popup(title=self.name, content=show, size_hint=(None, None), size=(1000, 800), separator_color=[.6,.4,.8,1], background_color=[0,0,0,.3])
        popupWindow.open()


def load_delete_tasks(self, inDeleteState, tasksLoaded, addingWidget): #function that loads all tasks as the TaskButtons to the delete_task screen
    if not tasksLoaded or addingWidget: #logic works like that so I can reload tasks whenever one is deleted and to avoid multiplication of tasks at the same time
        normaltasks = MDLabel(text='Tasks with standard importance')
        normaltasks.id = 'nt_title'
        normaltasks.halign = 'center'
        normaltasks.font_name = 'fonts/Bock_Personaluse.otf'
        normaltasks.font_size = 70
        normaltasks.size_hint = 1, None
        normaltasks.height = 0.6 * self.ids.scroller.height
        self.ids.TasksToDelete.add_widget(normaltasks)
    if not tasksLoaded or addingWidget:
        for i in self.parent.get_screen('main').normaltasks:
            task = taskButton(self, text=i.taskname)
            self.ids.TasksToDelete.add_widget(task)
    if not tasksLoaded or addingWidget:
        VIPtasks = MDLabel(text='Tasks with high importance')
        VIPtasks.id = 'vt_title'
        VIPtasks.halign = 'center'
        VIPtasks.font_name = 'fonts/Bock_Personaluse.otf'
        VIPtasks.font_size = 80
        VIPtasks.size_hint = 1, None
        VIPtasks.height = 0.6 * self.ids.scroller.height
        self.ids.TasksToDelete.add_widget(VIPtasks)
    if not tasksLoaded or addingWidget:
        for i in self.parent.get_screen('main').VIPtasks:
            task = taskButton(self, text=i.taskname)
            self.ids.TasksToDelete.add_widget(task)
    if inDeleteState:
        self.inDeleteState = 0
    if addingWidget:
        self.addingWidget = 0

def load_finished_tasks(self): #loads finished tasks as buttons to the finish_task screen
    normaltasks = MDLabel(text='Finished standard tasks')
    normaltasks.id = 'nt_title'
    normaltasks.halign = 'center'
    normaltasks.font_name = 'fonts/Bock_Personaluse.otf'
    normaltasks.font_size = 70
    normaltasks.size_hint = 1, None
    normaltasks.height = 0.6 * self.ids.scroller.height
    self.ids.FinishedTasks.add_widget(normaltasks)
    for i in self.manager.get_screen('main').normaltasks:
        y = int(i.taskdate2[0:4])
        m = int(i.taskdate2[5:7])
        d = int(i.taskdate2[8:10])
        task_date = date(y, m, d)
        if task_date < date.today(): #they should be here only if their dates are below current - so the deadline is passed.
            task = task2Button(self, i.taskname, i.descr, i.taskdate2)
            self.ids.FinishedTasks.add_widget(task)
    VIPtasks = MDLabel(text='Finished high importance tasks')
    VIPtasks.id = 'vt_title'
    VIPtasks.halign = 'center'
    VIPtasks.font_name = 'fonts/Bock_Personaluse.otf'
    VIPtasks.font_size = 80
    VIPtasks.size_hint = 1, None
    VIPtasks.height = 0.6 * self.ids.scroller.height
    self.ids.FinishedTasks.add_widget(VIPtasks)
    for i in self.manager.get_screen('main').VIPtasks:
        y = int(i.taskdate2[0:4])
        m = int(i.taskdate2[5:7])
        d = int(i.taskdate2[8:10])
        task_date = date(y, m, d)
        if task_date < date.today():
            task = task2Button(self, i.taskname, i.descr, i.taskdate2)
            self.ids.FinishedTasks.add_widget(task)


def delete_task(self, task):
    file = open("JSON/Task_data_base.JSON")
    data = json.load(file)
    self.parent.get_screen('show_tasks').ids.NormalTasksCard.clear_widgets() #I reset all visuals to re-create them with new set of tasks after deleting one
    self.parent.get_screen('show_tasks').ids.VIPTasksCard.clear_widgets()
    self.parent.get_screen('delete_task').ids.TasksToDelete.clear_widgets()
    self.parent.get_screen('finish_task').ids.FinishedTasks.clear_widgets()
    for i in data[self.parent.get_screen('main').currentuser]:
        if i['name'] == task.text:
            data[self.parent.get_screen('main').currentuser].remove(i) #removing the task that was pressed
    json_object = json.dumps(data, indent=4)
    with open("JSON/Task_data_base.JSON", "w") as outfile: #updating json file
        outfile.write(json_object)
    file.close()
    outfile.close()
    self.inDeleteState = 1
    load_tasks(self)
    load_delete_tasks(self, self.inDeleteState, 0, 0) #calling for functions to re-load the tasks


