def handle_uploaded_file(f,car):
    string = "/home/greengears/media_root/"
    string += str(car.YEAR) + '-' + str(car.id) + '-' + str(car.COUNT)
    destination = open(string, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

