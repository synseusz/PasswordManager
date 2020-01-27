displayed_label = [0]
            
for x in displayed_label:
    l = len(displayed_label)
    print("tu jestem: " + str(x))
    if x == 0:
        displayed_label.clear()
        displayed_label.append(1)
        x += x
        print("1: " + str(displayed_label))
    else:
        print("2: " + str(displayed_label))
        