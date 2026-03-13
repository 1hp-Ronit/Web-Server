def fun():
    with open('pages/404.html', 'rb') as f:
        data = f.read()
        return data
print(fun())