s = 'qwertyuiopasdfghjklzxcvbAEUnm'

vocales = 0
for i in s:
    if i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u':
        vocales += 1

print(f'Numero de vocales minúsculas: {vocales}')

