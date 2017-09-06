import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pynfb.protocols.psycho.cross_present import PsyExperiment
import os
import numpy as np
import time
import mne
from matplotlib import cm
from matplotlib import colors as mcolors


class ProtocolWidget(pg.PlotWidget):
    def __init__(self, **kwargs):
        super(ProtocolWidget, self).__init__(**kwargs)
        self.dimensionality = 2
        width = 5
        self.setYRange(-width, width)
        self.setXRange(-width, width)
        size = 500
        self.setMaximumWidth(size)
        self.setMaximumHeight(size)
        self.setMinimumWidth(size)
        self.setMinimumHeight(size)
        self.hideAxis('bottom')
        self.hideAxis('left')
        self.setBackgroundBrush(pg.mkBrush('#252120'))
        self.reward_str = '<font size="4" color="#B48375">Reward: </font><font size="5" color="#91C7A9">{}</font>'
        self.reward = pg.TextItem(html=self.reward_str.format(0))
        self.reward.setPos(-4.7, 4.7)
        self.reward.setTextWidth(300)
        self.addItem(self.reward)
        self.clear_all()

    def clear_all(self):
        for item in self.items():
            self.removeItem(item)
        self.addItem(self.reward)

    def update_reward(self, reward):
        self.reward.setHtml(self.reward_str.format(reward))

    def show_reward(self, flag):
        if flag:
            self.reward.show()
        else:
            self.reward.hide()

class ProtocolWidget3D(gl.GLViewWidget):
    def __init__(self, **kwargs):
        super(ProtocolWidget3D, self).__init__(**kwargs)
        self.dimensionality = 3
        self.reward = None
        self.clear_all()

    def clear_all(self):
        for item in self.items:
            self.removeItem(item)
        # self.addItem(self.reward)

    def update_reward(self, reward):
        self.reward.setHtml(self.reward_str.format(reward))

    def show_reward(self, flag):
        pass

class Painter3D:
    def __init__(self, show_reward=False):
        self.show_reward = show_reward

    def prepare_widget(self, widget):
        if widget.dimensionality != 3:
            layout = widget.parent().layout()
            layout.removeWidget(widget)
            widget = ProtocolWidget3D()
            layout.addWidget(widget)
        widget.show_reward(self.show_reward)
        return widget


class Painter:
    def __init__(self, show_reward=False):
        self.show_reward = show_reward

    def prepare_widget(self, widget):
        if widget.dimensionality != 2:
            layout = widget.parent().layout()
            layout.removeWidget(widget)
            widget = ProtocolWidget()
            layout.addWidget(widget)
        widget.show_reward(self.show_reward)
        return widget


class CircleFeedbackProtocolWidgetPainter(Painter):
    def __init__(self, noise_scaler=2, show_reward=False, radius = 3, circle_border=0, m_threshold=1):
        super(CircleFeedbackProtocolWidgetPainter, self).__init__(show_reward=show_reward)
        self.noise_scaler = noise_scaler
        self.x = np.linspace(-np.pi/2, np.pi/2, 100)
        np.random.seed(42)
        self.noise = np.sin(15*self.x)*0.5-0.5 if not circle_border else np.random.uniform(-0.5, 0.5, 100)-0.5
        self.widget = None
        self.radius = radius
        self.m_threshold = m_threshold

    def prepare_widget(self, widget):
        widget = super(CircleFeedbackProtocolWidgetPainter, self).prepare_widget(widget)
        self.p1 = widget.plot(np.sin(self.x), np.cos(self.x), pen=pg.mkPen(229, 223, 213)).curve
        self.p2 = widget.plot(np.sin(self.x), -np.cos(self.x), pen=pg.mkPen(229, 223, 213)).curve
        fill = pg.FillBetweenItem(self.p1, self.p2, brush=(229, 223, 213, 25))
        self.fill = fill
        widget.addItem(fill)

    def set_red_state(self, flag):
        if flag:
            self.p1.setPen(pg.mkPen(176, 35, 48))
            self.p2.setPen(pg.mkPen(176, 35, 48))
            self.fill.setBrush(176, 35, 48, 25)
        else:
            self.p1.setPen(pg.mkPen(229, 223, 213))
            self.p2.setPen(pg.mkPen(229, 223, 213))
            self.fill.setBrush(229, 223, 213, 25)

    def redraw_state(self, sample, m_sample, chunk):
        if m_sample is not None:
            self.set_red_state(m_sample > self.m_threshold)
        if np.ndim(sample)>0:
            sample = np.sum(sample)
        noise_ampl = -np.tanh(sample + self.noise_scaler) + 1
        noise = self.noise*noise_ampl
        self.p1.setData(self.radius * np.sin(self.x)*(1+noise), self.radius * np.cos(self.x)*(1+noise))
        self.p2.setData(self.radius * np.sin(self.x)*(1+noise), -self.radius * np.cos(self.x)*(1+noise))
        pass

