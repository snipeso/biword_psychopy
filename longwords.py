path = './datasets/american-english'
with open(path, 'r') as f:
    dataset = f.read().split('\n')
    word= max(dataset, key=len)
    print word.upper()
