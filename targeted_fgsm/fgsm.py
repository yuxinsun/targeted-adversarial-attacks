import torch
import torch.nn.functional as F


class TargetedFGSM:

    def __init__(self, epsilon=0.1, alpha=0.01, max_iter=100):
        self.epsilon = epsilon
        self.alpha = alpha
        self.max_iter = max_iter

    def add_noise(self, image, target_label, model, device='cpu'):

        model.eval()
        image = image.clone().detach().to(device)
        target_label = torch.tensor([target_label], dtype=torch.long).to(device)
        adv_image = image.clone().detach().requires_grad_(True)

        for _ in range(self.max_iter):
            output = model(adv_image)
            loss = F.cross_entropy(output, target_label)

            model.zero_grad()
            loss.backward()

            with torch.no_grad():

                # make image closer to the target class
                adv_image -= self.alpha * adv_image.grad.sign()

                # project back into the epsilon ball around the original image
                delta = torch.clamp(adv_image - image, min=-self.epsilon, max=self.epsilon)
                adv_image = torch.clamp(image + delta, 0, 1).detach_().requires_grad_(True)

        return adv_image