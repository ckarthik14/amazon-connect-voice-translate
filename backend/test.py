from base64 import b64decode

a = b64decode("eyJ0cmFuc2xhdGVkX3RleHQiOiAiXHUwOTIwXHUwOTQwXHUwOTE1IFx1MDkzOVx1MDk0OD8ifQ==")
utf_decoded = a.decode('utf-8')

print(a)
print(utf_decoded)

print("a", "b")