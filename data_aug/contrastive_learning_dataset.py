from torchvision.transforms import transforms
from data_aug.gaussian_blur import GaussianBlur
from torchvision import transforms, datasets
from data_aug.view_generator import ContrastiveLearningViewGenerator
from exceptions.exceptions import InvalidDatasetSelection
from data_aug.custom_datasets import custom_COVID19_Xray_faster, custom_histopathology_faster


class ContrastiveLearningDataset:
    def __init__(self, root_folder, dataset_name):
        self.root_folder = root_folder
        self.dataset_name = dataset_name

    @staticmethod
    def get_simclr_pipeline_transform(size, s=1):
        """Return a set of data augmentation transformations as described in the SimCLR paper."""
        color_jitter = transforms.ColorJitter(0.8 * s, 0.8 * s, 0.8 * s, 0.2 * s)

        if self.dataset_name == "histopathology":
            data_transforms = transforms.Compose([transforms.RandomResizedCrop(size=size),
                                                transforms.RandomHorizontalFlip(),
                                                transforms.RandomApply([color_jitter], p=0.8),
                                                transforms.RandomGrayscale(p=0.2),
                                                GaussianBlur(kernel_size=int(0.1 * size)),
                                                transforms.ToTensor(),
                                                transforms.Normalize(mean=[.5], std=[.5])])

        elif self.dataset_name =="COVID19_Xray":
            data_transforms = transforms.Compose([transforms.RandomResizedCrop(size=size),
                                                transforms.RandomHorizontalFlip(),
                                                transforms.RandomApply([color_jitter], p=0.8),
                                                transforms.RandomGrayscale(p=0.2),
                                                GaussianBlur(kernel_size=int(0.1 * size)),
                                                transforms.ToTensor(),
                                                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                std=[0.229, 0.224, 0.225])])
        

        # data_transforms =  transforms.Compose([
        #         transforms.RandomResizedCrop(size=(224,224)),
        #         transforms.RandomHorizontalFlip(),
        #         transforms.RandomRotation(10),
        #         transforms.RandomAdjustSharpness(3),
        #         transforms.RandomAutocontrast(),
        #         transforms.RandomEqualize(),
               
        #     ])
        
        return data_transforms

    def get_dataset(self, name, n_views):
        valid_datasets = {'cifar10': lambda: datasets.CIFAR10(self.root_folder, train=True,
                                                              transform=ContrastiveLearningViewGenerator(
                                                                  self.get_simclr_pipeline_transform(32),
                                                                  n_views),
                                                              download=True),

                          'stl10': lambda: datasets.STL10(self.root_folder, split='unlabeled',
                                                          transform=ContrastiveLearningViewGenerator(
                                                              self.get_simclr_pipeline_transform(96),
                                                              n_views),
                                                          download=True),
                                                          
                           'COVID19_Xray': lambda: custom_COVID19_Xray_faster(self.root_folder,train=True,
                                                              transform=ContrastiveLearningViewGenerator(
                                                                  self.get_simclr_pipeline_transform(224),
                                                                  n_views)),
        
                           'histopathology': lambda: custom_histopathology_faster(self.root_folder,train=True,
                                                              transform=ContrastiveLearningViewGenerator(
                                                                  self.get_simclr_pipeline_transform(224),
                                                                  n_views))}

        try:
            dataset_fn = valid_datasets[name]
        except KeyError:
            raise InvalidDatasetSelection()
        else:
            return dataset_fn()
