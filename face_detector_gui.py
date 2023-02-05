import dearpygui.dearpygui as dpg #pip install dearpygui
import cv2 #pip install opencv-python
import os

face_features = cv2.CascadeClassifier("features/frontal_face_haarcascade.xml")
selected_folder = None
drawed = []
results = []

width1, height1, channels1, data1 = dpg.load_image("dory.jpg")
width2, height2, channels2, data2 = dpg.load_image("sishik.jpg")
def_width, def_height, def_channels, def_data = dpg.load_image("default.jpg")


dpg.create_context()

def callback(sender, data): #OK button
    global selected_folder
    selected_folder = data['current_path']
    dpg.set_value("selected_folder", ("Selected path: " + selected_folder))

def button_click(sender, data):
    global selected_folder, updater, results
    if(selected_folder != None):
        files = []
        results = [] #file paths of recognised images with faces
        for image in os.listdir(selected_folder):
            if(image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".bmp")):
                files.append((cv2.imread(selected_folder + '/' + image), selected_folder + '/' + image)) #firt is image and second is path     

        global drawed 
        drawed = []       
        for i in files:
            temp_faces = [] #list to hold how many faces was found
            resized = cv2.resize(i[0], (960, 554), cv2.INTER_AREA)
            grayscaled = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            temp_faces = face_features.detectMultiScale(grayscaled, 1.6)
            for (x, y, w, h) in temp_faces:
                cv2.rectangle(resized, (x, y), (x+w, y+h), (0, 0 , 255), 2)             
            if len(temp_faces) > 0:           
                drawed.append(resized)
                results.append(i[1])
        if len(results) > 0:   
            #show happy sishik image                  
            dpg.set_value("img", data2)
            dpg.set_value("status", "\t\t\t\tYay!\nAn experienced detective worked well and found all these people on the photos:")
        else: 
            #show sad dori image  
            dpg.set_value("img", data1)
            dpg.set_value("status", "\t\t\t\tOops...\nDory couldn`t recognize any people on the photos(")
        dpg.configure_item("result", items=results)
          

with dpg.texture_registry(show=False):
    dpg.add_dynamic_texture(width=width2, height=height2, default_value = def_data, tag="img") 


def myfunc(sender):
    index = results.index(dpg.get_value(sender))
    cv2.imshow(f"{dpg.get_value(sender)}", drawed[index])
    cv2.waitKey(0)     

dpg.add_file_dialog(
    directory_selector=True, height=300, width=600, show=False, callback=callback, tag="file_dialog_id")

with dpg.theme() as new_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (238,136,204,255)) #(r,g,b,a) pink
        dpg.add_theme_color(dpg.mvThemeCol_Text, (21,21,21,255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (223,223,223,255))
        dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (223,223,223,255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (223,223,223,255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (141,249,217,255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (141,249,217,255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (141,249,217,255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (249,141,174,255))
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (254,178,201,255))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (254,178,201,255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

with dpg.window(label="FaceFounder", width=800, height=450, tag="primary"):
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text(tag="selected_folder", default_value="Selected path: None")
    dpg.add_image(texture_tag="img", width=80, height=80)
    dpg.add_text(tag="status")
    dpg.add_button(label="Find faces", callback=button_click)
    dpg.add_listbox(tag="result", callback=myfunc,  num_items=5)

dpg.bind_theme(new_theme)

dpg.create_viewport(title='Window1', height=450, width=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary", True)
dpg.start_dearpygui()
dpg.destroy_context()