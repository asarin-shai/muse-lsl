
def view(window=5, scale=100, refresh=0.2, figure="15x6", version=1, backend='TkAgg',
         filt=True, window_step=1.0, scale_factor=1.2, subsample=None):
    if version == 2:
        from . import viewer_v2
        viewer_v2.view(window=window, scale=scale, refresh=refresh, filt=filt)
    else:
        from . import viewer_v1
        viewer_v1.view(window, scale, refresh, figure, backend, filt=filt,
                       window_step=window_step, scale_factor=scale_factor,
                       subsample=subsample)
