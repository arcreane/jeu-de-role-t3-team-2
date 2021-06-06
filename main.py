import tkinter as tk
import Designer
import Player
import Splash
import HB_Utilities


def UserFunctionChoice():
    def answerDesign():
        Designer.launchDesigner()
        root.focus_force()
        return

    def answerPlay():
        Player.launchGamePlayer()
        return

    def answerQuit():
        quit(1)  # 1 is the code that will be return by the application
        return

    root = tk.Tk()
    root.title('HeroBook')

    label1 = tk.Label(master=root, text='Please select function below...')
    btn1 = tk.Button(master=root, width=20, text='Design', command=answerDesign)
    btn2 = tk.Button(master=root, width=20, text='Play', command=answerPlay)
    btn3 = tk.Button(master=root, width=20, text='Quit', command=answerQuit)

    label1.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
    btn1.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
    btn2.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))
    btn3.grid(row=1, column=2, padx=(10, 10), pady=(10, 10))

    root.withdraw()
    HB_Utilities.RemoveTKBorders(root)
    HB_Utilities.CenterTK(root)
    root.withdraw()

    splash = Splash.Splash(root, './images/splashMain.gif', 3)

    root.mainloop()

    return


# This is the main function : while the user don't want to quit : ask him the expected function and launch it ... or quit
if __name__ == '__main__':


    while True:
        UserFunctionChoice()
        # TrySample.main()
