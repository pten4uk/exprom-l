import os.path

from PIL import Image


class PhotoFormatter:
    ALLOWED_FORMATS = ['jpg', 'jpeg', 'png', 'JPG', 'JPEG']
    default_msg = 'Фотография может быть только в формате "jpg" или "png"'

    def __init__(self, path):
        self.path = path
        self.photo = Image.open(path)
        self.name = path.split('\\')[-1]
        self.format = self.name.split('.')[-1]

    def __is_valid(self, msg=None):
        if self.format not in self.ALLOWED_FORMATS:
            raise ValueError(msg or self.default_msg)
        return True

    def _resize_photo(self):
        """ Приводит self.photo к соотношению сторон 3/2 """

        ratio = self.photo.width / self.photo.height

        left = 0
        upper = 0
        right = self.photo.width
        lower = self.photo.height

        if ratio > 1.5:
            # подрезаем width
            new_width = int(self.photo.height * 1.5)
            diff = (self.photo.width - new_width) // 2
            left = diff
            right -= diff
        elif ratio < 1.5:
            # подрезаем height
            new_height = int(self.photo.width // 1.5)
            diff = (self.photo.height - new_height) // 2
            upper = diff
            lower -= diff
        else:
            return

        self.photo = self.photo.crop((left, upper, right, lower))

    @staticmethod
    def _remove_old_photo(path):
        if os.path.exists(path):
            os.remove(path)

    def save(self, msg=None):
        self.__is_valid(msg)

        self._resize_photo()
        self._remove_old_photo(self.path)
        self.photo.save(self.path)
        return self.path