class SourceSpaceProtocolWidgetPainter(Painter3D):
    def __init__(self, protocol, show_reward=False):
        super(SourceSpaceProtocolWidgetPainter, self).__init__(show_reward=show_reward)
        self.protocol = protocol
        self.chunk_to_sources = protocol.chunk_to_sources

        self.cortex_mesh_data = None
        self.vertex_idx = None
        self.cortex_mesh_item = None

        self.colormap = cm.viridis

    def prepare_widget(self, widget):
        widget = super(SourceSpaceProtocolWidgetPainter, self).prepare_widget(widget)

        self.cortex_mesh_data = self.protocol.mesh_data
        self.vertex_idx = self.protocol.vertex_idx

        # We will only be assigning colors to a subset of vertexes used for forward/inverse modelling. First, we need to
        # assign an initial color to all the vertices.
        total_vertex_cnt = self.cortex_mesh_data.vertexes().shape[0]
        initial_color = self.colormap(0.5)
        initial_colors = np.tile(initial_color, (total_vertex_cnt, 1))
        self.cortex_mesh_data.setVertexColors(initial_colors)

        # Set the camera at twice the size of the mesh along the widest dimension
        max_ptp = max(np.ptp(self.cortex_mesh_data.vertexes(), axis=0))
        widget.setCameraPosition(distance=2*max_ptp)

        self.cortex_mesh_item = gl.GLMeshItem(meshdata=self.cortex_mesh_data)
        widget.addItem(self.cortex_mesh_item)

        print('Widget prepared')

    def set_red_state(self, flag):
        if flag:
            pass
        else:
            pass

    def redraw_state(self, sample, m_sample, chunk):
        sources = self.chunk_to_sources(chunk)
        sources_normalized = self.normalize_to_01(sources)
        colors = self.colormap(sources_normalized)
        self.update_mesh_colors(colors)

    def update_mesh_colors(self, colors):
        # using cortex_mesh_data.setVertexColors() is much slower, bc we are coloring only a subset of vertices
        self.cortex_mesh_data._vertexColors[self.vertex_idx] = colors
        self.cortex_mesh_data._vertexColorsIndexedByFaces = None
        self.cortex_mesh_item.meshDataChanged()

    @staticmethod
    def normalize_to_01(values):
        vmin = np.min(values)
        vmax = np.max(values)
        return (values - vmin) / vmax


class PsyProtocolWidgetPainter(Painter):
    def __init__(self, detection=False):
        print('DETECTION', detection)
        self.detection = detection
        super(PsyProtocolWidgetPainter, self).__init__()
        print('inited')
        self.t_start_trial = 0

    def prepare_widget(self, widget):
        self.exp = PsyExperiment(widget, detection_task=self.detection)
        #self.exp.run()
        print('prepared')

    def redraw_state(self, sample, m_sample, chunk):
        stimulus_presented = self.exp.run_trial(sample)
        if stimulus_presented:
            print('STIMULUS PRESENTED')
        return stimulus_presented

    def close(self):
        pass


class BaselineProtocolWidgetPainter(Painter):
    def __init__(self, text='Relax', show_reward=False):
        super(BaselineProtocolWidgetPainter, self).__init__(show_reward=show_reward)
        self.text = text

    def prepare_widget(self, widget):
        widget = super(BaselineProtocolWidgetPainter, self).prepare_widget(widget)
        self.text_item = pg.TextItem(html='<center><font size="7" color="#e5dfc5">{}</font></center>'.format(self.text),
                                anchor=(0.5, 0.5))
        self.text_item.setTextWidth(500)
        widget.addItem(self.text_item)
        self.plotItem = widget.plotItem

    def redraw_state(self, sample, m_sample, chunk):
        pass

    def set_message(self, text):
        self.text = text
        self.text_item.setHtml('<center><font size="7" color="#e5dfc5">{}</font></center>'.format(self.text))

