import os


basedir = os.path.abspath(os.path.dirname(__file__))
fig_path = os.path.join(basedir, 'static', 'images')


def gc_fig_clearance():
    for images in os.listdir(fig_path): #очищаем папку
        os.remove(os.path.join(fig_path, images))
