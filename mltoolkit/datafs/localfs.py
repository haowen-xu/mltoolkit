import os

from mltoolkit.utils import makedirs
from .utils import ActiveFiles, iter_files
from .base import *

__all__ = ['LocalFS']


class LocalFS(DataFS):
    """
    A :class:`DataFS` backed by local file system.
    """

    def __init__(self, root_dir, strict=False):
        """
        Construct a new :class:`LocalFS`.

        Args:
            root_dir (str): The root directory for this :class:`LocalFS`.
            strict (bool): Whether or not this :class:`DataFS` works in
                strict mode?  (default :obj:`False`)
        """
        super(LocalFS, self).__init__(strict=strict)

        root_dir = os.path.abspath(root_dir)
        if not os.path.isdir(root_dir):
            raise IOError('Not a directory: {!r}'.format(root_dir))
        self._root_dir = root_dir
        self._capacity = DataFSCapacity(
            DataFSCapacity.READ_DATA,
            DataFSCapacity.WRITE_DATA,
        )
        self._active_files = ActiveFiles()

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def capacity(self):
        return self._capacity

    def clone(self):
        return LocalFS(self.root_dir)

    def _init(self):
        pass

    def _close(self):
        self._active_files.close_all()

    def iter_names(self):
        self.init()
        return iter_files(self.root_dir)

    def sample_names(self, n_samples):
        raise UnsupportedOperation()

    def open(self, filename, mode):
        self.init()
        file_path = os.path.join(self.root_dir, filename)
        if mode == 'r':
            return self._active_files.add(open(file_path, 'rb'))
        elif mode == 'w':
            parent_dir = os.path.split(file_path)[0]
            makedirs(parent_dir, exist_ok=True)
            return self._active_files.add(open(file_path, 'wb'))
        else:
            raise ValueError('Invalid open mode {!r}'.format(mode))

    def isfile(self, filename):
        return os.path.isfile(os.path.join(self.root_dir, filename))

    def list_meta(self, filename):
        raise UnsupportedOperation()

    def get_meta(self, filename, meta_keys):
        raise UnsupportedOperation()

    def put_meta(self, filename, meta_dict=None, **meta_dict_kwargs):
        raise UnsupportedOperation()

    def clear_meta(self, filename):
        raise UnsupportedOperation()
