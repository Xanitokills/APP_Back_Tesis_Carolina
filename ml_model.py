import io
from PIL import Image
import torch
from torchvision import transforms
import timm
from .config import settings

# Lista de estilos en el mismo orden usado al entrenar
CLASSES = [
    "Post Impressionism",
    "Cubism",
    "Realism",
    "PopArt",
    "Surrealism",
    "NaiveArt",
    "Symbolism",
    "Expressionism",
    "Baroque",
    "Romanticism",
    "Byzantin_Iconography",
    "Moderm",
    "Rococo",
    "High Renaissance",
    "Northern Renaissance",
    "Early Renaissance",
    "Fauvism"
    # ... el resto de estilos
]

# Transforms idénticos a los del entrenamiento
_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# 1) Creamos el modelo con timm
_model = timm.create_model(
    "vit_base_patch16_224",
    pretrained=False,
    num_classes=len(CLASSES)
)

# 2) Cargamos el state_dict desde disco
_state = torch.load(settings.model_path, map_location="cpu")

# 3) Desprefijamos las claves que vienen con "vit."
new_state = {}
for k, v in _state.items():
    # si el key empieza con "vit.", lo quitamos; si no, lo dejamos igual
    if k.startswith("vit."):
        new_state[k[len("vit."):]] = v
    else:
        new_state[k] = v

# 4) Cargamos en el modelo, indicando strict=False
#    (para ignorar cualquier clave sobrante o faltante)
_model.load_state_dict(new_state, strict=False)
_model.eval()

def predict_style_from_path(path: str) -> str:
    """
    Dada la ruta de una imagen en disco, devuelve el nombre del estilo.
    """
    img = Image.open(path).convert("RGB")
    x = _transform(img).unsqueeze(0)
    with torch.no_grad():
        logits = _model(x)
        idx = logits.argmax(dim=-1).item()
    return CLASSES[idx]
