"""Video rendering functions used for frame-based animation."""

import numpy as np
import imageio

from .drawing import Drawing


def render_svg_frames(frames, align_bottom=False, align_right=False,
                      bg=(255,)*4, **kwargs):
    arr_frames = [imageio.imread(d.rasterize().png_data)
                  for d in frames]
    max_width = max(map(lambda arr:arr.shape[1], arr_frames))
    max_height = max(map(lambda arr:arr.shape[0], arr_frames))

    def mod_frame(arr):
        new_arr = np.zeros((max_height, max_width) + arr.shape[2:],
                           dtype=arr.dtype)
        new_arr[:,:] = bg[:new_arr.shape[-1]]
        if align_bottom:
            slice0 = slice(-arr.shape[0], None)
        else:
            slice0 = slice(None, arr.shape[0])
        if align_right:
            slice1 = slice(-arr.shape[1], None)
        else:
            slice1 = slice(None, arr.shape[1])
        new_arr[slice0, slice1] = arr
        return new_arr
    return list(map(mod_frame, arr_frames))

def save_video(frames, file, **kwargs):
    """Save a series of drawings as a GIF or video.

    Args:
        frames: A list of `Drawing`s or a list of `numpy.array`s.
        file: File name or file-like object to write the video to.  The
            extension determines the output format.
        align_bottom: If frames are different sizes, align the bottoms of each
            frame in the video.  Default: False.
        align_right: If frames are different sizes, align the right edge of each
            frame in the video.  Default: False.
        bg: If frames are different sizes, fill the background with this color.
            Default: white (255, 255, 255, 255).
        fps: The animation speed in frames per second.
        **kwargs: Other arguments to imageio.mimsave().
    """
    if 'fps' in kwargs and file.endswith('.gif'):
        kwargs.setdefault('duration', 1/kwargs.pop('fps'))
    if isinstance(frames[0], Drawing):
        frames = render_svg_frames(frames, **kwargs)
    kwargs.pop('align_bottom', None)
    kwargs.pop('align_right', None)
    kwargs.pop('bg', None)
    imageio.mimsave(file, frames, **kwargs)