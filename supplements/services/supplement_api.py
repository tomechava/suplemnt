# supplements/services/supplement_api.py
import requests
import json

def get_supplements_by_keyword(keyword):
    url = "https://api.ods.od.nih.gov/dsld/v9/browse-products/"
    params = {
        "method": "by_keyword",
        "q": keyword
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()  # La respuesta es un JSON con la data
    else:
        return None




'''if __name__ == "__main__":
    # Ejemplo de uso
    supplements = get_supplements_by_keyword("Thermogenic Fat Burner")
    first_supplement = supplements["hits"][0] if supplements["total"]["value"]>0 else None
    if supplements:
        print(json.dumps(supplements, indent=4))  # Imprime la respuesta formateada
    else:
        print("No se encontraron suplementos.")
'''
