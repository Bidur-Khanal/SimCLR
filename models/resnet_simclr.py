import torch.nn as nn
import torchvision.models as models

from exceptions.exceptions import InvalidBackboneError


def ResNetSimCLR(base_model, out_dim):

    if base_model == "resnet18":
        model = models.resnet18(pretrained=False, num_classes=out_dim)
        dim_mlp = model.fc.in_features
        model.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), model.fc)

    elif base_model == "resnet50":
        model = models.resnet50(pretrained=False, num_classes=out_dim)
        dim_mlp = model.fc.in_features
        model.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), model.fc)

    return model