import subprocess

files = []

for i in range(137, 191):
    files.append('pic' + str(i) + '.png')

command = [
    'C:/Program Files/ImageMagick-7.0.9-Q8/magick.exe',
    'convert',
    '-delay', '10',
    '-size', '1150x930'
] + files + [
    'anim.gif'
]

subprocess.call(command)
