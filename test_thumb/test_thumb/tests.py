from io import BytesIO
from PIL import Image

from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import ImageMediaForm, VideoMediaForm


def create_test_image():
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.seek(0)
    in_memory_uploaded_file = InMemoryUploadedFile(
        file, None, 'test.jpg', 'png', None, None
    )
    return in_memory_uploaded_file


class ImageMediaTest(TestCase):

    def test_form_render(self):
        form = ImageMediaForm()
        self.assertIn("thumbnail", form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ImageMediaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['thumbnail'],
            ["This field cannot be blank."]
        )

    def test_submit_image(self):
        """
        thumbnail:data<<[
                <str: image path if any>
                <InMemoryFile: image>
                <list: colored text [<str: font text>,
                                    <str: text color>,
                                    <str: text border color>,
                                    <str: font style>],
                                    ],
        """
        colored_text_values = ["test", "0000", "0000", '0']
        form = ImageMediaForm(
            data={'thumbnail_0': '',
                  'thumbnail_1': create_test_image(),
                  'thumbnail_2_0': colored_text_values[0],
                  'thumbnail_2_1': colored_text_values[1],
                  'thumbnail_2_2': colored_text_values[2],
                  'thumbnail_2_3': colored_text_values[3]},
            files={'thumbnail_1': create_test_image()})
        self.assertEqual(form.is_valid(), True)


class VideoMediaFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = VideoMediaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['thumbnail'],
            ["This field cannot be blank."]
        )

    def test_form_render(self):
        form = VideoMediaForm()
        self.assertIn("thumbnail", form.as_p())

    def test_submit_video(self):
        """
            thumbnail:data<<[
                <str: image path if any>,
                <str: video path if any>,
                <str:cascade choose>,
                <str:specific time ex:MM:SS>,
                <bool:random time>,
                <InMemoryFile: manually submitted Imaged>,
                <list: [<str: font text>,<tuple: text color>, <tuple: text border color>, <str: font style>]>,
            ]
        """
        pass
