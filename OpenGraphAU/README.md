# OpenGrpahAU

### Example running on a RTX 3090 GPU (Avg. FPS>50):
<table border="0" style="width: 100%; text-align: left; margin-top: 20px;">
<!--   <tr> -->
<!--       <td> -->
          <video src="https://github.com/user-attachments/assets/69737b41-f215-4b69-9c10-08ae26ba5dc3" width="100%" controls autoplay loop></video>
          <video src="https://github.com/user-attachments/assets/7a672e51-5a0a-4730-b02e-e5015570ba1b" width="100%" controls autoplay loop></video>
</table>


This repo is the OpenGprahAU tool.

Models were traiend on hybrid dataset of 2,000k images.

This hybrid dataset includes:
 * [BP4D](http://www.cs.binghamton.edu/~lijun/Research/3DFE/3DFE_Analysis.html)
 * [DISFA](http://mohammadmahoor.com/disfa-contact-form/)
 * [RAF-AU](http://www.whdeng.cn/RAF/model3.html)
 * [AFF-Wild 2](https://ibug.doc.ic.ac.uk/resources/aff-wild2/)
 * [CK+](http://www.jeffcohn.net/Resources/)
 * [CASME II](http://casme.psych.ac.cn/casme/e2)


The tool can predict action units of 41 categories:

| AU1 | AU2 | AU4 | AU5 | AU6 | AU7 | AU9 |   AU10 | AU11  | AU12 | AU13 | AU14 | AU15 | AU16 | 
| :-----:  | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| Inner brow raiser| Outer brow raiser | Brow lowerer  | Upper lid raiser  | Cheek raiser | Lid tightener | Nose wrinkler | Upper lip raiser | Nasolabial deepener | Lip corner puller | Sharp lip puller | Dimpler | Lip corner depressor | Lower lip depressor |

| AU17 | AU18 | AU19 | AU20 | AU22 | AU23 | AU24 |   AU25 | AU26  | AU27 | AU32 | AU38 | AU39 | - | 
| :-----:  | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| Chin raiser | Lip pucker | Tongue show | Lip stretcher  | Lip funneler | Lip tightener | Lip pressor | Lips part | Jaw drop | Mouth stretch | Lip bite | Nostril dilator | Nostril compressor | - |

| AUL1 | AUL1 | AUL2 | AUR2 | AUL4 | AUR4 | AUL6 |   AUR6 | AUL10  | AUR10 | AUL12 | AUR12 | AUL14 | AUR14 | 
| :-----:  | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| Left inner brow raiser | Right inner brow raiser | Left outer brow raiser | Right outer brow raiser| Left brow lowerer | Right brow lowerer | Left cheek raiser | Right cheek raiser | Left upper lip raiser | Right upper lip raiser | Left nasolabial deepener | Right nasolabial deepener | Left dimpler | Right dimpler |


## Pretrained models

Hybrid Dataset

### Stage1:

|arch_type|GoogleDrive link| Average F1-score| Average Acc.|
| :--- | :---: |  :---: |  :---: | 
|`Ours (MobileNetV3)`| -| - |  - |
|`Ours (ResNet-18)`| [link](https://drive.google.com/file/d/1b9yrKF663K9IwY2C2-1SD6azpAdNgBm7/view?usp=share_link) | 22.33 |  92.97 |
|`Ours (ResNet-50)`| [link](https://drive.google.com/file/d/11xh9r2e4qCpWEtQ-ptJGWut_TQ0_AmSp/view?usp=share_link) | 22.52 |  92.63 |
|`Ours (Swin-Tiny)`| [link](https://drive.google.com/file/d/1JSa-ft965qXJlVGvnoMepbkRkSm78_to/view?usp=share_link) | 22.66 | 92.97 |
|`Ours (Swin-Small)`| [link](https://drive.google.com/file/d/1GNjFKpd00nvgYIP2q7AzRSzfzEUfAqfT/view?usp=share_link) | 24.49 | 92.84 |
|`Ours (Swin-Base)`| [link](https://drive.google.com/file/d/1nWwowmq4pQn1ACnSOOeyBy6-n0rmqTQ9/view?usp=share_link) | 23.53 | 92.91 |


### Stage2:

|arch_type|GoogleDrive link| Average F1-score| Average Acc.|
| :--- | :---: |  :---: | :---: |
|`Ours (MobileNetV3)`| -| - |  - |
|`Ours (ResNet-18)`|[link](https://drive.google.com/file/d/1CzWgr2ywt7TmxHLWM5tg1VaEbgGYyAZ4/view?usp=sharing) | 22.51 | 93.23 |
|`Ours (ResNet-50)`| [link](https://drive.google.com/file/d/1UMnpbj_YKlqHF1m0DHV0KYD3qmcOmeXp/view?usp=sharing)| 23.24 | 93.31 |
|`Ours (Swin-Tiny)`|[link](https://drive.google.com/file/d/1yRWnYY5BR_FDiquaKnzf_aCdkyjZM77E/view?usp=sharing)| 22.74 | 93.37 |
|`Ours (Swin-Small)`| - | - | - |
|`Ours (Swin-Base)`| - | - | - |



## Demo
- to detect facial action units in a facial image using our stage1 model, run:
```
uv run -m OpenGraphAU.main --arc resnet50 --stage 1 --exp-name demo --resume /path/to/the/checkpoint --input 10025.jpg --draw_text
```

- to detect facial action units in a facial image using our stage2 model, run:
```
uv run -m OpenGraphAU.main --arc resnet50 --stage 2 --exp-name demo --resume /path/to/the/checkpoint --input 10025.jpg --draw_text
```

## 🖊️ Citation

If you find this work useful in your research, please cite:

```bibtex
@inproceedings{luo2022learning,
  title     = {Learning Multi-dimensional Edge Feature-based AU Relation Graph for Facial Action Unit Recognition},
  author    = {Luo, Cheng and Song, Siyang and Xie, Weicheng and Shen, Linlin and Gunes, Hatice},
  booktitle = {Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence, {IJCAI-22}},
  pages     = {1239--1246},
  year      = {2022}
}
```

