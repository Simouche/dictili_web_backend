
def handle_uploaded_file(file, directory):
    with open(directory, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