class ThresholdBlinkFeedbackProtocolWidgetPainter(Painter):
    def __init__(self, threshold=2000, time_ms=50, show_reward=False):
        super(ThresholdBlinkFeedbackProtocolWidgetPainter, self).__init__(show_reward=show_reward)
        self.threshold = threshold
        self.time_ms = time_ms
        self.blink_start_time = -1
        self.widget = None
        self.x = np.linspace(-10, 10, 2)
        self.previous_sample = -np.inf

    def prepare_widget(self, widget):
        widget = super(ThresholdBlinkFeedbackProtocolWidgetPainter, self).prepare_widget(widget)
        self.p1 = widget.plot([-10, 10], [10, 10], pen=pg.mkPen(77, 144, 254)).curve
        self.p2 = widget.plot([-10, 10], [-10, -10], pen=pg.mkPen(77, 144, 254)).curve
        self.fill = pg.FillBetweenItem(self.p1, self.p2, brush=(255, 255, 255, 25))
        widget.addItem(self.fill)

    def redraw_state(self, samples, m_sample, chunk):
        samples = np.abs(samples)
        if np.ndim(samples)==0:
            samples = samples.reshape((1, ))

        previous_sample = self.previous_sample
        do_blink = False
        for sample in samples:
            if (sample >= self.threshold >= previous_sample) and (self.blink_start_time < 0):
                do_blink = True
            previous_sample = sample

        if do_blink:
            self.blink_start_time = time.time()

        if ((time.time() - self.blink_start_time < self.time_ms * 0.001) and (self.blink_start_time > 0)):
            self.fill.setBrush((255, 255, 255, 255))
        else:
            self.blink_start_time = -1
            self.fill.setBrush((255, 255, 255, 10))


        self.previous_sample = previous_sample
        pass


class VideoProtocolWidgetPainter(Painter):
    def __init__(self, video_file_path):
        super(VideoProtocolWidgetPainter, self).__init__()
        self.widget = None
        self.video = None
        self.timer = time.time()
        self.timer_period = 1 / 30
        self.frame_counter = 0
        self.n_frames = None
        self.err_msg = "Could't open video file. "
        import os.path
        if os.path.isfile(video_file_path):
            try:
                import imageio as imageio
                self.video = imageio.get_reader(video_file_path,  'ffmpeg')
                self.n_frames = self.video.get_length() - 1
            except ImportError as e:
                print(e.msg)
                self.err_msg += e.msg
        else:
            self.err_msg = "No file {}".format(video_file_path)


    def prepare_widget(self, widget):
        widget = super(VideoProtocolWidgetPainter, self).prepare_widget(widget)
        if self.video is not None:
            self.img = pg.ImageItem()
            self.img.setScale(10 / self.video.get_data(0).shape[1])
            self.img.rotate(-90)
            self.img.setX(-5)
            self.img.setY(5/self.video.get_data(0).shape[1]*self.video.get_data(0).shape[0])
            widget.addItem(self.img)

        else:
            text_item = pg.TextItem(html='<center><font size="6" color="#a92f41">{}'
                                         '</font></center>'.format(self.err_msg),
                                    anchor=(0.5, 0.5))
            text_item.setTextWidth(500)
            widget.addItem(text_item)

    def redraw_state(self, sample, m_sample, chunk):
        if self.video is not None:
            timer = time.time()
            if timer - self.timer > self.timer_period:
                self.timer = timer
                self.frame_counter = (self.frame_counter + 1) % self.n_frames
                self.img.setImage(self.video.get_data(self.frame_counter))
            pass


if __name__ == '__main__':
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    from time import sleep
    import numpy as np
    a = QtGui.QApplication([])
    w = ProtocolWidget()
    w.show()
    b = VideoProtocolWidgetPainter('C:\\Users\\Nikolai\PycharmProjects\\nfb\pynfb\protocols\\video\small.mp4')
    b.prepare_widget(w)
    timer = QtCore.QTimer()
    timer.start(1000/30)
    timer.timeout.connect(lambda: b.redraw_state(np.random.normal(scale=0.2), np.random.normal(scale=0.2)))
    a.exec_()
    #for k in range(10000):
    #    sleep(1/30)
    #    b.redraw_state(np.random.normal(size=1))

