from stegano import slsb

secret = slsb.hide("./pictures/Lenna.png", "Bonjour tout le monde")
secret.save("./Lenna-secret.png")