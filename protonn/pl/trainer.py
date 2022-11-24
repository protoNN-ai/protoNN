import pytorch_lightning as pl
from pytorch_lightning.callbacks import LearningRateMonitor
from pytorch_lightning.loggers import WandbLogger


def get_trainer(cluster_env, params):
    logger = WandbLogger(
        project=params["name_project"],
        save_dir=params["path_results"],
    )
    lr_monitor = LearningRateMonitor(logging_interval="step")
    trainer = pl.Trainer(
        plugins=[cluster_env],
        default_root_dir=params["path_results"],
        devices=params["devices"],
        accelerator=params["accelerator"],
        num_nodes=cluster_env.cnt_nodes(),
        num_sanity_val_steps=10,
        max_epochs=params["cnt_epochs"],
        strategy="ddp_find_unused_parameters_false",
        precision=params["precision"],
        replace_sampler_ddp=False,
        logger=logger,
        log_every_n_steps=50,
        reload_dataloaders_every_n_epochs=1,
        # callbacks=[lr_monitor, LayerNormCallback(), Monitor()],
        callbacks=[lr_monitor],
        gradient_clip_val=params["gradient_clip_val"],
        enable_progress_bar=False,
        enable_checkpointing=False,
        # TODO: figure out what is this
        track_grad_norm=1,
        # detect_anomaly=True, # This is very slow!
        # profiler="simple",
        # plugins="deepspeed_stage_2",
        accumulate_grad_batches=params["accumulate_batches"],
    )
    return trainer
