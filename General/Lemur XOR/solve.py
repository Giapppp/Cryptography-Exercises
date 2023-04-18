import imageio
lemur = imageio.imread('lemur.png')
flag = imageio.imread('flag.png')
answer = lemur ^ flag
imageio.imwrite("answer.png", answer)
