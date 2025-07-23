# Targeted adversarial attacks

## Description
This mini project aims to add adversarial noise to images to trick a classifier to predict the input images as the wrong class, while the input images remain human identifiable. The project specifically creates targeted adversarial attacks, such that the wrong class is predefined.

## Installation
Use `pip install -e .` inside the project's root folder.

## Example code
A Jupyter notebook is stored in `example/` folder.

## Methods
### 1. Adding adversarial noise

While there are multiple ways to add adversarial noise, iterative FGSM / PGD is used in this project because:
1. Easy to implement;
2. Supports both targeted and untargeted attacks (targeted in this project);
3. Relatively transferrable and widely recognised as a benchmark;
4. Iteratively refines the perturbation than FGSM, therefore more effective;
5. PGD has a bound on the perturbation, which makes sure that the attacked images are visually similar.

### 2. Validation
#### 2.1 Are the noisy images classified as the predefined wrong classes?
Validating this question is straight-forward: 
for an input image $I$, and a predefined class $y_target$, the classifier should incorrectly predict the attacked image, $I_noise$, as class $y_target$.

Ideally, the classifier should correctly predict $I$ as the true class $y_true$.

In this mini project, we only validate this aspect on images that are correctly predicted before being attacked.

#### 2.2 Are the attacked images human-identifiable?
While it may be easy for me (who happens to be a human) to look at several images and decide whether I can still recognise the attacked ones, it becomes challenging to repeat this process on many images and this approach lacks quantifiable metrics to prove the human readability.

Metrics such as Structural Similarity Index and Learned Perceptual Image Patch Similarity can be implemented to quantify human perception given more time.

### 3. Data & model choices

#### 3.1 Data
In this project, I chose MNIST data mainly because 
1. Accessible: built-in with torchvision; unlike ImageNet which requires an additional license
2. Lightweight: small in size, easy to train and test
3. Not so complex: so it's faster to train

#### 3.2 Model
I used ResNet18 because
1. Accessible: built-in with torchvision;
2. High performance & robustness

Built-in ResNet18 was further fine-tuned in two models:
1. ResNetMNIST: retain ResNet18's architecture but retrain all parameters
2. ResNetMNIST_ft: freeze ResNet18's parameters except for the final layer

I initially used ResNetMNIST only, which seemed too robust to attack on small/simpler datasets like MNIST. To verify my assumption, I created ResNetMNIST_ft to introduce a model that does not perform very well, and see if a lower perturbation is needed.

### 4. Results & conclusion

Full results can be found in `example/example_mnist.ipynb`

As mentioned above, ResNetMNIST was quite robust and a very high perturbation was needed to attack the images. Human (basically myself) can still recognise the digits, but the images are clearly super noisy.

ResNetMNIST_ft is easier to attack and a smaller perturbation is needed. But as the model itself is not very good, the performance on the non-attacked images are not very good.

For MNIST, a simpler model might have a better balance between performance before & after attacks (e.g. https://www.cs.toronto.edu/~lczhang/360/lec/w09/adv.html)

### 5. Next steps

There are a few things I want to try, given more time:

1. Use metrics that correlate to human perception to determine whether the attacked images are still human recognisable;
2. Parameter optimisation for iterative FGSM / PGD, e.g. via binary search;
3. Try other attacks;
3. Try a more complex dataset.