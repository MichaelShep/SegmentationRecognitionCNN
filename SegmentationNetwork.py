from DataLoader import ImageDataset
import torch.nn as nn
import torch
import os.path
import sys
import matplotlib.pyplot as plt

def extract_element_from_sublist(main_list, index):
  return [item[index] for item in main_list]

def display_outputs(input_tensor, output):
  fig = plt.figure('Output Channels', figsize=(20, 1))

  fig.add_subplot(1, len(output) + 1, 1)
  plt.imshow(input_tensor.permute(1, 2, 0))
  plt.axis('off')

  for i in range(1, len(output) + 1):
    fig.add_subplot(1, len(output) + 1, i + 1)
    plt.imshow(output[i - 1])
    plt.axis('off')

  plt.tight_layout()
  plt.show()

''' Class defining the Segmentation Network
    All the layers of the network are setup here and the flow through the network is also defined
'''
class SegmentationNetwork(nn.Module):
  ''' Constructor for the class
      All layers of the network and their parameters get defined here
  '''
  def __init__(self):
    super(SegmentationNetwork, self).__init__()

    #Create the layers for the network
    #First Conv layer - RGB image input so 3 channels, 3x3 kernal and padding 1 to keep same image size
    self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)

  ''' Performs a forward pass through the network for some data
      Method should not be called directly as only gets called as part of the lifecycle of the network
  '''
  def forward(self, x):
    x = self.conv1(x)
    return x

if __name__ == '__main__':
  current_directory = sys.path[0]
  dataset_directory = os.path.join(os.path.split(current_directory)[0], 'CelebAMask-HQ')
  image_directory = os.path.join(dataset_directory, 'CelebA-HQ-img')
  features_directory = os.path.join(dataset_directory, 'CelebAMask-HQ-mask-anno')

  dataset = ImageDataset(image_directory, features_directory)
  train_data = dataset.load_data(1, 1)

  train_data_input = torch.stack(extract_element_from_sublist(train_data, 0))
  train_data_output = torch.stack(extract_element_from_sublist(train_data, 1))

  network = SegmentationNetwork()
  output = network(train_data_input)
  print(output)

  display_outputs(train_data_input[0], output.detach()[0])