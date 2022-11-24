import torch
import os
import pytorch_lightning as pl
from torch.optim import AdamW


# TODO: make layers w weight decay configurable
class BaseModel(pl.LightningModule):
    def __init__(self):
        super().__init__()

    def setup(self, stage):
        if self.global_rank == 0:
            os.makedirs(self.hparams["path_results"], exist_ok=True)

    def configure_optimizers(self):
        # param_optimizer = list(self.net.named_parameters())
        param_optimizer = [param for param in self.named_parameters() if param[1].requires_grad]

        no_decay = ["bias", "gamma", "beta", "LayerNorm", "layer_norm"]

        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
                "weight_decay": self.hparams["weight_decay"],
            },
            {
                "params": [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
                "weight_decay": 0.0,
            },
        ]
        # no_decay = [n for n, p in param_optimizer if any(nd in n for nd in no_decay)]
        # print("no decay", no_decay)
        optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=self.hparams["initial_lr"],
            eps=self.hparams["eps"],
            # weight_decay=self.hparams["weight_decay"],
            betas=(self.hparams["beta1"], self.hparams["beta2"]),
        )
        # optimizer = FusedLAMB(
        #     optimizer_grouped_parameters,
        #     lr=self.hparams["initial_lr"],
        #     eps=self.hparams["eps"],
        #     # weight_decay=self.hparams["weight_decay"],
        #     betas=(self.hparams["beta1"], self.hparams["beta2"]),
        # )
        # optimizer.clip_grad_norm(1.0)
        cnt_epochs = self.hparams["cnt_epochs"]
        batch_size = self.hparams["batch_size_effective"]
        print("BATCH EFFECTIVE", batch_size)
        if hasattr(self.trainer.datamodule, "cnt_train_samples"):
            self.hparams["cnt_samples_per_train_epoch"] = self.trainer.datamodule.cnt_train_samples
        samples_per_epoch = self.hparams["cnt_samples_per_train_epoch"]
        # print(f"!!!!!!!! samples per epoch: {samples_per_epoch}")
        training_steps = int((batch_size + samples_per_epoch) * cnt_epochs / batch_size) + 1
        # print(f"!!!!!!!! expected steps: {training_steps}")
        # TODO: get rough estimation of training steps here
        # maybe after first epoch is trained - reset iterators?
        pct_start = self.hparams["percent_warmup"] / 100.0
        # print("setting training_steps as", training_steps)
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer,
            max_lr=self.hparams["max_lr"],
            total_steps=training_steps,
            pct_start=pct_start,
            anneal_strategy="linear",
        )
        scheduler = {"scheduler": scheduler, "interval": "step"}
        return [[optimizer], [scheduler]]
