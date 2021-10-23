import os

class Produit():

    def __init__(self, description,categorie, prix, code, marque, date_echantilion):
        self.description = description
        self.categorie = categorie
        self.prix = prix
        self.code = code
        self.marque = marque
        self.date_echantillion = date_echantilion

    def __iter__(self):
        return self


class Persistence():
    def save(self, produits):
        file_exists = os.path.isfile("produits.csv")
        with open("produits.csv", 'a+',encoding="utf-8") as f:
            if not file_exists:
                f.write("description,prix,code,marque,date\n")
            for p in produits:
                f.write("{},{},{},{},{},{}\n".format(p.description,p.categorie,p.prix,p.code,p.marque,p.date_echantillion))


# produits = []
# produits.append(Produit("urubu", 10.4, "24fsfds", "biu", 432434))
# Persistence().save(produits)
