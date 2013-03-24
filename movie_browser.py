#!/usr/bin/python3
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import os

class movieBrowser:

    config_file = ''
    movie_directory = ''
    movie_list = ''
    size = 20
    filtered_movie_list = []
    frame = Frame
    load_button = Button
    #stop_button = Button
    moviebox = Listbox

    def __init__(self,master):
        frame = Frame(master)
        frame.pack()
        Label(frame, text='Video Browser', font=("Helvetica", 16)).grid(row=0, column=0)
        self.moviebox = Listbox(frame, height=self.size, width=50, selectmode=BROWSE)

        # get the movies
        try:
            # call the get_movies function which inits movie_list
            self.get_movies()
            # loop through each movie
            for movie in self.movie_list:
                # remove text and script files
                fileName, fileExtension = os.path.splitext(movie)
                if (fileExtension == ".mp4") or (fileExtension == ".mkv") or (fileExtension == ".avi"):
                    videoFile = fileName + fileExtension
                    # record the filtered list of movies
                    self.filtered_movie_list.append(videoFile)
                    self.moviebox.insert(END, videoFile)

        except  Exception as problem:
            print('Error Running: ' + str(problem))

        self.moviebox.grid(row=1, column=0)

        # set up load button
        self.load_button = Button(frame, text='Load',font=("Helvetica", 12))
        self.load_button.grid(row=self.size+1, column=0)
        self.load_button.bind("<Button-1>", self.play)

        # Need to add multi thread
        # set up load button
        #self.stop_button = Button(frame, text='Stop',font=("Helvetica", 12))
        #self.stop_button.grid(row=self.size+2, column=0)
        #self.stop_button.bind("<Button-1>", self.stop)

    # play selected video
    def play(self, event):
        selected_video = list(self.moviebox.curselection())
        print('Loading: '+str(self.filtered_movie_list[int(selected_video[0])]))
        try:
            os.system('omxplayer -o hdmi '+str(self.filtered_movie_list[int(selected_video[0])]))
        except Exception as error:
            print(str(error))

    # stop playing video
    def stop(self, event):
        os.system('pkill omxplayer')

    def get_movies(self):
        try:
            self.config_file = self.get_directory()
            # change to video dir
            os.chdir(self.config_file)
            # get list of files in dir
            self.movie_list = os.listdir(os.getcwd())

        except IOError as e:
            print(str(e))

    def get_directory(self):
        try:
            dir_list = os.path.realpath(__file__).split('movie_browser.py')
            file = open(dir_list[0]+'config.txt','r')
            parse_file = True
            movie_list = []

            while (parse_file):
                textFile_data = file.readline().rstrip()
                if textFile_data == '':
                    parse_file = False
                else:
                    parse_file = True
                    movie_list.append(textFile_data)

            if any("dir" in s for s in movie_list):
                dir = movie_list[0].split('=')
                dir = dir[1].replace("'", "")
                return dir
            else:
                return ''
        except IOError:
            return  'No Config file or Option dir not in your config file'

# set up and run program
root = Tk()
# set window title
root.wm_title('Video Browser')
# set window size
root.geometry('450x425')
# init browser class
mb = movieBrowser(root)
# start mail loop
root.mainloop()