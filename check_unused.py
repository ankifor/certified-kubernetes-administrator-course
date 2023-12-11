from pathlib import Path
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


# First create the treeprocessor

class ImgExtractor(Treeprocessor):
    def run(self, doc):
        # Find all images and append to markdown.images. 
        self.md.images = []
        for image in doc.findall('.//img'):
            self.md.images.append(image.get('src'))

# Then tell markdown about it

class ImgExtExtension(Extension):
    def extendMarkdown(self, md):
        img_ext = ImgExtractor(md)
        md.treeprocessors.register(img_ext,'imgext',3.0)
        #md.treeprocessors.add('imgext', img_ext, '>inline')




used_images = set()
md = markdown.Markdown(extensions=[ImgExtExtension()])
path_mds = Path("docs").glob('**/*.md')
for path_md in path_mds:
    with path_md.open() as f:
        data = f.read()
    dir_md = path_md.parent
    _ = md.convert(data)
    for image in md.images:
        path_image = dir_md.joinpath(image).resolve()
        used_images.add(path_image)


path_images = Path("images").glob('**/*.*')
for path_image in path_images:
    path_image_final = path_image.resolve()
    if not path_image_final in used_images:
        print(str(path_image))


