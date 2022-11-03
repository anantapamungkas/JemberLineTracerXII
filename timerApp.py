import time 
import threading
import tkinter as tk
import pygame
from tkinter import CENTER, Label, PhotoImage, ttk
from tkVideoPlayer import TkinterVideo

pygame.mixer.init()

class Timer:
    def __init__(self) -> None:

        # define window object
        self.root = tk.Tk()

        self.width, self.height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.width, self.height))
        self.root.title('Jember Line Tracer XII')
        self.root.iconbitmap("assets\images\LOGO FIX.ico")

        # set background image
        self.bg = PhotoImage(file="assets\images\Background.png")
        self.myLabel = Label(self.root, image=self.bg)
        self.myLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # ttk style
        self.s = ttk.Style()
        self.s.layout("TNotebook.Tab", [])
        self.s.configure("TNotebook.Tab", font=("Fira Sans", 12))
        self.s.configure("TButton", font=("Fira Sans", 12))
        self.s.configure("TButton", font=("Fira Sans", 12))


        # ttk tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.place(relx=0.5, rely=0.5, anchor=CENTER)

        # create tabs
        self.tab1 = ttk.Frame(self.tabs, height=220, width=550)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.videoplayer = TkinterVideo(master=self.tab3, scaled=True)    

        # four minutes timer tabs
        self.play_time_timer_label = ttk.Label(self.tab1, text="04:00", fon="Technology", font=("Technology", 200))
        self.play_time_timer_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.preparation_timer_label = ttk.Label(self.tab2, text="4:00", fon="Technology", font=("Technology", 200))
        self.preparation_timer_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.tabs.add(self.tab1, text="Preparation Time")
        self.tabs.add(self.tab2, text="Play Time")
        self.tabs.add(self.tab3, text="Countdown")


        # ttk grid layout
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.place(relx=0.5, rely=0.71, anchor=CENTER)
        
        # create button
        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=1, column=0)

        self.skip_button = ttk.Button(self.grid_layout, text="Stop", command=self.stop_clock)
        self.skip_button.grid(row=1, column=1)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=1, column=2)


        # default timer mode
        self.skipped = False
        self.stopped = False

        self.root.mainloop()

    # start thread
    def start_timer_thread(self):
        t = threading.Thread(target=self.start_timer)
        t.start()
        
    # start timer
    def start_timer(self): 
        self.stopped = False
        self.skipped = False
        self.root.attributes('-fullscreen', True)

        # get timer_id when selecting specific ttk tabs
        timer_id = self.tabs.index(self.tabs.select()) + 1

        # when timer id equals to 1, start two minutes countdown
        if timer_id == 1:
            # palce tabs at the center and remove background for tab 3
            self.tab3.config(width=0, height=0)
            self.tabs.place(relx=0.5, rely=0.5, anchor=CENTER)

            # set 2 minutes timer
            full_seconds = 0

            # play preparation music
            # pygame.mixer.music.load("assets/sounds/battle-sakmenit.mp3")
            # pygame.mixer.music.play(loops=0)

            while full_seconds > -1 and not self.stopped:
                
                # timer logic
                # save minutes and second value using divmod
                # change text label every second with configure function and updating display every second
                minutes, seconds = divmod(full_seconds, 60)
                self.play_time_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            
            # after exiting loop, select other tabs, and rechecking timer id
            if not self.stopped or self.skipped:
                self.tabs.select(2)
                self.start_timer()

        # when timer id equals to 3, start 4 minutes count up
        elif timer_id == 2:
            # place tabs at the center of the screen and place button after the main text
            self.tabs.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.grid_layout.place(relx=0.5, rely=0.71, anchor=CENTER)

            full_seconds = 0

            # play playtime music


            while full_seconds < 60*4+1 and not self.stopped:

                # when timer reach 0s, play gong
                if full_seconds == 0:
                    pygame.mixer.music.load("assets\sounds\gong.mp3")
                    pygame.mixer.music.play()

                # when timer reach 3m 50s, play stop countdown music 
                if full_seconds == 230:
                    pygame.mixer.music.load("assets\sounds\stop.mp3")
                    pygame.mixer.music.play()

                if full_seconds == 60*4:
                    pygame.mixer.music.load("assets\sounds\peluit.mp3")
                    pygame.mixer.music.play()
 
                # timer logic
                # save minutes and second value using divmod
                # change text label every second with configure function and updating display every second
                minutes, seconds = divmod(full_seconds, 60)
                self.preparation_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds += 1

        elif timer_id == 3:
            # full screen video and remove button
            self.tabs.pack(fill="both", expand=True, padx=0, pady=0)
            self.grid_layout.place(relx=0, rely=2, anchor=CENTER)

            full_seconds = 0
            
            # play video for 6s and start countdown at 3s
            while full_seconds < 6 and not self.stopped:
                if full_seconds == 0:
                    self.videoplayer.load(r"assets\videos\20221030-080015-618.MP4")
                    self.videoplayer.pack(expand=True, fill="both")
                    self.videoplayer.play()

                if full_seconds == 3:
                    pygame.mixer.music.load("assets/sounds/3sekon.mp3")
                    pygame.mixer.music.play(loops=0)

                time.sleep(1)
                full_seconds += 1

            # after exiting loop, select other tabs, and rechecking timer id
            if not self.stopped or self.skipped:
                self.tabs.select(1)
                self.start_timer()

        else: 
            print("Invalid Timer ID")

    def reset_clock(self):
        self.root.attributes('-fullscreen', False)
        self.stopped = True
        self.skipped = False
        self.play_time_timer_label.config(text="00:00")
        self.preparation_timer_label.config(text="02:00")
        pygame.mixer.music.stop();
        self.tabs.select(0)

    def stop_clock(self):
        self.stopped = True
        pygame.mixer.music.stop();

Timer()