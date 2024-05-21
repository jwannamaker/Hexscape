import pyglet
from pyglet import gl
from pyglet.window import key, mouse


# Allows images to load with their alpha values blended? 
# I definitely need to learn how OpenGL works. (Eventually)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)

main_batch = pyglet.graphics.Batch()


@main_window.event
def on_draw():
    main_window.clear()
    main_batch.draw()

if __name__ == '__main__':
    pyglet.app.run()