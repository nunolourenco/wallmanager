from pymt import *
from ui.mainwindow import MainWindow
from ui.appslist import AppsList
from ui.appbutton import AppButton
from application import get_all_apps

#######
# UI
#######

main_window = MainWindow(width=800, 
                         height=600)

# Scatter to make AppsList movable
scatter = MTScatterWidget(pos=(150,50),
                          size=(500, 500))

# Construct AppsList looping through all apps
apps_grid = AppsList(pos=(20,20),
                     size=(460,460))

for app in get_all_apps():
    style = {'bg-color': (0, .2, 0, 1), 'draw-background': 1}
    item = AppButton(app,
                           anchor_x='center',
                           anchor_y='middle',
                           halign='center', 
                           valign='middle',
                           style=style,
                           size=(200,200))
    apps_grid.add_widget(item)
    

# Add appsList to Scatter
scatter.add_widget(apps_grid)

# Add Scatter to MainWindow
main_window.add_widget(scatter)

# Execute main loop
if __name__ == '__main__':
    runTouchApp()