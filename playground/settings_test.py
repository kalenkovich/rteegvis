from nfb.pynfb.brain import SourceSpaceWidgetPainterSettings

settings = SourceSpaceWidgetPainterSettings()
widget = settings.create_widget()
widget.show()
slider_widget = list(settings.colormap.threshold_pct.items.items())[0][0].slider_widget


ss = """
    QSlider::groove:horizontal {
        height: 40px;
    }

    QSlider::handle:horizontal {
        height: 20px;
    }
"""