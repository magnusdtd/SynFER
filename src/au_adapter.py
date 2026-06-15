import torch


class AUProjModel(torch.nn.Module):
    def __init__(self, au_dim, cross_attention_dim):
        super().__init__()
        self.au_dim = au_dim
        self.cross_attn_dim = cross_attention_dim

        self.proj = torch.nn.Linear(au_dim, self.cross_attn_dim)

    def forward(self, au_label):
        au_embeddings = self.proj(au_label)
        au_embeddings = au_embeddings.unsqueeze(dim=1)
        return au_embeddings


class AUAdapter(torch.nn.Module):
    """Modified from IP-Adapter"""

    def __init__(self, unet, au_proj_model, adapter_modules, ckpt_path=None):
        super().__init__()
        self.unet = unet
        self.au_proj_model = au_proj_model
        self.adapter_modules = adapter_modules  # attention

        if ckpt_path is not None:
            self.load_from_checkpoint(ckpt_path)

    def forward(self, noisy_latents, timesteps, encoder_hidden_states, au_label):
        au_token = self.au_proj_model(au_label)
        # print(au_token.shape, encoder_hidden_states.shape)
        encoder_hidden_states = torch.cat([encoder_hidden_states, au_token], dim=1)
        # Predict the noise residual
        noise_pred = self.unet(noisy_latents, timesteps, encoder_hidden_states).sample
        return noise_pred

    def load_from_checkpoint(self, ckpt_path: str):
        # Calculate original checksums
        orig_ip_proj_sum = torch.sum(torch.stack([torch.sum(p) for p in self.au_proj_model.parameters()]))
        orig_adapter_sum = torch.sum(torch.stack([torch.sum(p) for p in self.adapter_modules.parameters()]))

        state_dict = torch.load(ckpt_path, map_location="cpu")

        # Load state dict for au_proj_model and adapter_modules
        self.au_proj_model.load_state_dict(state_dict["image_proj"], strict=True)
        self.adapter_modules.load_state_dict(state_dict["ip_adapter"], strict=True)

        # Calculate new checksums
        new_ip_proj_sum = torch.sum(torch.stack([torch.sum(p) for p in self.au_proj_model.parameters()]))
        new_adapter_sum = torch.sum(torch.stack([torch.sum(p) for p in self.adapter_modules.parameters()]))

        # Verify if the weights have changed
        assert orig_ip_proj_sum != new_ip_proj_sum, "Weights of image_proj_model did not change!"
        assert orig_adapter_sum != new_adapter_sum, "Weights of adapter_modules did not change!"

        print(f"Successfully loaded weights from checkpoint {ckpt_path}")
