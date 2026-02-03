from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image
from fastapi.responses import JSONResponse

app = FastAPI()

# Load model (ensure the model is in the same directory or provide the correct path)
fashion_model = load_model("cifar_model.h5")

class_names = [
    "Airplane", "Automobile", "Bird", "Cat", "Deer", "Dog", "Frog", "Horse", "Ship", "Truck"
]

def prepare_image(img):
    img = img.resize((32, 32))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    img = Image.open(BytesIO(await file.read()))
    img_array = prepare_image(img)

    prediction = fashion_model.predict(img_array)
    predicted_class = np.argmax(prediction)

    return JSONResponse(content={
        'prediction': class_names[predicted_class],
        'confidence': float(np.max(prediction))
    })

if __name__=="__main__":
    app.run(debug=True)
